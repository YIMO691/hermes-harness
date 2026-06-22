# WorklineSummary

## Task
Fix dropdown filter not working — TypeDropdown onChange listener commented out.
Mode: quick — single-file fix.

## Fix
Restored `TypeDropdown.onValueChanged.AddListener(_ => RefreshList());`

## Verification
| Check | Result |
|:---|---|
| Build | pass |
| Test | dropdown filter works after fix |

## Risks
- none
