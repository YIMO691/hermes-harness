# Client Impact Map

| Area | Impact | Required Action | Evidence | Risk |
|:---|:--:|:---|:---|:---|
| UI / View | Yes | nameText 追加 NEW 标记；detailText 追加倒计时 | 现有 InventorySlotView + InventoryPanel | 低 |
| UI State | No | N/A | — | — |
| Data Model | Yes | ItemData 新增 acquiredTime (DateTime) | 现有 ItemData.cs | 低 |
| Local State | Yes | 内存计时，30s 后自动清除 | — | 低 |
| Persistence | No | 本次不做持久化（已确认） | — | — |
| Config | No | N/A | — | — |
| Network | No | 本次不涉及服务器（已确认） | — | — |
| Resource | No | 文本方案不需要新资源 | — | — |
| Animation | No | N/A | — | — |
| Performance | No | 时间差判断 O(1)，无循环/协程开销 | — | 低 |
| Refresh | Yes | RefreshList 需检查 acquiredTime 更新显示 | 现有 RefreshList | 低 |
| Lifecycle | Yes | 切换页签/关闭背包后计时继续 | Time.time 判断 | 低 |
| Platform | No | N/A | — | — |
| QA | Yes | 手动验证：获得→NEW 出现→30s 消失→切换页签仍显示→关闭再打开仍显示 | Unity Play | 低 |
