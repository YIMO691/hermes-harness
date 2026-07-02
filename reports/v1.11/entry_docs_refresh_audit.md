# v1.11 Entry Docs Refresh Audit

> 日期：2026-07-02 | 审计类型：入口文档差距分析（只读）

---

## 1. 仓库状态

| 项目 | 值 |
|:---|---|
| 当前分支 | `master` |
| 当前 commit | `62cb7e5` (merge: v1.11 → master) |
| git status | clean |
| stable tag | `v1.11-office-onboarding-stable` ✅ |

---

## 2. 总体结论

| 入口文档 | 是否落后 | 严重程度 |
|:---|:---:|:---:|
| **README.md** | ❌ 严重落后 | 🔴 高 — 停留在 v1.9 |
| **CONTRIBUTING.md** | ❌ 落后 | 🟡 中 — 停留在 v1.10 trial |
| **SECURITY.md** | ❌ 严重落后 | 🔴 高 — 停留在 v1.7 之前 |
| **LICENSE** | ✅ 无误 | 🟢 不需要修改 |
| **docs/INDEX.md** | ❌ 不存在 | 🟡 中 — 13 个 docs 文件无统一入口 |

---

## 3. README 差距

| 检查项 | 当前状态 | 建议 |
|:---|:---|:---|
| 版本 badge | `v1.9-stable` | 更新为 `v1.11-office-onboarding-stable` |
| 当前版本列表 | 只到 v1.10 trial | 增加 v1.11-office-onboarding-stable |
| v1.11 定位说明 | 无 | 增加：Personal Agent Workline + Safe Office Onboarding Harness |
| v1.10 baseline 回填 | 无 | 说明 v1.10 Intake/AUTO-BLOCK/Experience/Coverage 已完整回填 |
| 四种模式 | 无 | 增加 safe-note/office-lite/full-harness/personal-lab |
| 五个 Gate | 无 | 增加 Company Policy/Sensitive Data/Action Permission/Persistence/Mode Switch |
| 链接到 Office 文档 | 无 | 增加：总设计、SOP、每日指南、Vault 安全结构、Release Notes |
| "当前不做" | "新 active Gate" | 移除或修正（v1.11 已新增 5 个 Gate） |
| Mode Router 流程图 | 只显示 full/quick | 增加 office mode 路由 |
| 最后更新时间 | 2026-06-22 | 更新 |
| v1.11 tag 名 | 无 | 写清楚 tag 名称：`v1.11-office-onboarding-stable` |

---

## 4. CONTRIBUTING 差距

| 检查项 | 当前状态 | 建议 |
|:---|:---|:---|
| 版本演进规则 | 停留在 v1.10 trial | 更新当前版本到 v1.11 |
| Office Mode 修改规则 | 无 | 增加：修改 Office Mode/Gate 必须走 office_onboarding regression |
| MANUAL_VERIFY 规则 | 无 | 增加：MANUAL_VERIFY 不能伪装成自动化测试 |
| 安全边界修改规则 | 无 | 增加：修改 Company Policy/Sensitive Data/Persistence Gate 需要额外审查 |
| personal-lab 边界 | 无 | 增加：personal-lab 与 office onboarding 的隔离规则 |
| tag/release 封版要求 | 无 | 增加：必须通过 Phase 9 最终审计才能打 stable tag |
| runtime→repo 同步 | 只写 repo→runtime | 增加：双向同步规则（GAP #4 教训） |

---

## 5. SECURITY 差距

| 检查项 | 当前状态 | 建议 |
|:---|:---|:---|
| API Key / Token 规则 | ✅ 已有 | 保留 |
| Office Onboarding 安全边界 | ❌ 无 | 新增完整章节 |
| 公司规范未知 → safe-note | ❌ 无 | 新增 |
| Codex 待授权执行者 | ❌ 无 | 新增 |
| ChatGPT 脱敏规则 | ❌ 无 | 新增 |
| Obsidian Vault 限制 | ❌ 无 | 新增（11 项禁止保存内容） |
| 敏感信息发现后处理流程 | ❌ 无 | 新增 |
| Git Guardrails | ✅ 已有 | 保留 |
| 仓库范围 | ✅ 已有但需更新 | 增加 v1.11 新增目录 |

**SECURITY 需要新增"Office Onboarding Security Section"，包含**：

- 公司规范未确认时默认 safe-note
- Codex 是待授权执行者（不是默认执行者）
- ChatGPT 只能接收脱敏抽象问题
- Obsidian 工作 Vault 禁止保存内容清单（11 项）
- 敏感信息发现后的处理流程

---

## 6. LICENSE 结论

| 检查项 | 当前状态 | 建议 |
|:---|:---|:---|
| License 类型 | MIT ✅ | 不修改 |
| 年份 | 2026 ✅ | 不修改 |
| 作者 | YIMO691 ✅ | 不修改 |

**结论**：✅ LICENSE 不需要修改。

---

## 7. docs/INDEX.md 建议

**当前状态**：docs/ 目录有 16 个文件（含 evaluations/），无统一入口索引。

**建议新增**：`docs/INDEX.md`

**建议结构**：

```markdown
# docs/INDEX.md

## 快速入口
- 入职第一周 SOP
- 每日使用指南
- Release Notes

## Workline 架构
- v1.7 稳定架构
- 仓库结构治理
- Git 工作流
- 工程评估

## Office Onboarding (v1.11)
- 总设计
- 模式参考
- Gate 参考
- Vault 安全结构
- 入职 Metrics

## Skill / Runtime
- SKILL.md (skills/workline-execution/)

## Regression
- 工程回归 (10 cases)
- Office Onboarding 回归 (6 cases, MANUAL_VERIFY)

## Templates
- Office Onboarding 模板 (6 个)

## Reports
- v1.11 Phase 0-9 审计链

## Stable Tags
- v1.11-office-onboarding-stable
- v1.9-stable
- v1.8-stable
- v1.7-stable
```

---

## 8. 建议修改范围（Phase 1）

| 文件 | 修改类型 | 预估改动量 |
|:---|:---|:---|
| **README.md** | 重写 | 全量更新（版本/能力/文档索引/路线图） |
| **CONTRIBUTING.md** | 新增章节 | + 6 条 Office/Security/MANUAL_VERIFY 规则 |
| **SECURITY.md** | 新增章节 | + Office Onboarding Security Section |
| **docs/INDEX.md** | 新建 | 初始版本 |
| **LICENSE** | 不改 | — |

---

## 9. 风险与禁止事项

Phase 1 修改时必须遵守：

- ❌ 不改 SKILL.md
- ❌ 不改 checker
- ❌ 不改 CI
- ❌ 不改 regression
- ❌ 不接触 ET6 / DailyReward / 公司项目
- ❌ 不修改 LICENSE 正文
- ❌ 不打 tag
- ❌ 不 push（通过 Phase 2 最终确认后再 push）

---

## 10. 是否建议进入 Phase 1

**✅ 建议进入 Phase 1（入口文档刷新）**。

README 和 SECURITY 落后两个大版本（v1.9 → v1.11），已构成"门面与实际不符"的问题。CONTRIBUTING 缺少 Office/Security 修改规则。docs/ 缺少统一入口索引。

建议修改顺序：
1. SECURITY.md（安全声明先于功能描述）
2. README.md（门面更新）
3. docs/INDEX.md（统一索引）
4. CONTRIBUTING.md（演进规则更新）
