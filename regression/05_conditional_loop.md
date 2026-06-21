# Regression 05：CONDITIONAL 多轮回路由（待完成）

类型：回路压测
项目：obsidian-normalizer（或同等级复杂度）
验证能力：Loop 机制在真实条件下触发

## 任务摘要
设计一个修复任务，使 Agent 第一轮修不完全，触发 CONDITIONAL。
例如："新增需求导致旧能力回归"——让 Agent 加新功能但漏掉已有测试用例。

## 预期状态
- Round 1：pytest 失败或审查发现遗漏
- Reviewer 判 CONDITIONAL
- Hermes 重新 delegate_task
- Round 2：修复遗漏 + pytest 通过
- 审查 APPROVED
- metrics 记录 loop_count ≥ 1
- 保留 Round1/2 的独立报告

## 退化检查点
- 是否进入 CONDITIONAL（不能 APPROVED 糊弄）
- 是否保留每轮的证据
- 是否不伪造测试结果
- 是否不跳过回路

## 状态
⚠️ NOT YET RUN — Loop Maturity: 2.5/5
前一次尝试（frontmatter-merge）：Agent 一次通过，未触发 CONDITIONAL
下次任务：设计更难——Regression-Repair 模式
