# Phase 6.5: v1.10 兼容性审计

> 日期：2026-07-02 | 分支：`feature/v1.11-office-onboarding`
>
> 目的：确认 v1.11 没有绕过、覆盖或遗漏 v1.10 的关键规则。

---

## 1. 前置确认

| 项目 | 值 |
|:---|---|
| 审计分支 | `feature/v1.11-office-onboarding` |
| 审计 commit | `ba409ab` — "feat: v1.11 Phase 3-6" |
| SKILL.md 路径 | `skills/workline-execution/SKILL.md` |
| SKILL.md header 版本 | `version: 1.11.0` |
| SKILL.md 总行数 | 805 行 |

---

## 2. v1.10 AUTO-BLOCK 规则检查

v1.10 定义了 4 条 AUTO-BLOCK 规则。逐一检查：

| # | 规则 | v1.10 描述 | SKILL.md 中状态 | 判定 |
|:--|:---|:---|:---|:---:|
| 1 | Phase 0 .bak 检测 | `find . -name '*.bak' \| head -20`；非空 → 强制 `git init` | 有 5 处 .bak 引用，但均为 pitfall 级建议，不包含 grep 命令、Blocking rules 表格、Evidence format 模板 | ⚠️ 存在但未升级为 AUTO-BLOCK 格式 |
| 2 | Phase 1 学习产出清单 | Phase 1 末尾的"学习产出应用清单"表格；学了不用不准进 Phase 2 | **不存在**。grep `学习产出\|AUTO-BLOCK.*Phase 1` → 0 matches | ❌ 缺失 |
| 3 | Phase 7 命名合规 grep | `grep -rn 'p_n[A-Z]\|p_sz[A-Z]\|p_b[A-Z]'`；匹配 → NEEDS_FIX | **不存在**。grep `p_n\|p_sz\|naming.*check\|Naming.*Standard` → 0 matches | ❌ 缺失 |
| 4 | Phase 8 审计版本确认 | `git status -s` + `git log origin/main..HEAD` 确认审计目标 | **不存在**。grep `审计.*版本\|8\.0.*AUTO\|git status.*非空` → 0 matches | ❌ 缺失 |

**AUTO-BLOCK 结论**: 4 条规则中 1 条部分存在（未格式化），3 条完全缺失。❌ 不通过。

---

## 3. Experience Injection (经验注入) 检查

v1.10 的经验注入框架包含：

| 组件 | v1.10 描述 | SKILL.md 中状态 | 判定 |
|:---|:---|:---|:---:|
| 8c 经验资产注入章节 | 4 条通道检查（Rule/Metric/Template/Capability）+ 强制 metrics.yaml 填写 | **不存在**。grep `8c\|经验资产\|experience.injection\|四条通道` → 0 matches | ❌ 缺失 |
| Capability 矩阵引用 | `references/harness-capability-matrix.md` 的引用和更新规则 | **不存在** | ❌ 缺失 |
| metrics.yaml 的 `harness_injection` 字段 | yaml 模板中的 injection 段要求 | **不存在** | ❌ 缺失 |

**Experience Injection 结论**: 完全缺失。❌ 不通过。

---

## 4. Requirement Intake (需求摄入) 检查

v1.10 的 Intake 管线包含 7 份文档：

| 文档 | 搜索关键词 | SKILL.md 中状态 | 判定 |
|:---|:---|:---|:---:|
| AmbiguityReport | AmbiguityReport | 0 matches | ❌ 缺失 |
| ModeRoutingDecision | ModeRouting | 0 matches | ❌ 缺失 |
| TaskBreakdown | TaskBreakdown | 0 matches | ❌ 缺失 |
| AcceptanceCriteria | AcceptanceCriteria | 0 matches | ❌ 缺失 |
| ClientImpactMap | ClientImpactMap | 0 matches | ❌ 缺失 |
| ImplementationBrief | ImplementationBrief | 0 matches | ❌ 缺失 |
| RequirementDigest | RequirementDigest | 0 matches | ❌ 缺失 |

**Intake 结论**: 完全缺失。❌ 不通过。

---

## 5. 其他 v1.10 特征检查

