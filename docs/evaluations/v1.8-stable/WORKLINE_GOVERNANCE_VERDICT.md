# WORKLINE_GOVERNANCE_VERDICT

> 版本：v1.0
> 评估对象：hermes-harness v1.8-stable
> 日期：2026-06-22
> 输入：Hermes 工程自评 + 思考线独立审判
> 输出：治理裁决

---

## 0. Verdict Summary

```
当前版本:         v1.8-stable
当前真实等级:      Strong Personal Harness Prototype
Hermes 自评分:     64/100
Thinking Line 修正: 40/100
最终治理判定:       KEEP_STABLE_BUT_DO_NOT_UPGRADE_SCOPE
```

**解释**：

- v1.8-stable 作为最小 harness-check 里程碑**可以保留**
- 但**不能宣称为 Stable Personal Harness**
- 当前**不允许进入复杂架构扩展**
- 下一阶段**只能补最薄弱工程证据**：CI、regression、真实 Git workflow、真实任务样本

---

## 1. Acceptance of Thinking Line Judgment

Hermes 自评高估了系统成熟度。

### 高估原因

1. **把文档化计入工程化得分** — Git Workflow 文档被计为工程化能力，但从未执行
2. **把样例通过计入真实稳定** — 4 fixtures + 5 small tasks 被计为"证据充足"
3. **把 Git Workflow 文档当成 Git Workflow 执行** — 零 PR/merge/release 记录
4. **把 demo 验证当成 Unity 领域覆盖** — BackpackDemo（7 文件）被计为领域覆盖
5. **低估了 CI / trace / eval / observability 缺口** — Automation 4/10 实为 1/10

### 思考线修正

```
Hermes:           64/100
Thinking Line:    40/100
Delta:            -24
Overestimation:   ~37%
```

**本裁决完全接受思考线修正评分。**

---

## 2. Current True Level

```
Personal Harness Prototype
```

可补充表述：**Strong Personal Harness Prototype**。

### 不可使用的表述

- ~~Stable Personal Harness~~
- ~~Early Engineering Harness~~
- ~~Production-grade Harness~~

### 原因

| 已具备 | 仍缺失 |
|:---|:---|
| 流程骨架 | CI 自动触发 |
| full / quick Mode Router | 自动 regression |
| Conflict Gate | 真实 Git workflow 执行记录 |
| v1.8 checker | trace / observability |
| metrics schema | 真实 Unity 复杂项目验证 |
| 真实任务验证（5 个，小规模） | 跨任务 metrics 聚合 |

---

## 3. Why It Is Not Stable Personal Harness Yet

### 3.1 CI does not exist

当前 checker 可以手动运行（`python tools/check_workline_task.py`），但没有 GitHub Actions / CI 自动触发。手动可运行 ≠ 自动化。

**对应命题**：P4 Automation — Thinking Line 1/10

### 3.2 Git Workflow has not been executed

当前有完整的 Git Workflow 文档（`docs/WORKLINE_GIT_WORKFLOW.md`，13 章），但没有真实执行记录：feature branch、fix branch、PR/MR、release branch、hotfix branch、merge record。所有 commit 均在 master 单分支上。

**对应命题**：P6 Git Workflow — Thinking Line 3/10

### 3.3 Regression sample is too small

当前 regression 仅 6 个用例（1 个待补）。样本不足以建立统计信心。

**对应命题**：P5 Evidence Quality — Thinking Line 5/10

### 3.4 Unity validation scope is too narrow

当前验证集中在 BackpackDemo（7 个 .cs 文件）。未覆盖真实游戏客户端常见复杂度：大量 Prefab、AssetBundle/Addressables、UI 状态复杂度、网络同步、配置表、性能/GC、平台差异。

**对应命题**：P7 Unity Coverage — Thinking Line 2/10

### 3.5 Trace / observability is missing

当前没有 agent trace、token/cost、latency、failure waste、phase-level cost、cross-task metrics aggregation。无法判断系统升级是否降低成本、提高成功率或减少失败浪费。

---

## 4. Most Valuable Capabilities Preserved

### 4.1 full / quick Mode Router

将大任务和小任务分流，避免所有任务进入重流程。v1.7-stable 的核心收益。quick 比 full 快 ~5x。**保留。**

### 4.2 Conflict Gate

编码前阻断需求冲突，当前唯一 active hard gate。符合"只激活有证据的 Gate"原则。经 4+ 次验证，零误调用。**保留。**

### 4.3 v1.8 Harness Checker

将部分文档规则变成可执行检查，能检查 full/quick 产物，输出 PASS/WARNING/BLOCKED。是从文档型流程走向工程型 Harness 的第一步。**保留。**

### 4.4 metrics schema

full/quick 有统一 metrics 结构，为后续 regression、health report、token observability 提供基础。**保留。**

### 4.5 Anti-overengineering principle

已拒绝过早接 LangGraph/LangChain、一次性激活所有 Gate、拆分 skill 目录。这是当前系统最重要的自我保护机制。**保留并强化。**

---

## 5. Governance Decision

```
Decision: KEEP_STABLE_BUT_RECLASSIFY
```

**含义**：

