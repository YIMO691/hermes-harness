# Regression 09：Full Missing Multiple Required Reports

类型：full completeness check
验证能力：full 缺多个 required reports 时应 BLOCKED

## 任务摘要
full 任务缺 SDD + REVIEW + metrics.yaml（3 个 required）。

## 预期状态
- mode: full
- 缺 SDD.md, REVIEW.md, metrics.yaml
- → BLOCKED
- exit code=2
