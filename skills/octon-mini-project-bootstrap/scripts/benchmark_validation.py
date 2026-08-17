#!/usr/bin/env python3
"""Measure scaffold, check, and bounded mutation costs without retaining projects."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


CHECK_TARGET_SECONDS = 2.0
MUTATION_TARGET_SECONDS = 10.0
SCAFFOLD_TARGET_SECONDS = 10.0
DEFAULT_SIZES = (0, 2_000, 10_000, 20_000)
PROFILES = ("minimal", "standard", "high-assurance")


def timed(argv: list[str], cwd: Path) -> tuple[float, subprocess.CompletedProcess[str]]:
    started = time.perf_counter()
    result = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
        shell=False,
    )
    return time.perf_counter() - started, result


def require_success(label: str, sample: tuple[float, subprocess.CompletedProcess[str]]) -> float:
    elapsed, result = sample
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"{label} failed ({result.returncode}): {detail}")
    return elapsed


def percentile_90(values: list[float]) -> float:
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = max(0, int(len(ordered) * 0.9 + 0.999999) - 1)
    return ordered[min(index, len(ordered) - 1)]


def write_payload(root: Path, current: int, target: int) -> None:
    payload = root / "benchmark-payload"
    payload.mkdir(exist_ok=True)
    for index in range(current, target):
        bucket = payload / f"b{index // 1000:03d}"
        bucket.mkdir(exist_ok=True)
        (bucket / f"f{index:05d}.txt").write_text(
            f"bounded benchmark payload {index}\n",
            encoding="utf-8",
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local, content-free validation scale benchmarks."
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=list(DEFAULT_SIZES),
        help="cumulative synthetic repository file counts",
    )
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()
    if (
        args.samples < 1
        or any(size < 0 for size in args.sizes)
        or args.sizes != sorted(set(args.sizes))
    ):
        parser.error("sizes must be unique ascending nonnegative values; samples >= 1")

    script_root = Path(__file__).resolve().parent
    scaffold = script_root / "scaffold_project.py"
    with tempfile.TemporaryDirectory(prefix="octon-mini-validation-scale-") as temporary:
        area = Path(temporary)
        scaffold_measurements: list[dict[str, object]] = []
        for profile in PROFILES:
            values: list[float] = []
            for sample in range(args.samples):
                destination = area / f"{profile}-sample-{sample}"
                values.append(
                    require_success(
                        f"{profile} scaffold sample {sample + 1}",
                        timed(
                            [
                                sys.executable,
                                str(scaffold),
                                "--project-name",
                                f"{profile.title()} Validation Benchmark",
                                "--profile",
                                profile,
                                "--layout",
                                "compact",
                                "--target",
                                str(destination),
                            ],
                            script_root,
                        ),
                    )
                )
            scaffold_measurements.append(
                {
                    "profile": profile,
                    "layout": "compact",
                    "seconds": values,
                    "p90_seconds": percentile_90(values),
                }
            )
        target = area / "minimal-sample-0"
        measurements: list[dict[str, object]] = []
        current = 0
        for size in args.sizes:
            write_payload(target, current, size)
            current = size
            refresh = require_success(
                f"refresh at {size}",
                timed(
                    [sys.executable, "-B", ".agent/scripts/refresh.py", "--refresh"],
                    target,
                ),
            )
            checks = [
                require_success(
                    f"check at {size}",
                    timed(
                        [sys.executable, "-B", ".agent/scripts/validate.py", "--check"],
                        target,
                    ),
                )
                for _ in range(args.samples)
            ]
            mutations = [
                require_success(
                    f"fast mutation tier at {size}",
                    timed(
                        [
                            sys.executable,
                            "-B",
                            ".agent/tests/test_validate.py",
                            "--tier",
                            "fast",
                        ],
                        target,
                    ),
                )
                for _ in range(args.samples)
            ]
            measurements.append(
                {
                    "synthetic_payload_files": size,
                    "refresh_seconds": refresh,
                    "check_seconds": checks,
                    "check_p90_seconds": percentile_90(checks),
                    "fast_mutation_seconds": mutations,
                    "fast_mutation_p90_seconds": percentile_90(mutations),
                }
            )

    report = {
        "schema_version": "octon-mini.project.validation-benchmark.v1",
        "document_role": "local_content_free_non_authorizing_measurement",
        "scaffold_profiles": scaffold_measurements,
        "measurements": measurements,
        "thresholds": {
            "scaffold_seconds": SCAFFOLD_TARGET_SECONDS,
            "check_p90_seconds_at_10000_files": CHECK_TARGET_SECONDS,
            "fast_mutation_seconds": MUTATION_TARGET_SECONDS,
        },
        "limitations": [
            "Synthetic small files do not represent every filesystem or repository shape.",
            "Wall-clock results are host-specific and are never readiness evidence.",
        ],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if not args.enforce:
        return 0
    failures: list[str] = []
    for row in scaffold_measurements:
        if row["p90_seconds"] >= SCAFFOLD_TARGET_SECONDS:
            failures.append(f"{row['profile']} scaffold p90 threshold exceeded")
    for row in measurements:
        if row["fast_mutation_p90_seconds"] >= MUTATION_TARGET_SECONDS:
            failures.append(
                f"fast mutation threshold exceeded at {row['synthetic_payload_files']} files"
            )
        if (
            row["synthetic_payload_files"] == 10_000
            and row["check_p90_seconds"] >= CHECK_TARGET_SECONDS
        ):
            failures.append("10,000-file check threshold exceeded")
    for failure in failures:
        print(f"[FAIL] {failure}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
