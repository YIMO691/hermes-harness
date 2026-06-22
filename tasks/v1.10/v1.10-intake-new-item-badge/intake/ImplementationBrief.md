# Implementation Brief

## Task ID
v1.10-intake-new-item-badge

## Goal
背包物品增加"最近获得"标记（NEW badge），30 秒后自动消失。

## Confirmed Requirements
- NEW 标记持续 30 秒
- 切换页签后未超时仍显示
- 关闭再打开背包后未超时仍显示
- 不做持久化
- 不涉及服务器
- 不修改排序规则

## Explicit Non-goals
- 不做持久化
- 不涉及服务器
- 不修改排序
- 不新增 UI 控件
- 不修改配置表

## Files Likely Involved
1. `Assets/Scripts/Inventory/ItemData.cs` — add `acquiredTime` + `IsNew` property
2. `Assets/Scripts/Inventory/InventorySlotView.cs` — append " [NEW]" to nameText
3. `Assets/Scripts/Inventory/InventoryPanel.cs` — show remaining time in detailText

## Implementation Constraints
- Keep existing null checks
- Reuse existing nameText (no new GameObjects)
- Use DateTime.Now for time comparison (no Update() polling)
- [Assumption] Multiple items each have independent timers
- [Assumption] Timer continues when backpack panel is closed
- [Assumption] Default visual is text suffix " [NEW]"

## Acceptance Criteria
See `AcceptanceCriteria.md` — 11 items.

## Risks
- BLOCKER A1: "获得"触发方式未确认 → test via MockData modification
- Coexistence with ★ favorite marker: need to test combined display

## Recommended Workline Mode
**Current**: clarification-only (BLOCKER A1 pending)
**After A1 resolved**: quick — 3 files, ~15 lines, no architecture change.

## Blocking Issue
BLOCKER A1: "获得新物品"的触发方式未确认。需要用户选择方案 A/B/C 后进入实现。
方案 A: 测试按钮 → 3 files
方案 B: MockData初始化 → 2 files  
方案 C: 真实逻辑 → 可能升级 full