| 特征 | 搜索 | 结果 | 判定 |
|:---|:---|:---|:---:|
| Phase 7.5 Coverage Gate | `7\.5\|Coverage\|白盒覆盖` | 0 matches | ❌ 缺失 |
| Hungarian naming references | `hungarian\|Hungarian\|命名规范` | 0 matches | ❌ 缺失 |
| 冲突门 / 非目标 | `Conflict Gate\|非目标\|冲突` | ✅ 存在（line 250, 266） | ✅ |
| Phase 8b metrics | `8b\|metrics` | ✅ 存在（line 602） | ✅ |
| Core Pipeline Phase 0-8 | `### Phase [0-8]` | ✅ 全部 9 个 Phase 存在 | ✅ |

---

## 6. personal-lab 行为检查

| 检查项 | 结果 |
|:---|:---|
| personal-lab 模式是否定义 | ✅ line 71: "Full v1.10" |
| personal-lab 是否无安全壳 | ✅ line 94: "no safety shell, full v1.10" |
| Mode Router 是否保留 full/quick 路由 | ✅ line 104: "for personal-lab tasks, the original full/quick router applies" |
| Core Pipeline 是否完整 | ✅ Phase 0-8 全部保留 |

**personal-lab 结论**: ✅。v1.11 新增 Office Onboarding 章节没有改变 personal-lab 下的行为定义。

---

## 7. 版本号策略

| 项目 | 值 |
|:---|:---|
| 修改前 header 版本 | `version: 1.7.0` |
| 修改后 header 版本 | `version: 1.11.0` |
| 修改前内容对应的实际版本 | v1.7（缺少 v1.8/1.9/1.10 规则） |
| 根因 | GAP #4 — "Skill 目录未纳入 harness repo 同步"。v1.8/1.9/1.10 的更新应用到运行时 `~/.hermes/skills/` 但未回写到 repo 的 `skills/workline-execution/SKILL.md` |

**版本号判定**: header `1.7.0` 对 repo 文件是准确的（不是滞后，是 repo 文件确实停留在 v1.7）。v1.11 修改在这个基础上做了正确的新增。但 v1.8/v1.9/v1.10 的 repo 同步从未发生。

---

## 8. 审计总结论

```
┌──────────────────────────────────────────────────────────────┐
│  ❌ BLOCKED — v1.10 规则缺失，不允许进入 Phase 7。           │
│                                                              │
│  缺失项:                                                      │
│  • 4 条 AUTO-BLOCK 规则（3 条完全缺失，1 条未格式化）          │
│  • Experience Injection 框架（8c 章节 + 4 通道 + metrics 字段）│
│  • Requirement Intake 管线（7 文档链路）                       │
│  • Phase 7.5 Coverage Gate                                   │
│  • Hungarian naming standard 引用                             │
│                                                              │
│  保持项:                                                      │
│  • Core Pipeline Phase 0-8 ✅                                │
│  • Conflict Gate ✅                                           │
│  • personal-lab v1.10 行为 ✅                                 │
│  • v1.11 Office Onboarding 新增 ✅                            │
│                                                              │
│  根因: GAP #4 — v1.8/v1.9/v1.10 的运行时 skill 更新未回写    │
│  到 hermes-harness 仓库的 skills/workline-execution/SKILL.md  │
└──────────────────────────────────────────────────────────────┘
```

---

## 9. 是否允许进入 Phase 7

**不允许。** 按审计规则："如果 v1.10 规则缺失，立即 BLOCKED，不进入 Phase 7。"

---

## 10. 建议的修复策略（供用户决策）

| 选项 | 描述 | 工作量 | 风险 |
|:---|:---|:---|:---|
| A | 将运行时 `~/.hermes/skills/workline-execution/SKILL.md` 的 v1.10 版本复制到 repo，再在顶部重新应用 v1.11 的新增内容 | 低（文件替换 + 1 次 patch） | 低 |
| B | 保持 repo 当前 v1.7+v1.11 为 base，逐个手动补回 v1.10 规则 | 中（6 处补丁） | 可能遗漏 |
| C | 先合并 v1.10 到 repo，再将 v1.11 分支 rebase 到 v1.10 | 中 | Git rebase 可能冲突 |

---

## 11. git status

```
On branch feature/v1.11-office-onboarding
working tree clean
2 commits ahead of master
latest: ba409ab
```

---

## 12. 敏感信息检查

| 检查 | 结果 |
|:---|---|
| 包含公司源码 | 无 |
| 包含内部路径 | 无 |
| 包含 Token/Key | 无 |
