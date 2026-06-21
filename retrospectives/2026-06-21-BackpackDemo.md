# 复盘：背包筛选 UI（workline v1.4 验证）

> 日期：2026-06-21 | 结果：全部通过 ✅ | 项目：BackpackDemo (Unity 2022.3)

## 任务

在空 Unity 项目中实现背包道具筛选与选中状态保持。6 个 mock 道具，4 个筛选按钮，唯一选中 + 筛选后状态保持。

## v1.4 新增能力验证

| 能力 | 结果 |
|:---|:--:|
| SDD 含非目标段 | ✅ 禁止 14 类操作 |
| 越权检查 | ✅ ChangedFiles 确认 0 无关修改 |
| ChangedFiles.md | ✅ 19 文件全在范围内 |
| TestReport.md | ✅ 28 项代码审查通过，9 项诚实标注 UNVERIFIED |
| RiskReport.md | ✅ 5 类风险（Editor脚本/字体/空引用/反射/幂等） |
| 面试表达 | ✅ ObsidianNote.md |
| 回路机制 | ⬜ 未触发（审查 PASS） |

## 执行过程

```
SDD → Codex(4 commits, 7 .cs + scene) → compile(12 errors: 缺 ugui)
  → fix manifest → compile(0 errors) → review(4 reports PASS)
  → user verify(全部符合)
```

## 断裂点

### P1：Unity 新建项目缺少 UGUI 包

**现象**：`UnityEngine.UI` 命名空间找不到，12 个编译错误。

**根因**：`com.unity.ugui` 未包含在默认模板的 manifest.json 中。

**修复**：manifest.json 加 `"com.unity.ugui": "1.0.0"`

**是否需沉淀到 workline**：是。Phase 5 编译阶段应检查 Unity 项目的 manifest.json。

### P2：Codex 被中断导致报告缺漏

**现象**：delegate_task 超时中断，TestReport.md 和 RiskReport.md 未生成。

**修复**：补 delegate_task 完成报告。审查 GATE 检查了 4 份报告完整性。

## 做得好的

1. SDD 非目标段生效 — Agent 只改了 Inventory/ 和 Scenes/，0 越权
2. 审查发现报告缺失 → 补 delegate_task 完成
3. 编译回路生效：12 错误 → 补包 → 0 错误
4. 用户验证边角全过

## 违规标记

0 违规。0 Hermes .cs 写入。

## Harness 改进

- [ ] Phase 5：Unity 项目编译前检查 manifest.json 是否含 `com.unity.ugui`
- [ ] Phase 7：审查 checklist 加"4 份报告是否全部存在"
