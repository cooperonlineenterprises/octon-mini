#!/usr/bin/env python3
"""Focused methodology tests for the v2 validation benchmark."""

from __future__ import annotations

import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock


sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().with_name("benchmark_validation.py")
SOURCE_VALIDATOR_SCRIPT = Path(__file__).resolve().with_name(
    "validate_source_contracts.py"
)
SKILL_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = next(
    candidate
    for candidate in (
        Path(__file__).resolve().parents[3],
        SKILL_ROOT / "assets/octon-mini-source",
    )
    if (candidate / "shared/source-contracts").is_dir()
)
BENCHMARK_SCHEMA = (
    SOURCE_ROOT / "shared/source-contracts/validation-benchmark-report.schema.json"
)


def load_benchmark() -> types.ModuleType:
    spec = importlib.util.spec_from_file_location("octon_mini_benchmark_test", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("benchmark module cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    finally:
        sys.modules.pop(spec.name, None)
    return module


BENCHMARK = load_benchmark()


def load_source_validator() -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(
        "octon_mini_benchmark_schema_test", SOURCE_VALIDATOR_SCRIPT
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("source-contract validator cannot be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SOURCE_VALIDATOR = load_source_validator()


def sample(
    sequence: int,
    classification: str,
    seconds: float,
    *,
    exit_code: int = 0,
) -> dict[str, object]:
    return {
        "sequence": sequence,
        "classification": classification,
        "seconds": seconds,
        "exit_code": exit_code,
        "load_average_before": None,
        "load_average_after": None,
    }


class BenchmarkMethodologyTests(unittest.TestCase):
    def test_nearest_rank_p90_is_explicit_and_deterministic(self) -> None:
        self.assertEqual(BENCHMARK.percentile_90([3.0]), 3.0)
        self.assertEqual(
            BENCHMARK.percentile_90([10.0, 1.0, 9.0, 2.0, 8.0, 3.0, 7.0, 4.0, 6.0, 5.0]),
            9.0,
        )
        self.assertEqual(BENCHMARK.percentile_90([float(value) for value in range(1, 12)]), 10.0)
        with self.assertRaises(ValueError):
            BENCHMARK.percentile_90([])

    def test_configuration_rejects_malformed_or_weak_enforced_runs(self) -> None:
        configuration = BENCHMARK.BenchmarkConfiguration
        cases = (
            configuration(sizes=(), warm_samples=10),
            configuration(sizes=(-1,), warm_samples=10),
            configuration(sizes=(0, 0), warm_samples=10),
            configuration(sizes=(10_000, 2_000), warm_samples=10),
            configuration(sizes=(10_000,), warm_samples=0),
            configuration(sizes=(10_000,), warm_samples=9, enforce=True),
            configuration(sizes=(0, 2_000), warm_samples=10, enforce=True),
        )
        for case in cases:
            with self.subTest(case=case):
                self.assertTrue(BENCHMARK.configuration_errors(case))
        self.assertEqual(
            BENCHMARK.configuration_errors(
                configuration(sizes=(0, 10_000), warm_samples=10, enforce=True)
            ),
            [],
        )

    def test_default_report_is_v2_content_free_and_non_authorizing(self) -> None:
        configuration = BENCHMARK.BenchmarkConfiguration(sizes=(10_000,))
        with tempfile.TemporaryDirectory(prefix="octon-mini benchmark report ") as temporary:
            report = BENCHMARK.initial_report(configuration, Path(temporary))
        self.assertEqual(
            report["schema_version"], "octon-mini.project.validation-benchmark.v2"
        )
        self.assertIs(report["permission_grant"], False)
        config = report["benchmark_configuration"]
        self.assertEqual(config["warm_samples_per_series"], 10)
        self.assertEqual(config["cold_start_proxy_samples_per_series"], 1)
        self.assertEqual(config["percentile"]["name"], "nearest_rank")
        self.assertIs(config["independent_target_per_payload_size"], True)
        self.assertIn("independent destinations", config["cache_policy"]["warm_steady_state"])
        encoded = json.dumps(report, sort_keys=True)
        self.assertNotIn(temporary, encoded)
        self.assertNotIn(str(Path.home()), encoded)
        self.assertNotIn("hostname", encoded.casefold())
        self.assertEqual(report["sample_accounting"]["expected_samples"], 57)

    def test_default_report_conforms_to_the_v2_source_schema(self) -> None:
        configuration = BENCHMARK.BenchmarkConfiguration(sizes=(10_000,))
        with tempfile.TemporaryDirectory(prefix="octon-mini benchmark schema ") as temporary:
            report = BENCHMARK.initial_report(configuration, Path(temporary))
        schema = json.loads(BENCHMARK_SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(
            SOURCE_VALIDATOR.schema_issues(report, schema, "benchmark-report"),
            [],
        )

    def test_series_preserves_cold_and_warm_samples_and_both_p90_values(self) -> None:
        series = BENCHMARK.empty_series()
        series["samples"] = [
            sample(1, BENCHMARK.COLD_CLASSIFICATION, 99.0),
            *[
                sample(index + 2, BENCHMARK.WARM_CLASSIFICATION, float(index + 1))
                for index in range(10)
            ],
        ]
        BENCHMARK.summarize_series(series)
        self.assertEqual(series["combined_p90_seconds"], 10.0)
        self.assertEqual(series["warm_p90_seconds"], 9.0)
        self.assertEqual(len(series["samples"]), 11)
        self.assertEqual(series["samples"][0]["classification"], BENCHMARK.COLD_CLASSIFICATION)

    def test_sample_accounting_counts_every_classification(self) -> None:
        configuration = BENCHMARK.BenchmarkConfiguration(sizes=(10_000,))
        with tempfile.TemporaryDirectory() as temporary:
            report = BENCHMARK.initial_report(configuration, Path(temporary))
        sequence = 0
        for profile in BENCHMARK.PROFILES:
            samples = []
            for classification in [BENCHMARK.COLD_CLASSIFICATION] + [
                BENCHMARK.WARM_CLASSIFICATION
            ] * 10:
                sequence += 1
                samples.append(sample(sequence, classification, 0.1))
            report["scaffold_profiles"].append(
                {
                    "profile": profile,
                    "layout": "compact",
                    "samples": samples,
                    "combined_p90_seconds": 0.1,
                    "warm_p90_seconds": 0.1,
                }
            )
        preparation = []
        for _ in range(2):
            sequence += 1
            preparation.append(sample(sequence, BENCHMARK.PREPARATION_CLASSIFICATION, 0.1))
        check_samples = []
        mutation_samples = []
        for destination in (check_samples, mutation_samples):
            for classification in [BENCHMARK.COLD_CLASSIFICATION] + [
                BENCHMARK.WARM_CLASSIFICATION
            ] * 10:
                sequence += 1
                destination.append(sample(sequence, classification, 0.1))
        report["measurements"].append(
            {
                "synthetic_payload_files": 10_000,
                "preparation_samples": preparation,
                "check": {
                    "samples": check_samples,
                    "combined_p90_seconds": 0.1,
                    "warm_p90_seconds": 0.1,
                },
                "fast_mutation": {
                    "samples": mutation_samples,
                    "combined_p90_seconds": 0.1,
                    "warm_p90_seconds": 0.1,
                },
            }
        )
        BENCHMARK.update_sample_accounting(report)
        accounting = report["sample_accounting"]
        self.assertEqual(accounting["observed_samples"], 57)
        self.assertEqual(accounting["successful_samples"], 57)
        self.assertEqual(accounting["failed_samples"], 0)
        self.assertEqual(
            accounting["by_classification"],
            {
                BENCHMARK.COLD_CLASSIFICATION: 5,
                BENCHMARK.WARM_CLASSIFICATION: 50,
                BENCHMARK.PREPARATION_CLASSIFICATION: 2,
            },
        )
        self.assertIs(accounting["complete"], True)

    def test_enforcement_uses_unchanged_strict_thresholds(self) -> None:
        report = {
            "scaffold_profiles": [
                {
                    "profile": "minimal",
                    "combined_p90_seconds": BENCHMARK.SCAFFOLD_TARGET_SECONDS,
                }
            ],
            "measurements": [
                {
                    "synthetic_payload_files": 10_000,
                    "check": {
                        "combined_p90_seconds": BENCHMARK.CHECK_TARGET_SECONDS,
                        "warm_p90_seconds": BENCHMARK.CHECK_TARGET_SECONDS,
                    },
                    "fast_mutation": {
                        "combined_p90_seconds": BENCHMARK.MUTATION_TARGET_SECONDS,
                        "warm_p90_seconds": BENCHMARK.MUTATION_TARGET_SECONDS,
                    },
                }
            ],
        }
        failures = BENCHMARK.threshold_failures(report)
        self.assertEqual(len(failures), 5)
        report["scaffold_profiles"][0]["combined_p90_seconds"] -= 0.001
        for series in (report["measurements"][0]["check"], report["measurements"][0]["fast_mutation"]):
            series["combined_p90_seconds"] -= 0.001
            series["warm_p90_seconds"] -= 0.001
        self.assertEqual(BENCHMARK.threshold_failures(report), [])

    def test_command_failure_remains_in_partial_report(self) -> None:
        def failed_timed(
            _argv: list[str],
            _cwd: Path,
            *,
            classification: str,
            sequence: int,
        ) -> tuple[dict[str, object], subprocess.CompletedProcess[str]]:
            value = sample(sequence, classification, 0.25, exit_code=7)
            return value, subprocess.CompletedProcess([], 7, stdout="sensitive", stderr="detail")

        configuration = BENCHMARK.BenchmarkConfiguration(sizes=(0,), warm_samples=1)
        with mock.patch.object(BENCHMARK, "PROFILES", ("minimal",)), mock.patch.object(
            BENCHMARK, "timed", side_effect=failed_timed
        ):
            report, status = BENCHMARK.run_benchmark(configuration)
        self.assertEqual(status, 1)
        self.assertEqual(report["enforcement"]["status"], "measurement_failed")
        self.assertEqual(report["sample_accounting"]["observed_samples"], 1)
        self.assertEqual(report["sample_accounting"]["failed_samples"], 1)
        self.assertEqual(report["scaffold_profiles"][0]["samples"][0]["exit_code"], 7)
        self.assertEqual(report["execution_failures"][0]["sequence"], 1)
        encoded = json.dumps(report)
        self.assertNotIn('"sensitive"', encoded)
        self.assertNotIn('"detail"', encoded)

    def test_timed_command_forces_no_bytecode_environment(self) -> None:
        completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
        with mock.patch.object(BENCHMARK.subprocess, "run", return_value=completed) as invoked:
            measured, result = BENCHMARK.timed(
                [sys.executable, "-B", "example.py"],
                Path.cwd(),
                classification=BENCHMARK.WARM_CLASSIFICATION,
                sequence=3,
            )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(measured["sequence"], 3)
        kwargs = invoked.call_args.kwargs
        self.assertEqual(kwargs["env"]["PYTHONDONTWRITEBYTECODE"], "1")
        self.assertIs(kwargs["shell"], False)

    def test_main_prints_partial_report_before_failure_diagnostics(self) -> None:
        report = {
            "schema_version": BENCHMARK.SCHEMA_VERSION,
            "enforcement": {
                "enabled": False,
                "status": "measurement_failed",
                "failures": ["benchmark sample accounting is incomplete"],
            },
            "execution_failures": [
                {"stage": "scaffold_profile.minimal", "sequence": 1, "exit_code": 7}
            ],
        }
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(BENCHMARK, "parse_args", return_value=object()), mock.patch.object(
            BENCHMARK, "run_benchmark", return_value=(report, 1)
        ), redirect_stdout(stdout), redirect_stderr(stderr):
            status = BENCHMARK.main([])
        self.assertEqual(status, 1)
        self.assertEqual(json.loads(stdout.getvalue())["schema_version"], BENCHMARK.SCHEMA_VERSION)
        self.assertIn("scaffold_profile.minimal", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
