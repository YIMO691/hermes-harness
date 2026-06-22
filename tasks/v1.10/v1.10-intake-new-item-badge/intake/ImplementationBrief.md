# Implementation Brief

## Task ID
v1.10-intake-new-item-badge

## Goal
背包物品增加"最近获得"标记（NEW badge），30 秒后自动消失。

## A1 Resolution ✅
确认方案：MockData.GetItems() 初始化时设置 `acquiredTime = DateTime.Now`。本地模拟，不接服务器/掉落/持久化。

## Confirmed Requirements
- NEW 标记持续 30 秒
- 切换页签后未超时仍显示
- 关闭再打开背包后未超时仍显示
- 不做持久化 / 不涉及服务器 / 不修改排序

## Proposed Changes
1. `ItemData.cs` — add `acquiredTime` field + `IsNew` property
2. `InventoryMockData.cs` — set `acquiredTime = DateTime.Now` on each item
3. `InventorySlotView.cs` — append " [NEW]" to nameText when IsNew
4. `InventoryPanel.cs` — show remaining time in detailText (optional)

## Acceptance Criteria
See `AcceptanceCriteria.md` — 11 items.

## Recommended Workline Mode
**quick** — 3-4 files, ~15 lines, no architecture change.
