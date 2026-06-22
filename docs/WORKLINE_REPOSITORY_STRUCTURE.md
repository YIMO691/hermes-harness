# WORKLINE_REPOSITORY_STRUCTURE

> 版本：v1.0
> 适用版本：v1.9-stable
> 目的：定义仓库结构规则，先治理、后迁移
> 原则：不移动文件，不空建 future 目录，不破坏 CI/checker/evidence 链

---

## 0. Summary

```
Current status:  usable but needs governance
Strategy:        rule first, migration later
Migration:       no large-scale move after v1.9-stable
```

当前仓库约 109 files、9 tags（v1.2-stable → v1.9-stable）。结构基本合理，但已到达需要规则化的临界点。docs/、tasks/、tests/、regression/、retrospectives/ 的边界需要明确定义，避免未来无序膨胀。

**当前阶段只定义规则，不迁移文件。**

---

## 1. Current Repository Structure

```
hermes-harness/
├── .github/workflows/       CI — 自动运行 checker
├── docs/                    架构 / 计划 / 评估 / 治理 / 证据 / 归档
├── skills/                  Hermes runtime skill（单文件 Core）
├── tools/                   可执行工程工具（checker）
├── tests/                   可执行测试夹具和 runner
├── regression/              回归场景定义（设计文档）
├── tasks/                   真实任务证据包
├── retrospectives/          复盘和 metrics 汇总
├── scripts/                 辅助脚本
└── snippets/                可复用代码片段
```

---

## 2. Directory Responsibility Rules

### 2.1 docs/

**放**：
- 架构文档（`WORKLINE_ARCHITECTURE_V1.7_STABLE.md`）
- 工程计划（`V1.8_HARNESS_CHECK_MINIMAL_PLAN.md`、`V1.9_CI_REGRESSION_EVIDENCE_PLAN.md`）
- 治理裁决（`evaluations/<version>/WORKLINE_GOVERNANCE_VERDICT.md`）
- 评估报告（`WORKLINE_FULL_ENGINEERING_EVALUATION.md`、`evaluations/<version>/V1.9_EVIDENCE_REPORT.md`）
- 领域覆盖地图（`UNITY_CLIENT_LIFECYCLE_COVERAGE.md`）
- 历史归档（`SUPERSEDED_*`）

**不放**：
- 单次任务产物（WorklineSummary.md、metrics-lite.yaml）
- 运行时 skill
- checker fixture
- 临时代码片段

### 2.2 skills/

**放**：
- Hermes runtime skill（`workline-execution/SKILL.md`）
- Skill references（`references/` 目录）
- Agent 行为规则

**不放**：
- 评估报告
- 任务证据
- release report
- token 数据
- CI 配置

**原则**：

```text
skills/ is runtime layer. Do not modify it for documentation cleanup.
```

### 2.3 tools/

**放**：
- 长期维护的工程工具（`check_workline_task.py`）
- checker
- validator
- report generator

**不放**：
- 一次性临时脚本
- 临时分析代码

### 2.4 scripts/

**放**：
- 辅助脚本（`check_workline_outputs.py`）
- 一次性检查脚本
- 非核心工具

**规则**：如果脚本被 CI 依赖或长期维护，应考虑升级到 `tools/`。

### 2.5 tests/

**放**：
- 可执行测试夹具（`harness_check/` 下的各个 case）
- runner（`run_harness_check_cases.py`）
- golden report（`HarnessCheckReport.md`）

```text
tests/ = machine-executable verification
```

### 2.6 regression/

**放**：
- 回归场景定义（`01_*` 到 `10_*`）
- 测试意图、输入/预期/风险说明

**不放**：
- 实际 fixture 文件（在 `tests/`）
- 自动生成报告
- 真实任务产物

```text
regression/ = test specification (design)
tests/      = test execution (runner + fixtures)
```

### 2.7 tasks/

**放**：
- 真实任务证据包
- WorklineSummary.md
- metrics-lite.yaml / metrics.yaml
- HarnessCheckReport.md
- PullRequest.md（Git workflow 演练）
- TaskSpec / SDD / REVIEW / ChangedFiles / TestReport / RiskReport / retrospective

**建议未来按版本组织**：

```text
tasks/v1.8/
tasks/v1.9/
tasks/v1.10/
```

**当前不迁移** — 仅 v1.8 任务存在，后续新增按版本归档。

### 2.8 retrospectives/

**放**：
- 任务复盘（`2026-06-21-ET6.md`、`2026-06-21-BackpackDemo.md`）
- release 复盘（`2026-06-22-v1.7-stable-retro.md`）
- metrics 汇总（`*metrics.yaml`）
- 阶段路线回顾（`Harness发展路线图.md`、`LEVEL1_METRICS_REVIEW.md`、`工作线GAP分析.md`）

**建议未来可拆**：

```text
retrospectives/releases/
retrospectives/tasks/
retrospectives/metrics/
```

**当前不迁移**。

---

## 3. Future Target Structure

以下为未来目标结构。**不是立即迁移计划。** 仅在 v2.x 真实需求出现时才逐步调整。

```
docs/
├── architecture/           ← 架构文档
├── plans/                  ← 版本计划
├── evaluations/            ← 评估 + 治理裁决 + 证据报告
├── archive/                ← 历史归档
└── templates/              ← 报告模板

tasks/
├── v1.8/
├── v1.9/
└── v1.10/

retrospectives/
├── releases/
├── tasks/
└── metrics/
```

