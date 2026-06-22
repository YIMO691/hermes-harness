# SDD — v1.8 harness case runner

## Code Inventory

| File | Exists | This Change |
|:---|:--:|:---|
| tools/check_workline_task.py | ✅ | unchanged |
| tests/harness_check/valid_quick/ | ✅ | unchanged |
| tests/harness_check/missing_metrics_lite/ | ✅ | unchanged |
| tests/harness_check/full_missing_review/ | ✅ | unchanged |
| tests/harness_check/result_conflict/ | ✅ | unchanged |
| tests/harness_check/run_harness_check_cases.py | ❌ | NEW |

## Gap Analysis

| Requirement | Status |
|:---|:---|
| Run 4 fixture cases | missing |
| Validate exit codes | missing |
| Print summary | missing |

## Tasks

### Task 1: Create run_harness_check_cases.py

File: tests/harness_check/run_harness_check_cases.py

Content: Python script that:
1. Defines 4 test cases with expected exit codes
2. Runs each via subprocess
3. Compares actual vs expected exit code
4. Prints "4/4" or failure details
5. Exits 0 on all pass, non-zero otherwise

## Dependency Graph

```
Task 1 (standalone — depends on existing fixtures only)
```

## Acceptance Checklist

- [ ] `python tests/harness_check/run_harness_check_cases.py` outputs "4/4"
- [ ] Exit code 0 on all pass
- [ ] Exit code != 0 on failure

## Non-Goals

- 不修改 skills/
- 不修改 regression/
- 不修改 checker 规则
