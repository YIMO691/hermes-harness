# Phase 6.7: v1.10 Intake Reconstruction

> 日期：2026-07-02 | 策略：结构化补全（B 路线）

## 1. 三源交叉提取

| 源 | 内容 | Intake 覆盖 |
|:---|:---|:---:|
| **tasks/v1.10 evidence** | 7 份完整 Intake 文档（New Item Badge 任务） | ✅ 完整 — AmbiguityReport/ModeRouting/TaskBreakdown/AcceptanceCriteria/ClientImpactMap/ImplementationBrief/RequirementDigest |
| **runtime SKILL.md** | 在 office-lite 描述中提到了 "ambiguity reports" | ⚠️ 仅提及，无独立章节 |
| **repo SKILL.md (修改前)** | 无 Intake 内容 | ❌ 空 |

## 2. 提取方法

基于 7 份 task evidence 的实际内容格式，提取每个文档的精确定义：

| 文档 | 提取自 | 证据特征 |
|:---|:---|:---|
| AmbiguityReport | `AmbiguityReport.md` | BLOCKER/HIGH/MEDIUM/LOW 分级，resolved 状态，RESOLVED 标记 |
| ModeRoutingDecision | `ModeRoutingDecision.md` | quick/full 决定，文件数/行数估计，scope 检查，handoff target |
| TaskBreakdown | `TaskBreakdown.md` | Epic→Feature→Task 三级分解，per-task 文件/子任务/模式/依赖表 |
| AcceptanceCriteria | `AcceptanceCriteria.md` | 5 类：Functional/UI/State/Non-functional/Regression，全 checklist |
| ClientImpactMap | `ClientImpactMap.md` | 14 个 Area × 5 列（Impact/Action/Evidence/Risk） |
| ImplementationBrief | `ImplementationBrief.md` | Goal/Confirmed Requirements/Proposed Changes/Recommended Mode |
| RequirementDigest | `RequirementDigest.md` | 10 节：Source/Feature/Player/Core Rules/User Flow/State Flow/Data Flow/Out of Scope/Assumptions/Open Questions |

## 3. 插入位置

```
52: ## Office Onboarding (v1.11)    ← v1.11 安全层
    ...
101: ## Requirement Intake (v1.10)   ← 新增 Intake
    ...
131: ## Mode Router                  ← 原有路由器
```

位置选择理由：Intake 运行在 Mode Router 之前——先理解需求，再分类路由。

## 4. 补全范围

| Intake 文档 | SKILL.md 中定义 | 独立模板 |
|:---|:---:|:---:|
| AmbiguityReport | ✅ 表格 + 用途 | — |
| ModeRoutingDecision | ✅ 表格 + 用途 | — |
| TaskBreakdown | ✅ 表格 + 用途 | — |
| AcceptanceCriteria | ✅ 表格 + 用途 | — |
| ClientImpactMap | ✅ 表格 + 用途 | — |
| ImplementationBrief | ✅ 表格 + 用途 | — |
| RequirementDigest | ✅ 表格 + 用途 | — |
| **Lite 版本 (office-lite)** | 引用 | `templates/office_onboarding/requirement_intake_lite.md` |

## 5. 与 office-lite 的衔接

Intake section 明确引用 office-lite 模板：
```
- office-lite mode: Use templates/office_onboarding/requirement_intake_lite.md instead
```

这保证了公司入职场景下不会走完整的 7 文档 Intake 流程。

## 6. 不改变项

- ✅ v1.11 Office Onboarding: 未修改
- ✅ v1.10 原有 Phase 0-8: 未修改
- ✅ personal-lab: 未修改
- ✅ Mode Router: 未修改

## 7. 仍然缺失的 v1.10 特性

以下特性存在于运行时 `~/AppData/Local/hermes/skills/workline-execution/SKILL.md` 中，但尚未同步到 repo：

| 特性 | 运行时行号 | 状态 |
|:---|:---:|:---:|
| Phase 0 .bak AUTO-BLOCK (完整格式) | 179 | ❌ repo 仅有 pitfall 级 |
| Phase 1 学习产出清单 AUTO-BLOCK | 197 | ❌ |
| Phase 7 命名合规 grep AUTO-BLOCK | 607 | ❌ |
| Phase 8 审计版本确认 AUTO-BLOCK | 692 | ❌ |
| Phase 7.5 Coverage Gate | 667 | ❌ |
| Experience Injection 8c (4通道) | 758 | ❌ |
| Hungarian naming references | 607+ | ❌ |

**建议**: 后续 Phase（如 6.8）执行 runtime→repo 的结构化合并（非整文件替换），将以上特性逐个 patch 入 repo。
