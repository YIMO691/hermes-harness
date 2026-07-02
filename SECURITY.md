# Security Policy

> v1.11-office-onboarding-stable

## Scope

本仓库的安全目标：保护个人仓库、Hermes 工作线、Office Onboarding 使用场景中的敏感信息边界。

本仓库不是公司安全文档。本策略的合规要求不替代公司安全政策。

---

## Secrets

以下内容**永远不进入仓库**：

- API Key / Token / Secret / Bearer
- 服务端 IP / 端口
- 数据库连接字符串
- 个人身份信息
- `.env` 文件

---

## Office Onboarding Security Model

v1.11 引入 Office Onboarding 安全模型。核心规则：

**公司规范未确认时，默认进入 safe-note。**

### Default Rule

```
Company Policy Gate = UNKNOWN → safe-note
```

在 safe-note 下：
- 不扫描公司项目
- 不读取公司源码
- 不调用 Codex 修改公司代码
- 不向 ChatGPT 发送公司细节
- 不保存公司敏感信息

---

## Forbidden Data

以下内容**永远不进入 hermes-harness 仓库、Obsidian 工作 Vault、reports、或任何持久存储**：

- 公司源码
- 内部路径
- 内部类名 / 方法名
- 协议名 / 字段名
- 配置字段
- 资源名 / Prefab 名
- 服务器地址
- 账号 / Token / Key
- 未公开玩法 / 活动 / 数值
- 具体 Bug 单内容
- 内部文档原文

---

## Tool Boundaries

### Hermes

**允许**：
- 方案分析、任务拆解
- 生成提问话术、日报模板
- 脱敏复盘、checklist、SOP
- 通用技术概念解释（ET6、Unity 原理等）

**禁止**：
- 未授权扫描公司项目目录
- 未授权读取公司源码
- 未授权修改公司文件
- 自动外发公司内容

### Codex

```
Codex is an authorized-only executor.
```

- 公司规范未确认 → 不调用 Codex 处理公司代码
- 公司规范 = ALLOWED_NOTE → 不调用 Codex
- 公司规范 = ALLOWED_AGENT + 用户显式授权 → 允许在授权范围内执行
- personal-lab → 无限制

### ChatGPT / External LLMs

**只能接收脱敏后的抽象问题和方案。**

不得发送：
- 公司源码
- 内部文档
- 具体 Bug 描述
- 具体需求内容
- 内部协议 / 配置 / 资源信息

---

## Obsidian Work Vault

工作 Vault 只能保存：
- 抽象经验
- 通用 SOP / checklist
- 提问模板
- 脱敏日报 / 周报
- 脱敏复盘

**不能保存公司具体实现。** 详见 `docs/OBSIDIAN_WORK_VAULT_SAFE_STRUCTURE.md`。

---

## Git Guardrails

- 禁止 `git push --force`
- 禁止 `git reset --hard`
- 禁止 `git clean -fd`

---

## Incident Handling

如果发现敏感信息进入仓库：

1. 立即停止当前提交
2. 不在日志/终端中输出原文
3. 记录文件路径和敏感信息类型
4. 清理敏感内容后重新审计
5. 必要时重写 git 历史（`git filter-branch`），但必须由用户确认

---

## Repository Scope

本仓库管理：
- `skills/` — 管线约束（纯文本，无密钥）
- `docs/` — 架构 / 计划 / 审计 / 证据
- `templates/` — 可复用模板
- `regression/` — 回归用例
- `retrospectives/` — 复盘记录（脱敏后）
- `reports/` — Phase 审计报告
- `tools/` / `tests/` / `scripts/` — 工程工具
- `.github/workflows/` — CI 配置
- 项目文档（README / CONTRIBUTING / SECURITY / AGENTS）

不管理：
- `~/.hermes/` 完整配置目录（含 token、provider 配置）
- ET6 工程代码
- 任何含密钥的文件
