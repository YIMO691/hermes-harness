# Hermes Harness

> 个人 Agent 工程管线 — SDD 驱动、审查把关、证据追踪。

## 概述

Hermes Harness 是一个个人 AI Agent 工程管线。它把需求、Bug、代码修改、审查、验证、复盘组织成**可追踪、可验证、可演进**的工程流程。

它不是"用 AI 写代码"的工具，而是一套约束 AI 辅助开发的管线：

- **模式路由** — 功能开发走 full，Bug 修复走 quick
- **冲突检测** — 在编码前阻断矛盾需求
- **Agent 分工** — Hermes 调度、Codex 编码、Claude Code 审查
- **结构化证据** — 每个任务留下 git commit、报告、metrics、复盘
- **Git 工作流** — 分支规范、PR 模板、发布打 tag、回滚规则

## 当前状态

| 项目 | 状态 |
|:---|:---|
| 稳定版本 | **v1.8-stable** |
| 核心模式 | full / quick |
| Active Gate | Conflict Gate |
| Harness Checker | `tools/check_workline_task.py` — 自动检查 full/quick 合规 |
| Skill 结构 | 单文件 Workline Core |
| Git 工作流 | Workline Git Workflow v1 |
| LangGraph / LangChain | 未引入 |
| 回归套件 | 10 个用例（9 验证，1 待补） |

**证据**：v1.7-stable 三项验证通过。v1.8-stable 新增 checker + fixture（4/4） + 真实 quick/full 验证。

## 解决什么问题

> AI 能生成代码，但没有范围约束、审查、验证和证据，结果不稳定。

工作线补齐了：

- 任务范围控制（SDD + 非目标声明）
- full / quick 模式分流
- 编码前冲突检测
- 多 Agent 质量门
- 编译和审查验证
- metrics 和复盘记录
- Git 证据链和回滚流程

## 架构

```
需求 / Bug
  → Mode Router（full / quick）
    → Conflict Gate（仅 full）
      → Agent 执行（Hermes / Codex / Claude Code）
        → Build / Review / Verify
          → Metrics / Retro
            → Git Evidence
```

单文件 Core。Full/Quick 双入口。一个 active gate。Full/Lite 双套报告。Git 工作流负责分支规范和发布管理。

→ 详情：[`docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md`](docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md)

## 模式

### full

**适用**：新功能、多文件修改、涉及 UI + 数据状态。

**流程**：环境检查 → 上下文审计 → SDD → Conflict Gate → Codex 编码 → 编译/测试 → Claude 审查 → 用户验证 → Metrics/复盘

**产出**：TaskSpec、SDD、ConflictReport、REVIEW、ChangedFiles、TestReport、RiskReport、metrics、retrospective（9 份）

### quick

**适用**：小 Bug、单文件修改、无架构决策。

**流程**：环境检查 → 最小审计 → Codex 修复 → 编译/测试 → WorklineSummary + metrics-lite

**产出**：WorklineSummary.md、metrics-lite.yaml（2 份）

**自动升级**：修复触及 UI 结构、协议、配置、资源、平台、热更 → 自动升级为 full。

## Git 工作流

```
main                    ← 生产就绪，只接受 release/hotfix merge
  └── develop           ← 日常集成，所有 feature/fix/docs 合入这里
      ├── feature/<id>  ← full 模式
      ├── fix/<id>      ← quick 模式
      └── docs/<topic>  ← 文档
```

- full → `feature/<id>` → squash merge 到 develop
- quick → `fix/<id>` → squash merge 到 develop
- Release：`develop` → `release/<ver>` → `main` + tag → 回合 develop
- Hotfix：`main` → `hotfix/<id>` → `main` + tag → 回合 develop

→ 详情：[`docs/WORKLINE_GIT_WORKFLOW.md`](docs/WORKLINE_GIT_WORKFLOW.md)

## 仓库结构

```
hermes-harness/
├── docs/
│   ├── WORKLINE_ARCHITECTURE_V1.7_STABLE.md       ← 架构定义
│   ├── WORKLINE_GIT_WORKFLOW.md                   ← Git 工作流
│   └── V1.8_HARNESS_CHECK_MINIMAL_PLAN.md         ← v1.8 checker 方案
├── tools/
│   └── check_workline_task.py                     ← v1.8 harness checker
├── tests/harness_check/                           ← checker fixtures
├── skills/workline-execution/
│   └── SKILL.md                               ← 运行时 skill（v1.7.0）
├── regression/
│   ├── README.md                              ← 6 个回归用例索引
│   └── 06_quick_bugfix.md
├── scripts/
│   └── check_workline_outputs.py              ← 报告完整性检查
├── retrospectives/                            ← 任务复盘 + metrics
└── snippets/                                  ← 可复用代码片段
```

## 验证

任务完成的标准不是"代码写完了"，而是**有证据**。标准证据链：

```
git diff → 编译结果 → 审查报告 → 用户验证 → metrics → commit hash
```

**打 stable tag 要求**：回归通过 + 一个真实 quick + 一个真实 full + 架构文档更新 + git status clean。

## 文档索引

| 文档 | 用途 |
|:---|:---|
| `docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md` | 稳定架构定义（12 章） |
| `docs/WORKLINE_GIT_WORKFLOW.md` | Git 工作流——分支模型、PR 模板、Release/Hotfix |
| `docs/V1.8_HARNESS_CHECK_MINIMAL_PLAN.md` | v1.8 checker 方案——检查规则、阻断逻辑 |
| `docs/UNITY_CLIENT_LIFECYCLE_COVERAGE.md` | 游戏客户端生命周期覆盖地图 |
| `regression/README.md` | 回归套件索引（6 个用例） |
| `skills/workline-execution/SKILL.md` | 运行时 skill——完整管线定义 |
| `tools/check_workline_task.py` | v1.8 harness checker |

## 路线图

**当前阶段**：v1.8 稳定使用期。不出现真实断裂点，不启动 v1.9。

v1.9 触发条件（至少一个成立）：
- quick 被滥用（bug 率上升）
- full 过重（连续 3+ 任务超 30 分钟）
- Conflict Gate 漏掉真实冲突
- 某类 Unity 问题重复出现 2 次以上
- metrics 显示风险指标持续上升

**不能触发 v1.9 的情况**：觉得架构不够漂亮、想提前实现全部 Gate、想接 LangGraph 证明标准化、想拆目录让结构更像工程。

## 不做的事

当前项目**不是**：
- 完整游戏客户端研发平台
- CI/CD 系统
- 多人团队管理工具
- LangChain / LangGraph 运行时
- Unity 手动验证的替代品
- 人工代码审查的替代品

当前聚焦：**让 AI 辅助的工程任务范围可控、可审查、可验证、可演进**。

---

*最后更新：2026-06-22 · v1.8-stable*
