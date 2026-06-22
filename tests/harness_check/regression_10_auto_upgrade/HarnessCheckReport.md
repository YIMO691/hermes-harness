# Harness Check Report

## Summary

- task_id: regression_10_auto_upgrade
- mode: quick
- result: **BLOCKED**

## Required Files

| File | Status | Severity |
|---|---|---|
| WorklineSummary.md | ✅ | OK |
| metrics-lite.yaml | ✅ | OK |

## Metrics Check

| Field | Status | Severity |
|---|---|---|
| task_id | ✅ | OK |
| mode | ✅ | OK |
| result | ✅ | OK |
| changed_files | ✅ | OK |
| build | ✅ | OK |
| user_verified | ✅ | OK |
| scope | ✅ | OK |
| auto_upgrade | ✅ | OK |
| build.passed | ✅ | OK |

## Scope Check

| Item | Status | Severity |
|---|---|---|
| mode == quick | ✅ | OK |
| result=approved requires build.passed=true | ✅ | OK |
| result=approved requires user_verified=true | ✅ | OK |
| auto_upgrade.required=true cannot have result=approved | ❌ | BLOCKED |
| scope.violations empty when result=approved | ✅ | OK |

## Violations

- [BLOCKED] auto_upgrade.required=true cannot have result=approved

## Recommended Action

- Fix BLOCKED items before proceeding.
