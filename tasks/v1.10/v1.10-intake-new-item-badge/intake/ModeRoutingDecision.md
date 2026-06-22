# Mode Routing Decision

## Current Routing

```
clarification-only
```

**Reason**: BLOCKER A1 exists — "获得新物品"的触发方式未确认。当前 BackpackDemo 的 MockData 是静态初始化，没有"获得"动作。在确认触发方式之前，实现层无法正确设置 `acquiredTime`。

## Conditional Routing After A1 Resolved

```
quick
```

**Reason**: 如果 A1 确认为以下任一方案，实现很小：
- 方案 A: 添加测试按钮模拟获得 → 3 files, ~15 lines
- 方案 B: MockData 初始化时设置 acquiredTime → 2 files, ~10 lines
- 方案 C: 用户提供真实触发逻辑 → 根据复杂度可能升级 full

无论哪种，架构范围不变：无网络、无配置表、无资源、无性能影响。

## Blocking Questions

1. **BLOCKER A1**: "获得新物品"的触发来源是什么？
   - 选项 A: 新增一个 GM/测试按钮，点击后背包中随机物品获得 NEW
   - 选项 B: MockData 初始化时给所有物品设置 `acquiredTime = DateTime.Now`
   - 选项 C: 用户提供真实拾取/购买逻辑
   - **必须用户选择后，才允许进入实现。**

## Scope
- Files: ItemData.cs, InventorySlotView.cs, InventoryPanel.cs（3 files）
- Lines: ~15 additions

## Handoff Target
- After A1 resolved → enter v1.7/v1.8/v1.9 pipeline as quick task
- checker: `python tools/check_workline_task.py --task <dir> --mode quick`
- Expected: PASS
