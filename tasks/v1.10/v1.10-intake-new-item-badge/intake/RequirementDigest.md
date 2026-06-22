# Requirement Digest

## Source
- Source document: user-provided requirement
- Date: 2026-06-22
- Owner: YIMO

## Feature Goal
背包物品增加"最近获得"标记（NEW badge）。玩家获得新物品后在背包中可见，30 秒后自动消失。

## Player-facing Behavior
1. 玩家获得新物品 → 背包中该物品显示 NEW 标记
2. NEW 标记持续 30 秒后自动消失
3. 切换背包页签 → 未超时的 NEW 仍显示
4. 关闭背包再打开 → 未超时的 NEW 仍显示（本次会话内）

## Core Rules
- 计时：30 秒客户端倒计时
- 作用域：本次游戏会话内
- 排序：不影响现有排序规则
- 持久化：不做（确认）
- 服务器：不涉及（确认）

## User Flow
```
玩家获得物品 → 打开背包 → 看到 NEW 标记 → 30s 后标记消失
             → 切换页签 → NEW 仍在（如未超时）
             → 关闭背包 → 再打开 → NEW 仍在（如未超时）
```

## State Flow
```
Item state: normal → has NEW (timer starts) → normal (timer expires)
```

## Data Flow
```
ItemData 增加: acquiredTime (DateTime) 或 remainingSeconds (float)
UI 层判断: now - acquiredTime < 30s → show NEW
```

## Out of Scope
- 服务器同步
- 跨会话持久化
- 动画 / 音效
- 排序变更
- 红点系统集成

## Assumptions
- [Assumption] "获得新物品"指物品加入背包的时刻（非拾取动画、非服务端推送确认）
- [Assumption] 每个物品独立计时（非全局唯一 NEW）
- [Assumption] 当前 BackpackDemo 的 ItemData 结构可以被修改
- [Assumption] 30 秒倒计时在 Update() 或协程中驱动

## Open Questions
- 多次获得同一物品（如叠堆）是否刷新计时？
- NEW 标记的视觉表现形式？（文本/图标/背景色？）
- 是否需要手动关闭 NEW 的能力？
