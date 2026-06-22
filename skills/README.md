# skills/

Hermes 运行时 Skill 目录。

## 放什么

- Hermes runtime skill（`workline-execution/SKILL.md`）
- Skill references（`references/`）
- Agent 行为规则

## 不放什么

- 评估报告 → 放 `docs/evaluations/`
- 任务证据 → 放 `tasks/`
- token 数据
- CI 配置

## 当前 Skills

| Skill | 用途 |
|:---|:---|
| `workline-execution/` | 核心 — full/quick 模式、Conflict Gate、Pipeline |
| `et6-gm-testing/` | ET6 GM 测试指南 |

## 规则

- skills/ 是 **runtime 层** — 不要为了文档整理修改 SKILL.md
- 新增 skill 前必须先开 placement decision
- future skill（如 workline-evaluation、workline-observability）只在实现启动后创建
- 空建 future skill 目录 = C 级证据，不得计入工程化
