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
v1.6  Stable Harness ✅ 当前版本
  │    Conflict Gate + 三段式 metrics + Regression suite
  │    已验证：Unity 新建/修复、Python 修复、冲突拦截
  │    待补：CONDITIONAL 多轮证据
  ↓
v1.7  Real-Use  ← 当前分支
  │    不追 CONDITIONAL，开始做真实任务。让它自然失败。
  ↓
v1.9  Sensor Automation（自动检查脚本）
  ↓
v2.0  Loop Engineering 稳定版（APPROVED/BLOCKED/CONDITIONAL 三种状态全验证）
  ↓
v2.2  Unity 专用规则
  ↓
v3.0  Multi-Agent（等前面稳了再说）
```

## 当前状态

| 维度 | 等级 |
|:---|:--:|
| SOP | ✅ 5/5 |
| SDD | ✅ 4.5/5 |
| Harness | ✅ 3.5/5 — 个人工程级稳定版 |
| Loop | ⚠️ 2.5/5 — 机制有，多轮证据不足 |
| Sensor | ⚠️ 3.0/5 — 人工为主 |
| 通用性 | ✅ 3.5/5 — Unity + Python |
| 玩具化风险 | 已明显下降 |

## 回归套件

| # | 用例 | 结果 |
|:--|:---|:--:|
| 01 | Unity 新建功能 | ✅ |
| 02 | Unity GC 修复 | ✅ |
| 03 | Python 修复 | ✅ |
| 04 | 冲突需求拦截 | ✅ BLOCKED |
| 05 | CONDITIONAL 回路 | ⚠️ 待补证据 |

## 进化原则

1. 只加固断裂点 — 约束 = 成本，不在没断的地方加墙
2. 每改必 commit — 引用复盘证据
3. 实验走 branch — 改崩了 `git revert`
4. 不追 CONDITIONAL — 等真实任务自然失败

## 仓库生态

```
hermes-harness                ← 管线本体（skill + metrics + 回归套件 + snippets）
  ├── BackpackDemo            ← Unity 验证场
  ├── obsidian-normalizer     ← Python 验证场
  ├── unity-verification-projects ← 10 个历史 Unity 项目（Private）
  ├── unity-learning-lab      ← 6 个学习实验（公开作品集）
  └── unity-code-review-agent ← C# 静态审查工具
```

## 仓库沿革

本仓库取代了先前两个空壳仓库（`unity-agent-pipeline-template` / `unity-client-dev-harness`），并吸收了 `learning-backup` 中的 snippets 和 Unity 项目。
