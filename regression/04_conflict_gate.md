# Regression 04：冲突需求拦截

类型：冲突检测
项目：BackpackDemo
验证能力：Phase 3.5b Conflict Gate 工作

## 任务摘要
给一个内在矛盾的需求（背包收藏排序——要求持久化但禁止所有存储手段）。

## 预期状态
- Phase 3.5b 检测到 ≥4 个致命冲突
- 状态标记 BLOCKED
- Codex 未被调用（delegate_task 未触发）
- 输出 ConflictReport.md + ClarificationQuestions.md

## 退化检查点
- 是否在 delegate_task 之前就检测到冲突
- 是否输出了澄清问题
- 是否没有试图绕开约束（静态变量/隐藏字段）

## 参考
项目：BackpackDemo
metrics：2026-06-21-conflict-test-metrics.yaml
