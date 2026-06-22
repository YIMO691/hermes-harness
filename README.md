# Hermes Harness

> Personal Agent Engineering Workline — SDD-driven, Harness-constrained, Loop-ready.

## 版本路线

```
v0.0  Prompt 玩具
  ↓
v1.0  SOP 流程
  ↓
v1.3  Workline 基础版（Agent 分工 + GATE + Review + CONDITIONAL 雏形）
  ↓
v1.5  结构化 Harness（SDD 非目标 + 4 份报告 + 越权检查 + Metrics 驱动）
  ↓
v1.6  Stable Harness（Conflict Gate + 三段式 metrics + Regression suite）
  ↓
v1.7  Core-Freeze ✅ 当前版本
  │    Mode Router (full/quick) + Conflict Gate enforcement + Lite reports
  │    Gate plugin spec + 7 placeholder gates (defined, not implemented)
  │    验证：3 个任务（1 regression + 1 real quick + 1 full feature）
  │    设计审查：思考线 v4 反方审判 → 砍半修正
  ↓
v1.9  Sensor Automation（自动检查脚本）
  ↓
v2.0  Loop Engineering 稳定版（APPROVED/BLOCKED/CONDITIONAL 全验证）
  ↓
v3.0  Multi-Agent（等前面稳了再说）
```

## v1.7 核心变更

```
From: 一个大而全的线性流程（Phase 0-8，所有任务走同一条路）
To:   2 模式路由 + 1 active Gate + 7 placeholder + Lite 报告
```

| 变更 | 说明 |
|:---|:---|
| Mode Router | full（新功能/多文件）+ quick（Bug 修复/单文件），Agent 内部判断 |
| Conflict Gate | 唯一 active hard gate，peer_agent 审查，BLOCKED 时 Codex 零调用 |
| Placeholder Gates | UI/Network/Config/Performance/Asset/Platform/Hotfix — 已定义，断裂后激活 |
| Lite 报告 | quick 模式：WorklineSummary.md + metrics-lite.yaml（不做 4 份完整报告） |
| 不拆分 skill 目录 | 保持单文件结构，600 行可管理 |
| 不引入 LangChain/LangGraph | 决策记录在 `references/langgraph-evaluation.md` |

## 当前状态

| 维度 | 等级 |
|:---|:--:|
| SOP | ✅ 5/5 |
| SDD | ✅ 5/5 |
| Harness | ✅ 4.0/5 — Mode Router + Gate 执行规则 |
| Loop | ⚠️ 2.5/5 — 机制有，多轮证据不足 |
| Sensor | ⚠️ 3.0/5 — `check_workline_outputs.py` |
| 通用性 | ✅ 4.0/5 — Unity + Python + quick/full 双模式 |

## 回归套件

| # | 用例 | 模式 | 结果 |
|:--|:---|:--:|:--:|
| 01 | Unity 新建功能 | full | ✅ |
| 02 | Unity GC 修复 | full | ✅ |
| 03 | Python 修复 | full | ✅ |
| 04 | 冲突需求拦截 | full | ✅ BLOCKED |
| 05 | CONDITIONAL 回路 | full | ⚠️ 待补证据 |
| 06 | Quick bugfix | quick | ✅ |

## v1.7 设计审查

v1.7 草案（5 模式 + 8 Gate + 6 目录重组）经思考线 v4 反方审判后砍半修正：

| 攻击者 | 发现 | 结果 |
|:---|:---|:---|
| 管线原则 | 5 项提案仅 1.5 项对应真实断裂点 | 砍到 2 模式 + 1 Gate |
| 开发者 | TaskSpec 增加入口负担 | 改为 Agent 内部判断 |
| 架构师 | 6 层抽象协调税 > 收益 | 保持单文件 |

审查记录：`think-tank/studies/2026-06-22_工作线v1.7-core-freeze审查-v4/`

## 进化原则

1. 只加固断裂点 — 约束 = 成本，不在没断的地方加墙
2. 每改必 commit — 引用复盘证据
3. 实验走 branch — 改崩了 `git revert`
4. 不追 CONDITIONAL — 等真实任务自然失败
5. 验证后打 tag — 不基于文档打稳定版

## 仓库生态

```
hermes-harness                    ← 管线本体（skill + metrics + 回归套件 + snippets）
  ├── BackpackDemo                ← Unity 验证场
  ├── obsidian-normalizer         ← Python 验证场
  ├── unity-verification-projects ← 10 个历史 Unity 项目（Private）
  ├── unity-learning-lab          ← 6 个学习实验（公开作品集）
  └── unity-code-review-agent     ← C# 静态审查工具
```

## 仓库沿革

本仓库取代了先前两个空壳仓库（`unity-agent-pipeline-template` / `unity-client-dev-harness`），吸收了 `learning-backup` 中的 snippets 和 Unity 项目。v1.7 是首个经思考线审查 + 三项验证后 tag 的版本。
