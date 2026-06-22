# Task Breakdown

## Epic: Backpack New Item Badge
背包物品增加"最近获得"标记。

---

## Feature 1: Data Layer — acquiredTime

### Task 1.1: Add acquiredTime to ItemData
- File: `Assets/Scripts/Inventory/ItemData.cs`
- Subtask: add `public DateTime acquiredTime { get; set; }`
- Subtask: add helper `public bool IsNew => (DateTime.Now - acquiredTime).TotalSeconds < 30`
- Codex: ✅
- Mode: quick
- Dependency: none

---

## Feature 2: UI Layer — NEW display

### Task 2.1: Update InventorySlotView to show NEW
- File: `Assets/Scripts/Inventory/InventorySlotView.cs`
- Subtask: in Setup(), if item.IsNew, append " [NEW]" to nameText
- Codex: ✅
- Mode: quick
- Dependency: Task 1.1

### Task 2.2: Update InventoryPanel detail display
- File: `Assets/Scripts/Inventory/InventoryPanel.cs`
- Subtask: in UpdateDetailDisplay(), show NEW status + remaining seconds
- Codex: ✅
- Mode: quick
- Dependency: Task 1.1

### Task 2.3: Update InventoryPanel refresh logic
- File: `Assets/Scripts/Inventory/InventoryPanel.cs`
- Subtask: RefreshList already re-renders all slots — NEW display updates automatically
- Subtask: No additional changes needed (IsNew is dynamic, recalculated each frame)
- Codex: N/A
- Mode: same task as 2.2

---

## Feature 3: Test / Validation

### Task 3.1: Add test item acquisition
- File: optionally add a button or modify MockData to set acquiredTime
- Subtask: set MockData items' acquiredTime to DateTime.Now for testing
- Codex: optional
- Mode: quick
- Dependency: Task 1.1

---

## Summary

| # | Task | Files | Mode | Depends On |
|:--|:---|:---|:--:|:---|
| 1 | ItemData acquiredTime | ItemData.cs | quick | — |
| 2 | SlotView NEW display | InventorySlotView.cs | quick | 1 |
| 3 | Panel detail + refresh | InventoryPanel.cs | quick | 1 |
| 4 | Test acquisition | MockData (optional) | quick | 1 |

**Recommendation**: 4 tasks, all quick. No architecture decisions, no UI restructure, no network/config/resource changes. Can be a single quick feature if combined.

**Split?** No — scope is small enough for sequential quick tasks or one combined quick task.
