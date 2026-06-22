# Harness Check Report

## Summary

- task_id: result_conflict
- mode: full
- result: **BLOCKED**

## Required Files

| File | Status | Severity |
|---|---|---|
| SDD.md | ❌ | BLOCKED |
| ConflictReport.md | ❌ | BLOCKED |
| REVIEW.md | ❌ | BLOCKED |
| TestReport.md | ❌ | BLOCKED |
| metrics.yaml | ✅ | OK |
| TaskSpec.md | ❌ | OK |
| ChangedFiles.md | ❌ | OK |
| RiskReport.md | ❌ | OK |
| retrospective.md | ❌ | OK |

## Metrics Check

| Field | Status | Severity |
|---|---|---|
| task_id | ❌ | BLOCKED |
| mode | ✅ | OK |
| result | ✅ | OK |
| build | ✅ | OK |
| review | ✅ | OK |
| scope | ✅ | OK |
| user_verified | ✅ | OK |
| regression_required | ✅ | OK |
| skill_patch_required | ✅ | OK |
| build.attempted | ✅ | OK |
| build.passed | ✅ | OK |
| review.attempted | ✅ | OK |
| review.verdict | ✅ | OK |
| scope.unrelated_files_changed | ✅ | OK |
| scope.violations | ✅ | OK |

## Scope Check

| Item | Status | Severity |
|---|---|---|
| mode == full | ✅ | OK |
| result=approved requires build.passed=true | ❌ | BLOCKED |
| result=approved requires user_verified=true | ❌ | BLOCKED |
| review.verdict=REJECTED cannot have result=approved | ✅ | OK |
| scope.unrelated_files_changed == 0 | ✅ | OK |
| scope.violations empty when result=approved | ✅ | OK |

## Violations

- [BLOCKED] Missing required file: SDD.md
- [BLOCKED] Missing required file: ConflictReport.md
- [BLOCKED] Missing required file: REVIEW.md
- [BLOCKED] Missing required file: TestReport.md
- [BLOCKED] Missing metrics field: task_id
- [BLOCKED] result=approved requires build.passed=true
- [BLOCKED] result=approved requires user_verified=true
- [WARNING] Missing optional file: TaskSpec.md
- [WARNING] Missing optional file: ChangedFiles.md
- [WARNING] Missing optional file: RiskReport.md
- [WARNING] Missing optional file: retrospective.md

## Recommended Action

- Fix BLOCKED items before proceeding.