1. 保留 v1.8-stable tag；
2. 将成熟度重新定义为 **Strong Personal Harness Prototype**；
3. **不允许继续扩展架构**；
4. **不允许**立即接 LangGraph / token 系统大实现 / Dashboard；
5. v1.9 **只能补最低分命题**（P4/P5/P6）；
6. 所有下一步必须**提升 A/B 级证据**，不能继续增加 C/D 级文档。

---

## 6. v1.9 Priority

v1.9 必须聚焦以下事项，不得扩展范围：

### 6.1 CI / GitHub Actions — 自动运行 checker

**目标命题**：P4 Automation（1/10 → 目标 4/10）

- 在 PR/push/手动触发时运行 `tools/check_workline_task.py`
- 让 checker 从"手动工具"变成"自动检查"

### 6.2 Regression 6 → 10+

**目标命题**：P5 Evidence Quality（5/10 → 目标 7/10）

- 扩大 regression 样本
- 增加非法 quick、缺报告、metrics 冲突、scope 越界等用例

### 6.3 真实 feature/fix branch workflow 演练

**目标命题**：P6 Git Workflow（3/10 → 目标 5/10）

至少执行一次：develop → feature/fix branch → PR/MR-like review → merge。用真实 Git 轨迹证明 Git Workflow 不只是文档。

### 6.4 更多真实 Unity 任务验证

**目标命题**：P5 Evidence Quality（提升多样性）

不只跑 BackpackDemo 小任务，选择更接近真实客户端复杂度的任务。不急着激活 Unity UI/Performance/Network Gate。

---

## 7. Do Not Do Yet

以下明确**现在不做**：

| 项目 | 原因 |
|:---|:---|
| LangGraph / LangChain | 当前瓶颈不是编排框架，是最低分命题（CI/Git/regression） |
| Token observability 大实现 | 缺少足够真实任务样本，没有 CI/regression 基础时数据解释力不足 |
| Dashboard | 数据源不足，会变成展示层先行 |
| UI / Network / Performance Gate | 目前都是 placeholder，必须等真实断裂点重复出现 |
| 完整游戏客户端生命周期 | 远超当前阶段，保持在 coverage map 层 |

---

## 8. Token / Cost Evaluation Status

```
Token Evaluation: NOT AVAILABLE
Reason: token observability not implemented yet
Future role: will become the third input of workline-evaluation skill
```

Token/cost 评判未来会成为工作线治理的第三输入：

```
Engineering Evaluation
+ Thinking Line Review
+ Token / Cost Evaluation
= Governance Verdict
```

当前不得编造 token 数据，不得声称 v1.8 更省 token。

---

## 9. Evidence Grade Policy

以后所有工程评估必须标注证据等级：

```
A = 已实现 + 多次验证（≥3 次，不同项目）
B = 已实现但验证有限（1-2 次，同一项目）
C = 仅文档化（有文档但未执行/未验证）
D = 只是计划（文档中提及但未实现）
E = 不成立或缺乏证据
```

### 治理规则

- A/B 级证据**可以**计入工程化得分
- C 级**只能**计入设计成熟度，**不能**计入工程化成熟度
- D/E 级**不能**计入已实现能力
- 任何 stable 判定**必须**明确 A/B/C/D/E 比例
- **不允许把文档化当成工程化**

### 当前 v1.8 证据分布（基于思考线 04_argument_map.md）

```
A 级: 12/33 = 36% — 已实现+已验证
B 级:  9/33 = 27% — 已实现但验证有限
C 级:  6/33 = 18% — 仅文档化 ← 不应计入工程化
D 级:  3/33 =  9% — 只是计划 ← 不应计入
E 级:  3/33 =  9% — 不成立 ← 不应计入
```

v1.9 目标：将 C/D/E 级证据占比从 36% 降至 20% 以下。

---

## 10. v1.9 Entry Criteria

只有满足以下**全部条件**，才允许进入 v1.9 实现：

1. ✅ 当前治理裁决文档已确认
2. v1.9 目标限制在 CI + regression + Git workflow execution + real task evidence
3. 不新增 Gate
4. 不接 LangGraph / LangChain
5. 不做 token observability 大实现
6. 每个 v1.9 子任务必须产生可执行证据（A/B 级）
7. v1.9 完成后必须再次交给思考线审判

---

## 11. Final Statement

```
v1.8-stable is valid as a minimal harness-check milestone,
but the overall workline must be reclassified from
Stable Personal Harness to Strong Personal Harness Prototype
until CI, regression expansion, real Git Workflow execution,
and broader real-task evidence are available.
```

---

## Appendix: Evidence Sources

| Source | Path |
|:---|:---|
| Hermes Engineering Evaluation | `docs/WORKLINE_FULL_ENGINEERING_EVALUATION.md` |
| Thinking Line Review | `think-tank/studies/2026-06-22_工作线v1.8工程评估审判-v4/` |
| Architecture Doc | `docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md` |
| Git Workflow Doc | `docs/WORKLINE_GIT_WORKFLOW.md` |
| v1.8 Checker Plan | `docs/V1.8_HARNESS_CHECK_MINIMAL_PLAN.md` |
| Unity Lifecycle Coverage | `docs/UNITY_CLIENT_LIFECYCLE_COVERAGE.md` |
| Workline Evaluation Skill Design | `D:\Google下载文件\WORKLINE_EVALUATION_SKILL_DESIGN.md` |
| Token Observability Plan | `D:\Google下载文件\hermes_token_observability_engineering.md` |
