# WorklineSummary

## Task
v1.10-new-item-badge-quick — 背包 NEW 标记 quick 任务

## Source Intake
- Path: `tasks/v1.10/v1.10-intake-new-item-badge/intake/`
- A1 status: RESOLVED — MockData 初始化时设置 acquiredTime

## Confirmed A1 Decision
MockData.GetItems() 中为每个 ItemData 设置 `acquiredTime = DateTime.Now`。本地模拟，不接服务器/掉落/持久化。

## Detected Files
```
Assets/Scripts/Inventory/ItemData.cs           ← data model
Assets/Scripts/Inventory/InventoryMockData.cs   ← static init
Assets/Scripts/Inventory/InventorySlotView.cs   ← slot display
Assets/Scripts/Inventory/InventoryPanel.cs      ← main controller
Assets/Scripts/Inventory/ItemType.cs            ← enum (no change)
```

## Proposed Changes
| File | Change | Lines |
|:---|:---|:--:|
| ItemData.cs | + acquiredTime field + IsNew property | +6 |
| InventoryMockData.cs | set acquiredTime on each item | +6 |
| InventorySlotView.cs | append " [NEW]" when IsNew | +1 |
| InventoryPanel.cs | show remaining time in detailText | +3 |

## Non-goals
- 不新增 UI 控件
- 不修改排序
- 不涉及网络/配置/资源
- 不做持久化

## Acceptance Criteria
- [ ] 物品显示 NEW 标记
- [ ] 30s 后自动消失
- [ ] 切换页签未超时仍显示
- [ ] 关闭再打开未超时仍显示
- [ ] 与 ★ 收藏标记共存
- [ ] 不破坏现有筛选

## Risks
- ★ 和 NEW 同时显示时 nameText 长度 — 测试覆盖
- 30s 阈值需手动验证 — Unity Play

## Recommended Next Action
进入 quick 实现 — 4 files, ~16 lines.
