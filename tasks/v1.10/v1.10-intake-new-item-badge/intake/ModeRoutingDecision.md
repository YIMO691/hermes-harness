# Mode Routing Decision

## Current Routing

```
quick
```

**Reason**: A1 resolved — "获得"触发方式确认为 MockData 初始化时设置 acquiredTime。实现范围：2-3 文件，~15 行，无网络/配置/资源/性能影响。

## A1 Resolution

- **Decision**: MockData.GetItems() 中给每个 ItemData 设置 `acquiredTime = DateTime.Now`
- **Impact**: ItemData.cs (+1 field +1 property), InventoryMockData.cs (+1 line per item), InventorySlotView.cs (+1 line), InventoryPanel.cs (+2 lines)
- **Files**: 3 (ItemData + MockData + SlotView) or 4 (with Panel detail display)

## Scope
- Files: ItemData.cs, InventoryMockData.cs, InventorySlotView.cs, InventoryPanel.cs
- Lines: ~15 additions
- Mode: quick — no architecture, no new UI

## Handoff Target
- Enter v1.7/v1.8/v1.9 pipeline as quick task
- checker: `python tools/check_workline_task.py --task <dir> --mode quick`
- Expected: PASS
