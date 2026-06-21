# Hermes Harness

> Hermes Agent 工作线进化仓库。管线本身的代码，比管线生产的代码更重要。

## 是什么

这不是一个项目。这是**生产项目的生产线**。

```
hermes-harness/
├── skills/           ← 管线 Skill（每次任务加载，约束 Agent 行为）
├── retrospectives/   ← 每次任务复盘（断裂点 → Skill 改进）
└── tags/             ← 稳定版本标记（哪个版本通过了什么验证）
```

## 怎么工作

```
┌─────────────────────────────────────────────┐
│  每次任务                                    │
│  1. 加载 skill/ 中的约束                     │
│  2. 按 workline 阶段执行                     │
│  3. 任务完成后 → 复盘 → retrospectives/      │
│  4. 复盘发现断裂 → patch skill               │
│  5. git commit → git tag 稳定版本            │
│                                              │
│  下次任务 → 加载更新后的 skill → 更强的约束   │
└─────────────────────────────────────────────┘
```

## 版本历史

| 版本 | 状态 | 验证任务 | 核心改进 |
|:---|:--:|:---|:---|
| v1.6 | stable | 背包收藏冲突 + frontmatter baseline | Conflict Gate + 三段式 metrics + 回归套件 |
| v1.5 | stable | GC修复 + obsidian-norm (3 tasks) | metrics.yaml + Level 2 指标分析 |
| v1.4 | stable | 背包筛选 UI（全部通过 ✅） | SDD 非目标 + 4 份结构化报告 + 越权检查 |
| v1.3 | stable | ET6 新鲜副本（发现 4 Bug ✅） | 依赖自动加载 + GATE 0 准入 + 回路机制 |
| v1.2 | stable | ET6 测试题（27/27 ✅） | Git 集成 + Agent 契约 + 代码审计 + 审查 GATE |

## 回归套件

| # | 用例 | 结果 | Loop |
|:--|:---|:--:|:--:|
| 01 | Unity 新建功能 | ✅ | — |
| 02 | Unity GC 修复 | ✅ | — |
| 03 | Python 修复 | ✅ | — |
| 04 | 冲突需求拦截 | ✅ BLOCKED | — |
| 05 | CONDITIONAL 回路压测 | ⚠️ 2次未触发 | Agent 对 Python 太强 |

## 当前能力矩阵

| 能力 | v1.2 | v1.3 | v1.4 | v1.5 | v1.6 |
|:---|:--:|:--:|:--:|:--:|:--:|
| Agent 分工 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 审查 GATE | ✅ | ✅ | ✅ | ✅ | ✅ |
| 回路机制 | — | ✅ | ✅ | ✅ | ✅ |
| Git 集成 | ✅ | ✅ | ✅ | ✅ | ✅ |
| 代码审计 | ✅ | ✅ | ✅ | ✅ | ✅ |
| SDD 非目标 | — | — | ✅ | ✅ | ✅ |
| 4 份结构化报告 | — | — | ✅ | ✅ | ✅ |
| 越权检查 | — | — | ✅ | ✅ | ✅ |
| Metrics 驱动 | — | — | — | ✅ | ✅ |
| Conflict Gate | — | — | — | — | ✅ |
| 三段式 metrics | — | — | — | — | ✅ |
| 回归套件 | — | — | — | — | ✅ |

## 8 份 metrics

```
ET6-v3          → CONDITIONAL→APPROVED, 4 bugs found
BackpackDemo    → COMPILE→FIX→APPROVED
GC-fix          → APPROVED, 0 scope creep
obsidian-norm   → APPROVED, 21 tests, 0 deps
conflict-test   → BLOCKED, 4 fatal conflicts
frontmatter-bl  → baseline_pass (36/36)
field-order     → baseline_pass (42/42)
```

## 两条 Git 铁律

1. **Skill 修改必 commit**，commit message 引用复盘证据
2. **实验走 branch**，验证后 merge → tag，改崩了 `git revert`
