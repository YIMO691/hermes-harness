# Regression 10：Quick Auto-upgrade Bypass

类型：quick auto-upgrade check
验证能力：auto_upgrade.required=true 但仍 approved 时应 BLOCKED

## 任务摘要
quick 任务触发 auto-upgrade（触及 UI/协议/配置），但仍标记 result=approved。

## 预期状态
- mode: quick
- auto_upgrade.required=true, result=approved
- → BLOCKED
- exit code=2
