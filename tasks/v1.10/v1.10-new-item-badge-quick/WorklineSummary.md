# WorklineSummary

## Task
v1.10-new-item-badge-quick — 背包 NEW 标记 quick 实现

## Source Intake
- Path: `tasks/v1.10/v1.10-intake-new-item-badge/intake/`
- A1 status: RESOLVED — MockData 初始化时设置 acquiredTime

## Confirmed A1 Decision
MockData.GetItems() 中为每个 ItemData 设置 `acquiredTime = DateTime.Now`。

## Implementation
| File | Change | Lines |
|:---|:---|:--:|
| ItemData.cs | + acquiredTime field + IsNew property | +3 |
| InventoryMockData.cs | set acquiredTime on each item + using System | +7/-6 |
| InventorySlotView.cs | append " [NEW]" when IsNew | +1/-1 |
| InventoryPanel.cs | show remaining seconds in detailText | +2/-1 |

Repository: BackpackDemo
Commit: `5b0ced9` (feat) + `6683f66` (fix: missing using System)

## Verification
- Unity Play: PASSED ✅
- NEW 标记显示正常
- 30s 内切换页签仍显示
- 关闭再打开仍显示
- 超过 30s 后消失
- 排序不变
- Console 无阻断性错误

## Mode Check
- [x] quick scope maintained
- [x] no architecture changes
- [x] no new UI controls
- [x] no network/config/resource changes

## Risks
- None — verified in Unity Play
