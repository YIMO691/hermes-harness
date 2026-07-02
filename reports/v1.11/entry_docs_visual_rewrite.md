# Entry Docs Visual Rewrite

> 日期：2026-07-02 | v1.11-office-onboarding-stable

## 1. 修改文件

| 文件 | 操作 | 变化 |
|:---|:---:|:---|
| `README.md` | 重写 | -27 lines — 增加 System/Mode/Version/Daily 4 张 Mermaid 图 |
| `CONTRIBUTING.md` | 重写 | -26 lines — 增加 Change Flow 图，规则精炼 |
| `SECURITY.md` | 重写 | -22 lines — 增加 Data Flow Boundary 图，安全模型清晰 |
| `docs/INDEX.md` | 优化 | -42 lines — 去重精简，关键入口突出 |
| **合计** | **4 files** | **-276 / +159 = net -117 lines** |

## 2. README 新结构

```
Current Stable Version → What This Is
→ System Overview (Mermaid)
→ Version Architecture (Mermaid)
→ Modes (table)
→ Gates (table)
→ Daily Usage Flow (Mermaid)
→ Start Here (key docs)
→ Safety Notice
→ Repository Status
```

## 3. 新增 Mermaid 图清单

| 文件 | 图 | 数量 |
|:---|:---|:---:|
| README | System Overview / Version Architecture / Daily Usage Flow | 3 |
| CONTRIBUTING | Change Flow | 1 |
| SECURITY | Data Flow Boundary | 1 |
| **合计** | | **5** |

## 4. CONTRIBUTING 新规则

- Contribution Principles（3 条基线保护）
- Change Flow（可视化演进流程）
- Skill Sync Rule（GAP #4 教训）
- Office Mode Rule
- MANUAL_VERIFY Rule
- Release Rule（6 条件检查表）
- Prohibited Actions

## 5. SECURITY 新安全模型

- Default Rule: UNKNOWN → safe-note
- Data Flow Boundary（公司→用户→Hermes→笔记→外部审查，公司→外部的禁止边）
- Tool Boundaries（Hermes / Codex / ChatGPT 三层 allow/deny 表）
- Forbidden Data（11 项清单）

## 6. LICENSE / SKILL

| 文件 | 状态 |
|:---|:---:|
| LICENSE | 未修改 ✅ |
| SKILL.md | 未修改 ✅ |

## 7. 敏感信息

- git diff 扫描：0 matches ✅

## 8. git status

```
4 files modified (README + CONTRIBUTING + SECURITY + INDEX)
clean working tree after commit
```

## 9. 建议

✅ 建议 push。README 现在是系统首页而非版本流水账。
