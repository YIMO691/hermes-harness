# Ambiguity Report

## Summary
- Total: 8 ambiguous points found
- BLOCKER: 0 ✅
- HIGH: 2
- MEDIUM: 3
- LOW: 2

---

## RESOLVED

### ~~A1. "获得新物品"的触发来源~~ → RESOLVED ✅
**Decision**: MockData 初始化时设置 `acquiredTime = DateTime.Now`。本地模拟，不接服务器/掉落/持久化。
**Evidence**: InventoryPanel.Start() → InventoryMockData.GetItems() → ItemData 列表。入口点为 MockData 初始化。
**Impact**: 2 files (ItemData.cs + InventoryMockData.cs)，无新方法，无新 UI。

---

## HIGH

### A2. 多次获得同一物品是否刷新计时
**问题**: 如果玩家已经拥有"铁剑"（剩余 10s NEW），又获得一把"铁剑"，NEW 是否回到 30s？
**影响**: 影响计时逻辑设计。
**Assumption**: 默认刷新计时。当前 MockData 无动态添加，此问题在真实场景才触发。可延后。

### A3. NEW 标记的视觉表现
**问题**: 文档只说"显示 NEW 标记"，未指定形式。
**Assumption**: 使用文本后缀 " [NEW]" 追加到 nameText。与收藏功能（★）一致。

---

## MEDIUM / LOW (unchanged from original)
