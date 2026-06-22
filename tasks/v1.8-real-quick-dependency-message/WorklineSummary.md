# WorklineSummary

## Task
Improve PyYAML dependency error message in check_workline_task.py.
Mode: quick — single-file fix, no architecture change.

## Context Audit (minimal)
- File: tools/check_workline_task.py
- Change: lines 22-28, replace error message block

## Fix
Before: `ERROR: PyYAML required. Install: pip install pyyaml`
After: multi-line message with explicit `pip install -r requirements-dev.txt`

## Verification
| Check | Result |
|:---|---|
| Code review | pass — 3 lines changed, no logic impact |
| Scope check | pass — 1 file modified |

## Risks
- none
