# Harness Check Report

## Summary

- task_id: missing_metrics_lite
- mode: quick
- result: **BLOCKED**

## Required Files

| File | Status | Severity |
|---|---|---|
| WorklineSummary.md | ✅ | OK |
| metrics-lite.yaml | ❌ | BLOCKED |

## Metrics Check

| Field | Status | Severity |
|---|---|---|
| task_id | ❌ | BLOCKED |
| mode | ❌ | BLOCKED |
| result | ❌ | BLOCKED |
| changed_files | ❌ | BLOCKED |
| build | ❌ | BLOCKED |
| user_verified | ❌ | BLOCKED |
| scope | ❌ | BLOCKED |
| auto_upgrade | ❌ | BLOCKED |
| build.passed | ❌ | BLOCKED |

## Scope Check

| Item | Status | Severity |
|---|---|---|
| mode == quick | ❌ | BLOCKED |
| result=approved requires build.passed=true | ✅ | OK |
| result=approved requires user_verified=true | ✅ | OK |
| auto_upgrade.required=true cannot have result=approved | ✅ | OK |
| scope.violations empty when result=approved | ✅ | OK |

## Violations

- [BLOCKED] Missing required file: metrics-lite.yaml
- [BLOCKED] Missing metrics field: task_id
- [BLOCKED] Missing metrics field: mode
- [BLOCKED] Missing metrics field: result
- [BLOCKED] Missing metrics field: changed_files
- [BLOCKED] Missing metrics field: build
- [BLOCKED] Missing metrics field: user_verified
- [BLOCKED] Missing metrics field: scope
- [BLOCKED] Missing metrics field: auto_upgrade
- [BLOCKED] Missing metrics field: build.passed
- [BLOCKED] mode == quick

## Recommended Action

- Fix BLOCKED items before proceeding.
