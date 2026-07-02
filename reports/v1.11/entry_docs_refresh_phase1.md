# Entry Docs Refresh — Phase 1

> 日期：2026-07-02 | 基于 Phase 0 审计报告

## 1. 修改文件

| 文件 | 操作 | 说明 |
|:---|:---:|:---|
| `README.md` | 重写 | 从 v1.9 更新到 v1.11-office-onboarding-stable |
| `CONTRIBUTING.md` | 更新 | 新增 Office/Security/MANUAL_VERIFY/封版规则 |
| `SECURITY.md` | 重写 | 从密钥防泄漏升级为 Office Onboarding 安全策略 |
| `docs/INDEX.md` | 新建 | 统一文档索引 |
| `reports/v1.11/entry_docs_refresh_phase1.md` | 新建 | 本报告 |

## 2. README 更新摘要

| 之前 (v1.9) | 之后 (v1.11) |
|:---|:---|
| Badge: `v1.9-stable` | Badge: `v1.11-office-onboarding-stable` |
| 版本列表到 v1.10 trial | 版本列表到 v1.11-stable，含 v1.10 baseline 回填说明 |
| 无 Office Onboarding 介绍 | Architecture 图 + Why v1.11 对比表 |
| 无模式说明 | 4 modes 表格 |
| 无 Gate 说明 | 5 gates 表格 |
| 文档索引只到 v1.9 | 包含所有 v1.11 关键文档链接 |
| 无安全声明 | Safety Notice（公司规范未确认默认 safe-note） |
| "当前不做"含"新 active Gate" | 移除（v1.11 已新增 5 个 Gate） |
| 最后更新 2026-06-22 | 已更新 |

## 3. CONTRIBUTING 更新摘要

新增规则：

| 规则 | 来源 |
|:---|:---|
| **Skill 同步铁律（GAP #4 修复）** | v1.8/1.9/1.10 runtime→repo 分裂教训 |
| **Office Mode 修改规则** | v1.11 — 涉及模式/Gate 改动必须走 regression |
| **MANUAL_VERIFY 规则** | 不能伪装成自动化测试 |
| **封版规则** | stable tag 必须具备的 6 项条件 |
| **禁止事项（6 条）** | 安全红线 |

## 4. SECURITY 更新摘要

| 之前 (pre-v1.7) | 之后 (v1.11) |
|:---|:---|
| 32 行，仅覆盖 API Key/Token | 120+ 行，覆盖 Office Onboarding 安全模型 |
| 无公司安全策略 | Default rule: UNKNOWN → safe-note |
| 无 Forbidden Data 列表 | 11 项禁止保存内容 |
| 无工具边界 | Hermes / Codex / ChatGPT 三层边界 |
| 无 Obsidian Vault 规则 | 工作 Vault 安全规则 |
| 无 Incident Handling | 敏感信息发现后处理流程 |

## 5. docs/INDEX.md 摘要

新增统一文档索引，覆盖 6 个分组：
- Start Here（3 个入口）
- Office Onboarding（5 个 v1.11 文档）
- Workline Architecture（6 个架构文档）
- Skills / Templates / Regression / Reports / Stable Tags

## 6. LICENSE

未修改。保持 MIT / 2026 / YIMO691。

## 7. 敏感信息检查

| 检查 | 结果 |
|:---|---|
| API Key / Token | 无 |
| 公司路径 | 无 |
| 内部类名 | 无 |
| 公司源码 | 无 |
| git diff 扫描 | 0 matches |

✅ 零敏感信息。

## 8. 禁止范围确认

| 文件/目录 | 是否修改 |
|:---|:---:|
| SKILL.md | ❌ 未改 |
| checker (tools/) | ❌ 未改 |
| CI (.github/) | ❌ 未改 |
| regression/ | ❌ 未改 |
| templates/ | ❌ 未改 |
| LICENSE | ❌ 未改 |
| ET6 / DailyReward | ❌ 未接触 |

✅ 修改范围正确。

## 9. git status

```
3 files modified (README + CONTRIBUTING + SECURITY)
1 file new (docs/INDEX.md)
1 file new (this report)
5 files total, clean working tree after commit
```

## 10. 结论

**✅ PASS — 建议提交。**
