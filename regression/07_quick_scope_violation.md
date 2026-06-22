# Regression 07：Quick Scope Violation

类型：quick scope check
验证能力：quick 任务修改无关文件时应 BLOCKED

## 任务摘要
quick 任务修改了 docs/ 文件（应只在 source 范围内）。

## 预期状态
- mode: quick
- scope.violations 非空
- result=approved 但存在 violations → BLOCKED

## 退化检查点
- checker 检测到 scope violation
- result=BLOCKED
- exit code=2
