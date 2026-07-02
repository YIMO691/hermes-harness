# Office Onboarding Modes — Runtime Reference

> 版本：v1.11 | 来源：`docs/OFFICE_ONBOARDING_WORKLINE_V1.11.md` §4
>
> 本文档是 Mode Router 的模式判定参考。每次任务启动时，Mode Router 按以下优先级判定应该进入哪个模式。

---

## Priority Order

```text
1. If 项目 = personal-lab 声明 → personal-lab (no safety shell)
2. If Company Policy Gate = UNKNOWN 或 DENIED → safe-note
3. If Company Policy Gate = ALLOWED_NOTE → office-lite
4. If Company Policy Gate = ALLOWED_AGENT + 用户授权范围 → full-harness
```

判定逻辑：**先看项目归属，再看 Policy Gate 状态。** Policy Gate 是 UNKNOWN 时，即使公司项目也无法升级。

---

## Mode 1: safe-note

**触发**: Company Policy Gate = UNKNOWN 或 DENIED

**前缀标记**: `[SAFE_NOTE]`

### 允许

| 动作 | Level |
|:---|---|
| 生成提问话术 | 0 |
| 生成日报/周报模板 | 0 |
| 生成脱敏 Work Card | 0 |
| 生成安全边界提醒 | 0 |
| 整理手动输入的抽象经验 | 0 |
| 通用技术概念解释（不涉及公司项目） | 0 |
| 需求拆解（仅给抽象模板框架，不涉及具体需求内容） | 1 |

### 禁止

- 读取公司源码
- 扫描公司项目目录
- 调用 Codex 修改任何代码
- 保存公司具体信息
- 外发内部信息
- 后台常驻
- 跨会话记忆公司内容

### 自动行为

- 每次响应前自动标注 `[SAFE_NOTE]`
- 用户提到公司相关内容时，提醒"当前为 safe-note 模式，不处理公司具体信息"
- 如果用户粘贴了可能包含公司信息的文本，只做通用分析，不保存源文本

---

## Mode 2: office-lite

**触发**: Company Policy Gate = ALLOWED_NOTE

**前缀标记**: `[OFFICE_LITE]`

### 允许

| 动作 | Level |
|:---|---|
| safe-note 全部动作 | 0-1 |
| 需求摘要 | 1 |
| 歧义识别 | 1 |
| 影响面拆解（客户端/服务端/配置/UI/资源/测试） | 1 |
| 确认问题清单 | 1 |
| 验收标准 | 1 |
| 风险提醒 | 1 |
| 汇报草稿 | 1 |
| 脱敏复盘 | 1 |
| 读取用户手动粘贴的指定代码片段 | 2 |

### 禁止

- 自动读取源码
- 自动扫描项目目录
- 自动修改文件
- 调用 Codex 修改代码
- 保存具体内部实现
- 外发公司内容
- 后台常驻

### 用户粘贴代码的特殊规则

- 仅用于当前分析，不保存到文件
- 不索引
- 不跨会话记忆（memory 工具不记录）
- 不发送给外部模型（Codex/Claude Code/ChatGPT）

---

## Mode 3: full-harness

**触发**: Company Policy Gate = ALLOWED_AGENT + 用户显式授权范围

**前缀标记**: `[FULL_HARNESS: <授权范围>]`

### 前置条件（必须全部满足）

1. Company Policy Gate = ALLOWED_AGENT
2. 用户通过 `clarify()` 确认授权范围（目录路径、允许的操作级别）
3. 授权范围记录在当前会话的上下文中

### 允许

| 动作 | Level |
|:---|---|
| office-lite 全部动作 | 0-2 |
| 扫描指定目录 | 3 |
| 修改本地文件（授权范围内） | 4 |
| Codex 写代码（授权范围内） | 5 |
| 走完整 v1.10 管线 | — |

### 禁止

| 动作 | 理由 |
|:---|:---|
| 超出授权范围的目录 | 安全规则 |
| 执行 git push | Level 6 永远禁止 |
| 后台常驻 | Level 6 永远禁止 |
| 自动提交 | Level 6 永远禁止 |
| 使用 Claude Code 审查公司代码 | 需外发，安全风险 |

### 授权记录格式

```text
[FULL_HARNESS]
  授权目录: <绝对路径>
  允许操作级别: 3 | 4 | 5
  授权时间: <ISO时间>
  有效期: 当前会话
```

---

## Mode 4: personal-lab

**触发**: 用户显式声明项目为 personal 项目（或者从 v1.10 直接调用）

**前缀标记**: `[PERSONAL_LAB]`

### 行为

**与 v1.10 的 full/quick 模式完全相同，不应用任何 v1.11 安全限制。**

所有 AUTO-BLOCK 规则、GATE 0、冲突门、审查门、覆盖门、经验注入均正常运作。

### personal-lab 项目列表

以下路径被识别为 personal-lab:

- `C:\Users\20544\Desktop\解题\testc\HotZoneTestC`
- `D:\Edge下载文件\...\project\ET6` (DailyReward)
- `D:\ET_official_release6.0`
- `C:\Users\20544\ET6源码学习沉淀`
- `C:\Users\20544\Desktop\hermes-harness`
- `C:\Users\20544\Desktop\Learning`

### 如何声明新的 personal-lab 项目

用户在任何时候可以说 "这是个人项目" → 当前任务自动切换为 personal-lab。

---

## Mode Resolution Examples

| 用户输入 | Policy Gate | 判定模式 |
|:---|:---|:---|
| "帮我分析 DailyReward 的代码" | — | personal-lab (已知 personal 路径) |
| "公司项目里这个 Bug 怎么修" | UNKNOWN | safe-note |
| "公司项目里这个 Bug 怎么修" | ALLOWED_NOTE | office-lite |
| "公司项目里这个 Bug 怎么修" | ALLOWED_AGENT | full-harness (需授权范围) |
| "帮我扫一下公司项目目录" | ALLOWED_NOTE | ❌ BLOCKED (office-lite 不允许扫描) |
| "这个 ET6 概念是什么意思" | 任意 | 通用学习 → 不依赖模式 |
