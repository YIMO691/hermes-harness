# Office Onboarding Metrics v1.11

> 入职阶段衡量指标 | 手动记录，不接入自动化

## 设计原则

1. **衡量入职安全，而非工程交付**。原 workline metrics 衡量编译错误数、审查回路——入职阶段需要衡量的是"跑通环境的卡点数""确认规范的次数""重复问题的数量"。
2. **手动记录**。入职初期不需要自动化 dashboard。一张手动更新的 yaml 文件足够。
3. **低摩擦**。每条指标 10 秒能填完，否则不会填。

---

## 1. 环境类

| 指标 | 类型 | 含义 |
|:---|:---|:---|
| `environment_bootstrap_done` | boolean | 项目是否能正常启动并 Play |
| `environment_blocker_count` | number | 跑环境过程中的阻断问题数 |
| `environment_setup_days` | number | 从拿到代码到能 Play 的天数 |

**为什么需要**: 跑环境是入职第一关。如果环境都跑不起来，后面全是空谈。

---

## 2. 规范类

| 指标 | 类型 | 含义 |
|:---|:---|:---|
| `policy_confirmed` | boolean | 是否已确认公司对个人 AI 工具的态度 |
| `tool_boundary_confirmed` | boolean | 是否已确认个人工具使用边界 |
| `sensitive_data_block_count` | number | Sensitive Data Gate 触发次数 |
| `persistence_block_count` | number | Persistence Gate 拦截写入次数 |

**为什么需要**: 安全合规是 v1.11 的最高优先级。这些指标直接衡量"有没有越界"。

---

## 3. 理解类

| 指标 | 类型 | 含义 |
|:---|:---|:---|
| `module_understanding_notes_count` | number | 脱敏理解笔记数 |
| `repeat_question_count` | number | 向导师重复问同类问题的次数 |
| `mentor_question_count` | number | 向导师提问总次数 |

**为什么需要**: 重复问同类问题是"学习无效"的直接信号。如果第一周 repeat_question > 2，说明理解方法需要调整。

---

## 4. 任务类

| 指标 | 类型 | 含义 |
|:---|:---|:---|
| `requirement_intake_lite_count` | number | 用 office-lite Intake Lite 拆过的需求数 |
| `acceptance_criteria_written` | number | 写出明确验收标准的次数 |
| `first_task_completed` | boolean | 第一个任务是否完成 |
| `bug_repro_success_rate` | percent | Bug 复现成功率（自评） |

**为什么需要**: 入职第二周开始接任务。"能拆需求"和"能写验收标准"是开发者的基本能力。

---

## 5. 复盘类

| 指标 | 类型 | 含义 |
|:---|:---|:---|
| `daily_work_card_count` | number | Work Card 完成天数 |
| `daily_report_count` | number | 日报完成天数 |
| `retrospective_count` | number | 任务复盘次数 |
| `checklist_created_count` | number | 新创建的 checklist 数 |
| `sop_updated` | boolean | 是否更新过 SOP |

**为什么需要**: 不复盘等于没学习。这些指标衡量"是否真的在沉淀经验"。

---

## 重点观察指标

入职前三周，优先盯这三个：

1. **repeat_question_count** — 如果 > 2，说明学习方式有问题
2. **sensitive_data_block_count** — 如果 > 0，说明安全边界需要加固
3. **first_task_completed** — 第一周结束应该是 true

---

## 记录方式

在 Obsidian 工作 Vault 的 `00_安全边界/onboarding_metrics.yaml` 中手动维护：

```yaml
# Week 1 Metrics
date: YYYY-MM-DD
environment:
  environment_bootstrap_done: true
  environment_blocker_count: 0
  environment_setup_days: 0
compliance:
  policy_confirmed: false
  tool_boundary_confirmed: false
  sensitive_data_block_count: 0
  persistence_block_count: 0
understanding:
  module_understanding_notes_count: 0
  repeat_question_count: 0
  mentor_question_count: 0
task:
  requirement_intake_lite_count: 0
  acceptance_criteria_written: 0
  first_task_completed: false
  bug_repro_success_rate: 0
retrospective:
  daily_work_card_count: 0
  daily_report_count: 0
  retrospective_count: 0
  checklist_created_count: 0
  sop_updated: false
```

## 不与原 workline metrics 冲突

原 `retrospectives/<task-id>-metrics.yaml` 是工程级指标（编译错误/审查回路/违规量）。本文件是入职阶段指标。两者并存，互不替代。
