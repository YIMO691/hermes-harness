# ⚠️ SUPERSEDED — 工作线系统全貌

> **本文档已被 `docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md` 取代。**
> 撰写日期：2026-06-22 | 基于 hermes-harness v1.6-stable
> 定稿日期：同日 v1.7-stable 发布后归档
> 保留原因：历史参考（v1.6 时期的全面分析）
> 如需当前架构信息，请查阅 `docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md`

---

## 目录

1. [概念定义](#1-概念定义)
2. [架构总览](#2-架构总览)
3. [完整流程（9 个 Phase + 3 个子 Gate）](#3-完整流程)
4. [Agent 分工与降级链](#4-agent-分工与降级链)
5. [Git 基础设施（双层用途）](#5-git-基础设施)
6. [Metrics 系统（Level 2）](#6-metrics-系统)
7. [回归套件](#7-回归套件)
8. [Skill 管理与沉淀机制](#8-skill-管理与沉淀机制)
9. [当前状态与成熟度](#9-当前状态与成熟度)
10. [GAP 与漏洞分析](#10-gap-与漏洞分析)
11. [优化建议](#11-优化建议)

---

## 1. 概念定义

### 工作线是什么

工作线 = **Agent 工程管线**。它不是一个"用 AI 写代码"的工具，而是一套规格驱动开发（SDD）的多 Agent 协作系统。它的核心价值是：

```
需求进入 → 规格分析 → 冲突检测 → Agent 编码 → 编译验证 → 审查 → 报告 → 复盘
                                    ↑                                              │
                                    └──────── 断裂点驱动 skill 进化 ←──────────────┘
```

### 三条线定位

| 线 | 本质 | 代理 | 存储 | 成熟度 |
|:---|:---|:---|:---|:--:|
| **工作线** | Agent 工程管线 | hermes-harness | GitHub + ~/.hermes/skills/ | v1.6-stable |
| **学习线** | 知识库 + 验证项目 | Obsidian + GitHub | Obsidian 489篇 + 4个仓库 | 持续维护 |
| **思考线** | 哲学社科研究 | think-tank/ | 本地 + Obsidian | v5 双论文完成 |

### 工作线的独特性

工作线与其他"AI 辅助编程"的本质区别：

| 普通 AI 编程 | 工作线 |
|:---|:---|
| 人提需求 → AI 直接写 → 人验证 | 人提需求 → SDD 规格 → 冲突检测 → **多 Agent 协作** → 四级报告 → 人验证 |
| 单一 Agent | 3 Agent 分工（调度/编码/审查） |
| 无约束 | 硬约束 GATE + 软约束违规标记 |
| 不进化 | 每次断裂 → patch skill → commit with evidence |
| 无度量 | 结构化 metrics.yaml → 趋势分析 |

---

## 2. 架构总览

### 2.1 仓库生态

```
hermes-harness/                    ← 管线本体
├── skills/                        ← 运行时 skill（workline-execution + et6-gm-testing）
│   └── workline-execution/
│       ├── SKILL.md               ← 核心：9 Phase + Pitfalls + Metrics 模板
│       └── references/            ← 10 份参考文档
├── regression/                    ← 5 个回归用例（4/5 验证）
├── retrospectives/                ← 7 份复盘 + 7 份 metrics.yaml
├── scripts/
│   └── check_workline_outputs.py  ← 报告完整性自动检查
├── snippets/                      ← 10 个可复用代码片段
├── docs/                          ← 本文档所在
├── AGENTS.md                      ← Agent 分工契约
├── WORKFLOW.md                    ← 管线设计文档（进化原则）
├── CONTRIBUTING.md                ← 贡献指南
└── README.md                      ← 版本路线图 + 状态矩阵

验证仓库：
├── BackpackDemo/                  ← Unity 验证场（背包筛选/排序/对象池）
├── obsidian-normalizer/           ← Python 验证场（36 个 pytest）
├── unity-verification-projects/   ← 10 个历史 Unity 项目（Private）
├── unity-learning-lab/            ← 6 个学习实验（公开）
└── unity-code-review-agent/       ← C# 静态审查工具
```

### 2.2 三层 Agent 协作架构

```
                      ┌─────────────────────┐
                      │     用  户           │
                      │  Mentor审阅 +        │
                      │  Unity Play 测试     │
                      └──────┬──────────────┘
                             │ 签字 / 截图
                             ▼
┌────────────────────────────────────────────────────────┐
│                    Hermes（调度层）                      │
│  - 需求理解 → 分析 → SDD 撰写                           │
│  - 冲突检测（Phase 3.5b）                               │
│  - 任务拆分 → 委托给下层                                │
│  - 编译验证                                              │
│  - 复盘 + metrics 产出                                   │
│  禁止：写 .cs 文件（编码阶段）                          │
└──────┬──────────────────────┬──────────────────────────┘
       │ delegate_task        │ delegate_task
       ▼                      ▼
┌──────────────┐     ┌──────────────────┐
│    Codex     │     │   Claude Code    │
│  （编码层）   │     │   （审查层）      │
│              │     │                  │
│ 写 .cs 文件   │     │ 代码审查：       │
│ 识图分析      │     │ - 模式一致性     │
│ 自修复        │     │ - 空安全         │
│              │     │ - IsCan+Do 完整  │
│ 禁止：       │     │ - Handler 覆盖   │
│ 架构决策      │     │                  │
└──────────────┘     └──────────────────┘
```

### 2.3 数据流

```
任务需求（用户输入 / 文档 / Bug 日志）
    │
    ▼
Phase 0  ──→ ENV_CHECK.md          ← 环境就绪检查
    │
Phase 1  ──→ [内存吸收]            ← 全文档读取
    │
Phase 2  ──→ PROJECT-ANALYSIS.md   ← 架构分析
    │
Phase 3  ──→ [设计文档]            ← 客户端 + 服务端设计
    │         ⚐ 用户审阅 Gate
Phase 3.5 ──→ SDD-需求拆分.md      ← 任务分解 + 非目标段
    │
Phase 3.5b──→ ConflictReport.md    ← 冲突检测（可能 BLOCKED）
    │
Phase 4  ──→ [Codex 写代码]        ← 委托编码（Hermes 不动手）
    │         git init + branch
Phase 5  ──→ dotnet build → 0 err  ← 编译修复循环
    │
Phase 6  ──→ HybridCLR 缓存清理    ← ET6 专有
    │         BuildCodeDebug
Phase 7  ──→ [Claude Code 审查]    ← 4 份结构化报告
    │         REVIEW / ChangedFiles / TestReport / RiskReport
    │         ⚐ 可能 CONDITIONAL → 回到 Phase 4
Phase 8  ──→ [用户 Unity Play]     ← 用户验证
    │
Phase 8b ──→ metrics.yaml          ← 结构化度量
    │         + Obsidian 复盘笔记
    │         + check_workline_outputs.py 验证
    ▼
复盘分析 → 断裂点 → patch skill → git commit
```

---

## 3. 完整流程

### Phase 0: GATE 0 — 环境就绪检查

**耗时**：~2 分钟 | **阻断性**：是

```yaml
工程可达:
  - 确认项目根目录绝对路径
  - cd + pwd 验证

编译工具:
  - dotnet --version（仅 ET6 项目）
  - 确认 .sln 文件存在

服务端:
  - 确认启动脚本（仅 ET6）
  - 确认端口（默认 20001）

GM 权限:
  - 确认 GM 账号可用（仅 ET6）

Agent 可用性:
  - codex --version
  - delegate_task 工具可用
  - claude --version 或 gh --version

项目状态:
  - git status 确认
  - .bak 文件存在 → git init 立即执行
```

输出：`tasks/doing/ENV_CHECK.md`，每项 ✅/❌。任一项 ❌ = 阻断。

### Phase 1: 全文档吸收

读取所有提供的文档——框架学习笔记、编码规范、UI 框架文档、参考模块需求文档、参考模块源码（Model/Hotfix/View 全层）。

**设计原则**：不在"知道一半"的状态下做决策。

### Phase 2: 分析

输出：`tasks/doing/PROJECT-ANALYSIS.md`

内容：
- 模块架构图（现有 + 待建）
- 参考模块模式提取
- 参考与目标模块差异
- 配置表依赖
- 协议定义需求

### Phase 3: 设计文档

按提供的参考文档格式，输出客户端设计文档 + 服务端设计文档。

**⚐ Mentor Gate**：用户审阅并批准设计文档后继续。

### Phase 3.5: SDD 需求拆分

输出：`tasks/doing/SDD-{项目}-需求拆分.md`

5 段结构：
1. **Code inventory** — 每个已有文件 ✅/❌
2. **Gap analysis** — 每层缺失内容
3. **Dependency-ordered tasks** — 从底向上排序
4. **Dependency graph** — ASCII 树
5. **Acceptance checklist** — 验证 Gate 复选框

关键约束：**Task 1 必须是最底层依赖**（Model 层数据定义）。

#### 非目标段（v1.4）

```markdown
## 非目标 / 本次不做
- 不重构无关模块
- 不修改未列入任务范围的系统
- 不顺手优化架构
- 不引入新的框架或依赖
- 不修改公共协议/公共接口/全局配置（除非 SDD 明确允许）
- 不处理与当前 Bug/需求无直接关系的问题
```

### Phase 3.5b: Conflict Gate — 冲突检测（v1.6）

**7 项检查**，在 delegate_task 之前运行：

```yaml
1. 功能目标之间是否冲突
2. 功能目标与非目标是否冲突
3. 验收标准与约束是否冲突
4. 持久化需求是否有合法存储位置
5. UI 交互需求是否有合法 UI 修改权限
6. 排序/筛选/状态需求是否允许修改对应逻辑
7. 输出文件要求是否与"不新增任何文件"冲突
```

任一冲突 → **BLOCKED**。输出 ConflictReport.md + ClarificationQuestions.md。Codex 不调用。等待 Mentor 回应。

**已验证**：背包收藏排序冲突测试 — 4 个致命冲突检测，Codex 零调用。

### Phase 4: 独立实现（委托编码）

**核心原则：Hermes 不写代码。Codex 写，Claude Code 审。**

#### Step 0: Git 初始化（强制）

```bash
git init && git add -A && git commit -m "initial: project baseline"
git checkout -b feature/<module-name>
```

#### 执行模型

```
Hermes 拆分 SDD 任务
  → delegate_task(tasks=[...]) 委托 Codex
    → Codex 写文件
    → Codex 返回摘要
  → Hermes 读文件，对照设计文档验证
  → git add -A && git commit
```

#### 关键防护

- **Pre-coding gate**：用 find/search_files 验证目标文件是否已存在
- **Model 逆推**：Hotfix 代码存在但 Model Component 缺失 → 用 subagent 逆推字段
- **文件计数 Gate**：对照设计文档文件清单计数，不假装完成

### Phase 5: 编译修复循环

```bash
dotnet build → 收集错误 → grep 参考源码查正确 API → patch → 重编译 → 直到 0 错误
```

常见 ET6 API 陷阱：
- `ConfigCategory.Instance.GetMould(id)` 不是 `GetXxxByXxxId(id)`
- `ConditionFactory.isCan(player, id)` 2 参数不是 3 参数
- `PlayerLoginInfo.XxxComponent` 包裹字段，不是直接属性
- `ErrorCode` enum 只有 ERR_SystemError 和 ERR_GoodsNotEnough

Unity 项目额外检查：`Packages/manifest.json` 是否有 `com.unity.ugui`。

### Phase 6: HybridCLR DLL 缓存修复（ET6 专有）

源文件变更不自动传播到 Unity Play：
```bash
rm -rf Unity/Library/ScriptAssemblies/
rm -f Unity/Assets/Bundles/Code/Code.dll.bytes
rm -f Unity/Assets/Bundles/Code/MonoHotUpdate.dll.bytes
# Unity Editor: Tools → Build → BuildCodeDebug
```

### Phase 7: 强制代码审查（Claude Code）

**不可跳过。即使 0 编译错误也要跑。**

#### 审查维度

| 维度 | 检查内容 |
|:---|:---|
| 模式一致性 | 是否遵循参考模块的 IsCan+Do、Handler 链、DlgSystem 模式 |
| 空安全 | GetComponent<T>() 是否检查了 null |
| IsCan+Do 完整性 | 每个 Do 是否有对应 IsCan |
| Handler 覆盖 | 每个网络 handler 是否有 try/catch + reply() |
| API 正确性 | 方法名/字段名是否匹配实际定义 |

#### 输出：4 份结构化报告

| 报告 | 内容 |
|:---|:---|
| REVIEW.md | 审查结论 + 问题表 + 越权检查 |
| ChangedFiles.md | 修改文件列表 + 关键修改说明 + 无关文件检查 |
| TestReport.md | 编译/启动/功能/日志/回归 5 项验证 |
| RiskReport.md | 风险等级 + 架构风险 + 运行时风险 |

#### 回路规则

| 判定 | 行动 |
|:---|:---|
| APPROVED | 进入 Phase 8 |
| NEEDS_FIX | 修复 → 重编译(Phase 5) → 重新审查(Phase 7)。最多 3 轮。 |
| REJECTED | 升级给用户。不继续。 |
| CONDITIONAL | 修复 → 重编译 → 重新审查。计入 loop_count。 |

### Phase 8: 验证

用户 Unity Play + 截图。Hermes 处理文件部署、编译和审查。

产出 Obsidian 复盘笔记，含「面试表达」和「可复用经验」。

### Phase 8b: 结构化 Metrics

产出 `retrospectives/<task-id>-metrics.yaml`：

```yaml
task: <任务名>
workline_version: <版本>
task_type: feature | fix | conflict_test | conditional_stress
phases:
  p0_gate: {passed: bool}
  p4_implementation: {delegated: bool, subagent_calls: int}
  p5_compile: {initial_errors: int, fix_loops: int}
  p7_review: {initial_verdict, reports_missing, rework_loops, bugs_found, final_verdict}
  p8_verify: {user_verified: bool}
violations:
  herm_write_code: int
  skip_review: int
  scope_creep: int
conditional_loop:
  triggered: bool
  loop_count: int
evidence:
  commit_hash: str
```

**报告完整性检查**：`python scripts/check_workline_outputs.py <task_dir>` 验证 4 份报告存在 + TestReport 内容非伪造 + metrics 三段完整。

---

## 4. Agent 分工与降级链

### 4.1 角色矩阵

| 角色 | 职责 | 禁止 |
|:---|:---|:---|
| **Hermes** | 调度、编译验证、GM 准备、分析/SDD/复盘 | 写 .cs 文件（编码阶段） |
| **Codex** | 写代码、识图 | 做架构决策 |
| **Claude Code** | 代码审查 | 写新代码 |
| **用户** | Mentor 审阅、Unity Play 测试 | 代替 Agent 写代码 |

### 4.2 降级链

```
优先: Codex 写代码 → Claude Code 审查
  ↓ Codex 不可用
降级: Claude Code 写代码 + 自查 → [FALLBACK]
  ↓ Claude 不可用
降级: Hermes 写代码 → [FALLBACK: herm-code]
```

降级一次 = 复盘标记一次。连续降级 = 升级为系统问题。

### 4.3 违规标记

| 标记 | 触发条件 | 严重度 |
|:---|:---|:--:|
| `[VIOLATION: herm-write-code]` | Hermes 写了 .cs | ⚠️ |
| `[VIOLATION: skip-review]` | 编译后没跑审查 | 🔴 |
| `[VIOLATION: skip-audit]` | 编码前没做代码审计 | ⚠️ |
| `[FALLBACK: herm-review]` | Claude 不可用 | 🟡 |
| `[FALLBACK: herm-code]` | Codex+Claude 都不可用 | 🟡 |

**不阻断，但标红。累计标红触发版本升级。**

---

## 5. Git 基础设施（双层用途）

### Layer 1: 工程产出
```
git diff  → Claude Code 审查对象（变更集，非全文件）
git log   → 追溯
git revert → 回退
git branch → 并行工作
```

### Layer 2: 管线进化
```
git tag   → 稳定版本标记（v1.2→v1.6 共 6 个里程碑）
git branch → 实验隔离（exp/* 分支）
git log skills/ → 管线演进史
```

### Commit 格式
```
patch: <skill> - <原因>
证据: 复盘/2026-06-21-ET6.md §二.P0
```

---

## 6. Metrics 系统（Level 2）

### 6.1 数据流

```
Phase 8b 产出 metrics.yaml
    ↓
check_workline_outputs.py 验证完整性
    ↓
攒够 3+ 份 → 横向对比分析
    ↓
产出 LEVEL_METRICS_REVIEW.md
    ↓
做出 GATE 调整决策
```

### 6.2 当前数据（4 份）

| 任务 | 类型 | 时长 | 编译错误 | 审查回路 | 违规 |
|:---|:---|:--:|:--:|:--:|:--:|
| ET6 v3 | feature | 35 min | 12 | 1 | 0 |
| BackpackDemo | feature | 45 min | 0 | 1 | 0 |
| obsidian-normalizer | fix | 25 min | 0 | 0 | 0 |
| GC fix | fix | 18 min | 0 | 0 | 0 |

### 6.3 趋势结论

- **任务时长** ↓ 加速中（skill 熟悉 + 模板成熟）
- **编译错误** → 0（v1.4.1 manifest 检查有效）
- **审查回路** → 0（末次首次审查即 APPROVED）
- **违规** 连续 4 任务 0（Agent 契约已内化）
- **审查发现 Bug** 首任务 4 个真 Bug → 后续 0（审查 GATE 必要）

### 6.4 GATE 调整决策

| GATE | 决定 | 理由 |
|:---|:---|:---|
| Phase 7 审查 | 保持不降级 | 首任务发现真 Bug，项目多样性不足时降级风险高 |
| Phase 4 编码委托 | 成熟，简化为 P2 pitfall | 4 任务 0 次 herm-write-code |
| Phase 0 GATE 0 | 加项目类型分支 | 不同项目类型需要不同检查项 |
| Phase 5 编译 | manifest 检查保持 | v1.4.1 后 2 个 Unity 任务 0 错误 |

---

## 7. 回归套件

| # | 用例 | 类型 | 项目 | 预期 | 状态 |
|:--|:---|:---|:---|:---|:--:|
| 01 | Unity 新建功能 | feature | BackpackDemo | APPROVED | ✅ |
| 02 | Unity GC 修复 | fix | BackpackDemo | APPROVED | ✅ |
| 03 | Python 修复 | fix | obsidian-normalizer | APPROVED | ✅ |
| 04 | 冲突需求拦截 | conflict_test | BackpackDemo | BLOCKED | ✅ |
| 05 | CONDITIONAL 回路 | conditional_stress | 待定 | 多轮→APPROVED | ⚠️ |

**每次 workline skill 升级后**跑一遍回归套件。任一退化 → 修复后再升。

---

## 8. Skill 管理与沉淀机制

### 8.1 Skill 生命周期

```
发现断裂点（复盘）
  → 归属到具体 skill
  → patch skill（skill_manage action='patch'）
  → git commit with evidence reference
  → 回归验证
```

### 8.2 当前 Skill 地图

```
~/.hermes/skills/
├── workline-execution/       ← 核心：9 Phase 流程 + Pitfalls + Metrics
│   └── references/           ← 10 份参考文档
├── subagent-driven-development/ ← 委托编码模式
├── codex/                    ← Codex CLI 调用模式
├── claude-code/              ← Claude Code 审查模式
├── et6-gm-testing/           ← ET6 GM 测试指南
├── agent-pipeline/           ← Agent 管线编排规则
├── agent-workline/           ← 工作线双入口（诊断/需求）
├── post-task-alignment/      ← 任务后对齐
└── ... (其他 30+ skills)
```

### 8.3 断裂点驱动的进化

| 版本 | 断裂点 | 加的约束 |
|:---|:---|:---|
| v1.3 | Hermes 越权写代码 | 编码阶段 Hermes 禁止写 .cs |
| v1.3 | Claude 审查被跳过 | 编译后强制审查 GATE |
| v1.3 | 代码审计缺失 | Phase 1.5 强制 find+读已有代码 |
| v1.3 | 依赖 skill 未加载 | Phase 0a 自动加载 |
| v1.3 | 环境未就绪就开干 | Phase 0 GATE 0 |
| v1.4 | SDD 无作用域边界 | 「非目标」段 |
| v1.4 | 审查只有结论无证据 | 4 份结构化报告 |
| v1.4 | Agent 可能越权改无关文件 | 无关文件修改检查 |
| v1.4 | 复盘无面试表达 | 面试表达模板 |
| v1.4.1 | Unity 缺 UGUI 包 | manifest 检查 |
| v1.5 | 无度量 | metrics.yaml 系统 |
| v1.6 | 冲突需求无拦截 | Conflict Gate |

---

## 9. 当前状态与成熟度

### 9.1 能力矩阵

| 维度 | 等级 | 说明 |
|:---|:--:|:---|
| SOP | 5/5 | Phase 0-8 完整流程 |
| SDD | 4.5/5 | 任务拆分 + 非目标 + 冲突检测 |
| Harness | 3.5/5 | 个人工程级稳定版 |
| Loop | 2.5/5 | 机制有，多轮证据不足（regression 05 待补） |
| Sensor | 3.0/5 | 人工为主，check_workline_outputs.py 自动检查 |
| 通用性 | 3.5/5 | Unity + Python 双验证 |
| 玩具化风险 | 已明显下降 | 从"概念演示"到"真实可用" |

### 9.2 已验证能力

```
✅ Unity 新建功能（BackpackDemo）
✅ Unity GC 修复
✅ Python 修复（obsidian-normalizer）
✅ 冲突需求拦截（Conflict Gate — BLOCKED）
✅ ET6 服务端编码（nerve + raffle 模块）
✅ 结构化报告（4 份/任务）
✅ 面试表达模板
⚠️ CONDITIONAL 多轮回路由（机制就绪，缺证据）
```

### 9.3 版本里程碑

```
v1.2-stable  Git + Agent 契约 + 代码审计
v1.3-stable  依赖加载 + GATE 0 + 审查模板 + 回路机制
v1.4-stable  SDD 非目标 + 4 份报告 + 越权检查 + 面试复盘
v1.4.1       Unity manifest 检查
v1.5-stable  Metrics 基础
v1.6-stable  Conflict Gate + 三段式 metrics + Regression suite ✅ 当前
v1.7         真实任务积累（进行中）
```

---

## 10. GAP 与漏洞分析

### 10.1 🔴 已修复的断裂点

| GAP | 证据 | 修复 |
|:---|:---|:---|
| Skill 依赖链断裂 | Hermes 不知道 delegate_task 怎么用 → 自己写代码 | Phase 0 自动加载依赖 skill |
| GATE 0 缺失 | 不知道工程在哪、dotnet 路径错、GM 按钮无响应 | Phase 0 准入检查 |
| Claude 审查无模板 | 审查被跳过，"不知道具体怎么做" | Phase 7 审查模板 + 4 份报告 |
| SDD 无作用域 | Agent "顺手优化"无关代码 | 「非目标」段 |

### 10.2 🟡 已知未修复的 GAP

| GAP | 描述 | 严重度 | 计划 |
|:---|:---|:--:|:---|
| Skill 目录同步 | hermes-harness/skills/ 和 ~/.hermes/skills/ 手动同步 | 🟡 | CONTRIBUTING.md 加了规则，但无自动机制 |
| CONDITIONAL 证据不足 | 机制有，但从未在真实任务中触发过 | 🟡 | 等真实任务自然失败（v1.7 策略） |
| 回归自动化 | 回归套件靠人工跑 | 🟡 | 未自动化 |
| Cron 维护 | 4 个 cron @23:00 维护知识库，但工作线本身无 cron | 🟢 | 工作线是手动触发，不需要 cron |

### 10.3 🟢 已知但不必补的

| 提议 | 不补的理由 |
|:---|:---|
| 任务分类器 | 目前只有一种任务类型 |
| 多 Agent 并行编码 | 上下文冲突，得不偿失 |
| 自动 git tag | 人工 tag 更准确，目前频率不高 |
| Webhook 触发 | 无外部事件源 |

### 10.4 ⚠️ 潜在漏洞（未断裂但值得关注）

| 漏洞 | 描述 | 触发条件 |
|:---|:---|:---|
| **单点故障** | 3 个 Agent 中任一个不可用 → 降级 → 质量下降 | 网络故障 / API 配额 / 服务宕机 |
| **Codex 幻觉** | Codex 写的代码可能"看起来对但逻辑错误" | 复杂业务逻辑 |
| **审查疲劳** | 多次 CONDITIONAL 回路后审查质量可能下降 | 连续 3+ 轮回路 |
| **上下文膨胀** | SDD + 源码 + 审查报告累积 → 上下文窗口不足 | 大项目（10+ 文件） |
| **Mentor 瓶颈** | 用户在 Gate 3 / Gate 7 签字，但用户可能不在线 | 异步工作时间 |
| **跨平台假设** | ET6 流程高度依赖 Windows + dotnet + Unity | 非 Windows / 非 Unity 项目 |
| **版本漂移** | ~/.hermes/skills/ 和 hermes-harness/skills/ 可能不同步 | 改了 harness 忘了 cp |

---

## 11. 优化建议

### 11.1 短期（本月可做）

#### A. 完成 CONDITIONAL 证据

**问题**：regression 05 未验证。回路机制存在但从未在真实任务中触发。

**方案**：
- 不做刻意触发（v1.7 策略：等自然任务失败）
- 或设计一个故意不完整的任务（如第 8 条需求漏写），让 Codex 第一轮修不完
- 建议使用 Unity 任务（Python 任务通常一次通过，参考 Pitfalls 中的教训）

#### B. Skill 同步自动化

**问题**：hermes-harness/skills/ 改了但 ~/.hermes/skills/ 没更新。

**方案**：
- 最小方案：`make sync` 或 `./scripts/sync_skills.sh` 一键同步
- 中等方案：git hook（commit 时自动 cp）
- 大步方案：symlink（但 Windows symlink 有权限坑）

#### C. 加一个「快速诊断入口」

**问题**：当前工作线需要从 Phase 0 完整跑。简单的"帮我看看这个 Bug"不需要全流程。

**方案**：在 agent-pipeline skill 中已有路由规则⑨（Bug Fix 直接 delegate Codex），但 workline-execution 没有对应的轻量模式。可以加一个 `workline-quick` 变体：
```
Bug/截图 → Codex 诊断 → Hermes 验证 → 单份报告
```

### 11.2 中期（下月可做）

#### D. 审查自动化

**问题**：Phase 7 Claude Code 审查靠 delegate_task，但 checklist 可以部分自动化。

**方案**：
- `check_workline_outputs.py` 已有报告完整性检查
- 可以扩展：自动检查 IsCan+Do 配对、try/catch 覆盖
- 但别过度自动化——"代码审查发现真 Bug"是审查 GATE 不降级的核心理由

#### E. 跨项目模板

**问题**：当前强烈绑定 ET6/Unity。Python 项目已验证可用，但缺乏模板。

**方案**：
- 加 `references/python-project-checklist.md`（类似 unity-fresh-project-checklist.md）
- GATE 0 已有项目类型分支，扩展即可

#### F. Cron 检查工作线健康度

**方案**：每周跑一次 `check_workline_outputs.py` 全量扫描，发现报告缺失或 metrics 不完整时报告。

### 11.3 长期（Level 3）

#### G. 自动沉淀

**问题**：复盘 pitfall → patch skill 目前是人工的。

**方案**（Level 3）：
- 设计 pitfall→skill 映射 schema
- stable string matching（skill 文本结构稳定化）
- 复盘时自动生成 patch 建议 → 人工 review → merge

#### H. 多项目并行

**问题**：当前工作线假设一次一个项目。但实际可能有多个并行任务。

**方案**：
- 每个项目独立 git branch
- 工作线状态文件（`tasks/doing/ACTIVE_TASK.md` 而非隐式上下文）
- 但暂不急——目前还没有并行需求

---

## 附录 A：关键文件索引

| 文件 | 路径 | 用途 |
|:---|:---|:---|
| 核心 Skill | `skills/workline-execution/SKILL.md` | 9 Phase 流程定义 |
| 管线设计 | `WORKFLOW.md` | 进化原则 + 断裂点表 |
| Agent 契约 | `AGENTS.md` | 角色 + 约束 + 降级链 |
| 版本路线 | `README.md` | v0.0→v3.0 路线图 |
| 回归套件 | `regression/README.md` | 5 个用例 |
| 报告检查 | `scripts/check_workline_outputs.py` | 完整性验证 |
| 指标分析 | `retrospectives/LEVEL1_METRICS_REVIEW.md` | Level 2 分析报告 |
| GAP 分析 | `retrospectives/工作线GAP分析.md` | 断裂点成因 |
| 路线图 | `retrospectives/Harness发展路线图.md` | Step 1→4 计划 |
| 架构文档 | `docs/工作线系统全貌.md` | **本文档** |

## 附录 B：常见问题与陷阱（Pitfalls 精选）

| 陷阱 | 教训 |
|:---|:---|
| Hermes 写代码 | 工作线崩塌。必须委托 Codex |
| 不检查已有代码 | 浪费数小时写 17 个已存在的文件 |
| 编译前审查 | 浪费审查时间在 API 名称错误上 |
| 跳过审查 | 🔴 违规。首任务审查发现 4 个真 Bug |
| .bak 文件 | 无 git 的红旗。立即 git init |
| Python 逼 CONDITIONAL | Codex 对 Python 修复太保守，用 Unity 任务 |
| 约束不能阻断输出文件 | "不新增文件"→ 不新增业务代码文件 |
| Server.sln 路径 | 在 ET6 根目录，不在 Server/ 子目录 |

---

> **审查邀请**：以上是工作线系统的完整摊开。请对照你的实际使用体验，检查：
> 1. 是否有遗漏的流程/组件？
> 2. GAP 分析是否准确？（特别是有没有你已经遇到但我没标记的断裂点）
> 3. 优化建议优先级是否合理？
> 4. 潜在漏洞中有没有你实际担心但未标记为紧急的？