### Future-only 目录

以下目录在目标结构中定义，但**当前不得创建**：

| 目录 | 创建条件 |
|:---|:---|
| `observability/` | token observability 最小实现启动时 |
| `skills/workline-evaluation/` | evaluation skill 进入实现阶段时 |
| `skills/workline-observability/` | observability skill 被正式批准时 |

**原则**：空目录 = C 级证据（仅文档化）。禁止为了"看起来完整"而空建 future 目录。

---

## 4. File Placement Rules

新增文件按以下规则放置：

| 文件类型 | 位置 |
|:---|:---|
| 架构文档 | `docs/` |
| 版本计划 | `docs/` |
| 治理裁决 | `docs/evaluations/<version>/` |
| 证据报告 | `docs/evaluations/<version>/` |
| 真实任务证据 | `tasks/<version>/<task-id>/` |
| 可执行 checker | `tools/` |
| 可执行测试夹具 | `tests/` |
| 回归场景定义 | `regression/` |
| Skill 运行时规则 | `skills/<skill-name>/` |
| Release 复盘 | `retrospectives/` |
| 临时实验 | exp branch，不进入 main docs |

---

## 5. Stable Release Evidence Rules

每个 stable release 必须至少有：

1. ✅ tag
2. ✅ evidence report（`docs/evaluations/<version>/V*_EVIDENCE_REPORT.md`）
3. ✅ checker / CI result（10/10 或 runner 输出）
4. ✅ governance verdict（或 release note）
5. ✅ git status clean
6. ✅ scope statement（明确做了什么、不做什么）
7. ✅ explicit non-goals

**重要**：

```text
Stable tag must point to a commit that already contains its evidence report.
Do not tag first and write evidence later.
```

---

## 6. Task Evidence Package Rules

### quick 任务

```
tasks/<version>/<task-id>/
├── WorklineSummary.md
├── metrics-lite.yaml
└── HarnessCheckReport.md
```

Git workflow 演练额外包含：

```
└── PullRequest.md
```

### full 任务

```
tasks/<version>/<task-id>/
├── TaskSpec.md
├── SDD.md
├── ConflictReport.md
├── REVIEW.md
├── ChangedFiles.md
├── TestReport.md
├── RiskReport.md
├── metrics.yaml
├── retrospective.md
└── HarnessCheckReport.md
```

---

## 7. Evidence Grade Policy

```
A = 已实现 + 多次验证（≥3 次，不同项目/场景）
B = 已实现但验证有限（1-2 次，同一项目/场景）
C = 仅文档化（有文档但未执行/未验证）
D = 只是计划（文档中提及但未实现）
E = 不成立或缺乏证据
```

### 治理规则

- A/B 级**可**计入工程化成熟度
- C 级**只能**计入设计成熟度，**不得**计入工程化成熟度
- D/E 级**不得**计入已实现能力
- 任何 stable 判定**必须**说明 A/B/C/D/E 比例
- **严禁**把文档化当成工程化

---

## 8. Migration Policy

当前不迁移。

### 允许迁移的条件

- 某个目录职责已明显混乱（如 docs/ 混杂 10+ 种类型）
- CI / checker 路径已更新且验证通过
- old path 有迁移说明（commit message 或 migration doc）
- 迁移在专门 migration branch 执行
- 迁移后 CI 通过
- 迁移后更新 release index / repository structure doc

### 禁止

- 为了好看移动文件
- v1.9 刚稳定后立即大搬迁
- 一次性移动 docs / tasks / retrospectives 全部内容
- 破坏历史证据路径

---

## 9. Cleanup Policy

### Safe cleanup（随时可做）

- 增加 README（`docs/README.md`、`tasks/README.md` 等）
- 标记 `SUPERSEDED_` 前缀
- 添加 archive 说明

### Controlled cleanup（需 migration branch）

- 移动历史文档到 `docs/archive/`
- 归档旧任务到 `tasks/v1.x/`
- 拆分 `retrospectives/`

### Forbidden cleanup（禁止）

- 改 `skills/`
- 改 checker 核心规则
- 改 CI 路径但不验证
- 删除证据文件
- 移动 stable 证据报告

---

## 10. Current Recommendation

```
Do Now:
  ✅ Add repository structure governance doc (this file)
  ✅ Keep existing files in place
  ✅ Use rules for all future additions

Do Later:
  ○ Add docs/README.md
  ○ Add tasks/README.md
  ○ Add retrospectives/README.md
  ○ Consider versioned tasks layout

Do Not Do Yet:
  ✗ Large migration
  ✗ Empty observability/
  ✗ workline-evaluation skill creation
  ✗ workline-observability skill creation
  ✗ Dashboard / platform structure
```

---

## 11. Final Statement

```
The repository is usable and increasingly engineered,
but it has reached the point where structure governance is required.
The correct next step is not migration, but rule definition.

Future directories such as observability/ and workline-evaluation/
are valid target concepts, but they must remain future-only
until backed by implementation evidence.

Do not confuse "documented" with "implemented."
Do not create empty directories to make the structure look complete.
Do not move files just to make the repository prettier.
```
