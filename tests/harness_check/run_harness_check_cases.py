#!/usr/bin/env python3
"""v1.8 harness check — test runner for 4 fixture cases.

Usage:
  python tests/harness_check/run_harness_check_cases.py

Exit: 0 if all cases match expected exit codes, 1 otherwise.
"""

import subprocess
import sys

CHECKER = "tools/check_workline_task.py"
BASE = "tests/harness_check"

CASES = [
    ("valid_quick", "quick", 0),
    ("missing_metrics_lite", "quick", 2),
    ("full_missing_review", "full", 2),
    ("result_conflict", "full", 2),
]

failed = 0
for name, mode, expected in CASES:
    task_dir = f"{BASE}/{name}"
    result = subprocess.run(
        [sys.executable, CHECKER, "--task", task_dir, "--mode", mode],
        capture_output=True, text=True
    )
    actual = result.returncode
    status = "PASS" if actual == expected else "FAIL"
    if actual != expected:
        failed += 1
        print(f"[{status}] {name}: expected exit {expected}, got {result.returncode}")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"[{status}] {name}: exit {actual}")

total = len(CASES)
passed = total - failed
print(f"\n{passed}/{total} harness check cases passed")

sys.exit(0 if failed == 0 else 1)
