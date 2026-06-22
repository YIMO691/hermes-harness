# Regression 08：Full Metrics Conflict — Build Failed

类型：full consistency check
验证能力：result=approved 但 build.passed=false 时应 BLOCKED

## 任务摘要
full 任务 metrics 声称 approved，但 build.passed=false。

## 预期状态
- mode: full
- result=approved, build.passed=false
- → BLOCKED
- exit code=2
