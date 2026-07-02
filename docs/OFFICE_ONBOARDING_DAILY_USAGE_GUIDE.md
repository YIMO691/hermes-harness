# Office Onboarding Daily Usage Guide

> v1.11 | 每天照着用的轻量指南

## 早上 5 分钟：Work Card

打开模板: `templates/office_onboarding/work_card.md`

写下：
- 今日目标（1-2 条）
- 需要问的问题
- 今日风险

**不要写太多。这是一张卡片，不是一篇论文。**

---

## 接到需求时 10 分钟：Requirement Intake Lite

收到任务描述后，打开模板: `templates/office_onboarding/requirement_intake_lite.md`

写清：
1. 需求一句话摘要
2. 歧义点（你没看懂的地方）
3. 影响面（客户端/服务端/配置/UI/资源/测试）
4. 验收标准（做完以后拿什么验证）
5. 需要确认的问题

**如果歧义点 > 3 个，先去问清楚再接。**

---

## 遇到 Bug 时：Bug Triage Lite

模板: `templates/office_onboarding/bug_triage_lite.md`

填满这五行再动手：
1. 现象是什么
2. 怎么复现
3. 期望结果是什么
4. 实际结果是什么
5. 可能原因（按概率排序）

**先排查，再修复。不要改完代码才发现根因错了。**

---

## 不敢问问题时：Mentor Question

模板: `templates/office_onboarding/mentor_question.md`

核心公式：
```
我现在在处理 [问题]
我已经确认了 [自己查的结果]
我目前卡在 [具体卡点]
我想确认 [具体问题]
```

**不要说"我不知道怎么做"。说"我试了 A 和 B，卡在 C，组里通常怎么处理 C？"**

---

## 下班前 5 分钟：日报 + 复盘

先写日报：模板 `templates/office_onboarding/daily_report.md`
- 今天完成了什么
- 卡在哪里
- 明天计划

再如果有任务完成：模板 `templates/office_onboarding/task_retrospective.md`
- 做了什么 → 怎么做的 → 遇到什么问题 → 学到了什么

**必须脱敏。日报是发给导师看的，复盘是给自己看的。两份都要通过敏感信息检查。**

---

## 每周末 15 分钟：周复盘

回顾本周：
- 环境跑通了吗？
- 规范确认了吗？
- 接了几个任务？完成几个？
- 有没有重复问同类问题？
- 有没有触发敏感信息拦截？
- 沉淀了哪些 checklist / SOP？

更新 `onboarding_metrics.yaml`。

---

## 安全 reminders（每天看一遍）

```
□ 今天有没有不小心输出了公司内部类名/路径/协议？
□ 今天存到 Obsidian 的内容有没有通过脱敏检查？
□ 今天发给 ChatGPT 的信息有没有包含公司内容？
□ 今天 Hermes 有没有越权操作？
□ 如果导师问"你用什么工具辅助学习的"，我能说清楚且不踩线吗？
```
