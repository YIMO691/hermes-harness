# Acceptance Criteria

## Functional
- [ ] 物品获得后，背包列表中该物品显示 NEW 标记
- [ ] NEW 标记在 30 秒后自动消失
- [ ] 切换 TypeDropdown 筛选后，未超时的 NEW 仍显示
- [ ] 关闭背包面板再打开，未超时的 NEW 仍显示
- [ ] 超过 30 秒后不再显示 NEW

## UI
- [ ] NEW 标记以文本形式追加到物品名称后（如 "铁剑 [NEW]"）
- [ ] 详情面板显示剩余秒数

## State
- [ ] 计时在背包关闭期间继续运行（不暂停）
- [ ] ItemData.IsNew 基于 DateTime.Now 实时计算

## Non-functional
- [ ] 不修改排序规则
- [ ] 不请求服务器
- [ ] 不做本地持久化
- [ ] 不新增 UI 控件
- [ ] 不影响现有筛选功能

## Regression
- [ ] TypeDropdown 筛选仍正常
- [ ] 筛选按钮仍正常
- [ ] 收藏功能仍正常（★ 与 NEW 共存时显示正确）
