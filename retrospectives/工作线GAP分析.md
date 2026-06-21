# 工作线 GAP 分析

> 基于 ET6 实战，对照 Harness Level 1 标准逐项检查。
> 原则：只补「有证据的断裂点」，不补「想象的风险」。

---

## GAP 1：Skill 依赖链断裂 🔴

**证据**：ET6 任务中 workline-execution 已加载，但 Hermes 仍然直接写代码。根因不是"忘了约束"，是**协作 skill 没加载**。

```
workline 加载 ✅ → 说"用 delegate_task 交给 Codex"
                    但 codex skill 没加载 ❌
                    但 subagent skill 没加载 ❌
                    → Hermes 不知道 delegate_task 怎么用
                    → 自己写了
```

**断裂点**：workline 约束依赖 codex + subagent-driven-development + claude-code，但 skill 之间没有依赖声明。

**修复**：workline SKILL.md 加一段"必须先加载的协作 skills"，Hermes 在 Phase 0 自动加载它们。

---

## GAP 2：GATE 0 准入检查缺失 🔴

**证据**：

| ET6 实际浪费 | 如果有 GATE 0 |
|:---|:---|
| 不知道 ET6 工程在哪 → 手动找 | 准入时确认工程路径 |
| `dotnet build` 路径错 → 报错 | 验证 dotnet 可用 + .sln 路径 |
| GM 按钮无响应 → 排查服务器 | 确认服务器已启动 + GM 权限 |
| Codex sandbox 崩两次 → 浪费时间 | 预检 sandbox 可用性 |

**断裂点**：没有环境就绪检查。Phase 1 直接开始读文档，环境问题在后续阶段逐个爆炸。

**修复**：workline 新增 Phase 0（GATE 0），产出 `ENV_CHECK.md`。

---

## GAP 3：Claude Code 审查只有指令，没有模式 🟡

**证据**：workline Phase 7 说"Use Claude Code (claude -p) to review"，但没有：

- Claude Code 的调用范例（和 codex exec 一样需要有模式）
- 审查输入物规格（git diff 还是全文件？哪个范围？）
- 审查输出格式（REVIEW.md 必须包含什么字段？）
- 回路规则（审查不通过 → 回到编码还是直接修？）

**断裂点**：审查是可操作的，没有模板。本次被跳过，原因之一是"不知道具体怎么做"。

**修复**：workline 加一个审查模板（review checklist + Claude Code 调用范例）。

---

## GAP 4：Skill 目录未纳入 harness repo 同步 🟡

**证据**：`hermes-harness` 仓库是 source of truth，但 `~/.hermes/skills/` 是运行时加载的。两者目前手动同步（这次是 cp），没有机制保证一致。

**断裂点**：在 harness repo 改完 skill，忘记 cp 到 ~/.hermes/skills/ → 下次任务加载旧版本。

**修复**：小步方案 — CONTRIBUTING.md 加一条"改完必须 cp 到运行时目录"。大步方案 — 后续用 symlink 或脚本同步。

---

## 不需要补的（有证据）

| v2 提议 | 为什么不补 |
|:---|:---|
| 独立 et6-gm-testing skill | 已在 workline references 中 |
| codex sandbox patch | codex skill Rule 3 已有 |
| subagent delegation patch | subagent skill Workline Integration 已有 |
| 任务分类器 | 只有一种任务类型 |
| 指标系统 | 需要多次运行数据 |

---

## 补什么

```
GAP 1 → workline 加依赖声明段
GAP 2 → workline 加 Phase 0（GATE 0 准入检查）
GAP 3 → workline 加审查模板段
GAP 4 → CONTRIBUTING.md 加同步规则
```

全部在 workline-execution 一个 skill 上 patch。一个 commit。
