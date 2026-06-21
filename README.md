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

## 当前版本

| 版本 | 状态 | 验证任务 | 核心改进 |
|:---|:--:|:---|:---|
| v1.2 | stable | ET6 测试题（27/27 ✅） | Git 集成 + 硬约束 + 审查GATE + GM测试 |

## 管线状态

workline-execution v1.2.0 已包含：
- Agent 分工（Hermes 调度 / Codex 编码 / Claude 审查）
- Git 强制集成（编码前 git init + feature branch）
- 代码审计（Phase 1.5 — 防写冗余文件）
- 强制审查 GATE（编译后必须 Claude Code review）
- GM 测试完整指南（面板矩阵 + 物品ID + 测试组合）

## 两条 Git 铁律

1. **Skill 修改必 commit**，commit message 引用复盘证据
2. **实验走 branch**，验证后 merge → tag，改崩了 `git revert`
