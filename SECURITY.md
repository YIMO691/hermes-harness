# 安全策略

## 不存入仓库

- API Key / Token / Secret
- 服务端 IP / 端口
- 数据库连接字符串
- 个人身份信息

## Git Guardrails

本仓库启用 `git-guardrails-claude-code` Skill：
- 禁止 `git push --force`
- 禁止 `git reset --hard`
- 禁止 `git clean -fd`

## 仓库范围

本仓库仅管理：
- `skills/` — 管线约束（纯文本，无密钥）
- `retrospectives/` — 复盘记录（脱敏后）
- `regression/` — 回归用例
- `tools/` — checker 等工具
- `tests/` — 测试 fixtures
- `.github/workflows/` — CI 配置
- 项目文档（README / CONTRIBUTING / WORKFLOW / AGENTS / SECURITY）

不管理：
- `~/.hermes/` 完整配置目录（含 token、provider 配置）
- ET6 工程代码
- 任何含密钥的文件
- `.env` 文件
