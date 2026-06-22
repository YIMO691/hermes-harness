# Agent 分工契约

> 角色定义、约束、降级规则。违反 = 复盘标记。

## 角色矩阵

| 角色 | 职责 | 禁止 | 降级 |
|:---|:---|:---|:--:|
| **Hermes** | 调度、编译验证、GM准备、写分析/SDD/复盘 | 写 .cs 文件（编码阶段） | — |
| **Codex** | 写代码、识图 | 做架构决策 | Claude 接管 |
| **Claude Code** | 代码审查（模式/空安全/IsCan+Do完整性） | 写新代码 | Hermes 自查 |
| **用户** | Mentor 审阅（签字）、Unity Play 测试（截图） | 代替 Agent 写代码 | — |

## 违规标记

| 标记 | 触发 | 严重度 |
|:---|:---|:--:|
| `[VIOLATION: herm-write-code]` | Hermes 写了 .cs 文件 | ⚠️ |
| `[VIOLATION: skip-review]` | 编译后没跑审查 | 🔴 |
| `[VIOLATION: skip-audit]` | 编码前没做代码审计 | ⚠️ |
| `[FALLBACK: herm-review]` | Claude 不可用，Hermes 自查 | 🟡 |
| `[FALLBACK: herm-code]` | Codex+Claude 都不可用 | 🟡 |

## 降级链

```
优先: Codex 写代码 → Claude Code 审查
  ↓ Codex 不可用
降级: Claude Code 写代码 → Hermes 自查 → [FALLBACK]
  ↓ Claude 不可用
降级: Hermes 写代码 → [FALLBACK: herm-code]
```

每次降级 = 复盘标记。连续降级需修复基础设施。

## 调用方式

### Codex 写代码

```
delegate_task(goal="编写 PlayerNerveComponent.cs...", toolsets=["terminal","file"])
```

### Codex 识图

```
echo "分析这些截图..." | codex exec -i image1.png -i image2.png --skip-git-repo-check
```

### Claude Code 审查

```
delegate_task(goal="审查以下代码的 IsCan+Do 完整性...", context="GAP.md + git diff")
```

## 不可绕过

审查阶段不能跳过。用户说"跳过" → 复盘标记 `[VIOLATION: skip-review]`。

---

## Repository Placement Protocol

> 约束 Agent 在新增文件、目录、工具、任务证据时的放置行为。
> 规则来源：`docs/WORKLINE_REPOSITORY_STRUCTURE.md`

### 必须先查规则

任何 Agent 在新增文件、目录、工具、测试、任务证据、评估报告、skill、observability 相关内容前，**必须先参考**：

```text
docs/WORKLINE_REPOSITORY_STRUCTURE.md
```

### 新增文件必须说明归属

如果新增文件，Agent 必须在任务报告中说明：

```text
File:
Target path:
Directory category:
Reason:
Alternatives considered:
```

### 不确定时必须询问用户

如果出现以下情况，Agent **不得自行决定**，必须询问用户：

- 新增一级目录
- 新增 skill
- 新增 `observability/`
- 新增 `skills/workline-evaluation/`
- 新增 `skills/workline-observability/`
- 新增长期工具
- 移动 existing stable evidence
- 修改 CI/checker 路径
- 文件可以放在多个目录且边界不清

询问格式：

```text
Placement decision required.

Option A:
- path:
- reason:
- risk:

Option B:
- path:
- reason:
- risk:

Recommended:
- path:
- reason:
```

### future-only 目录不得空建

以下目录**只允许在真实实现任务启动后创建**：

```text
observability/
skills/workline-evaluation/
skills/workline-observability/
```

不得为了"先占位置"空建。空目录 = C 级证据（仅文档化），不得计入工程化。

### 文档化不等于工程化

```
A/B evidence can count as engineering maturity.
C-level documentation can only count as design maturity.
D/E evidence must not be counted as implemented capability.
```

### 迁移必须单独立项

任何文件移动 / 目录重组都必须：

1. 单独任务
2. 单独分支
3. 说明 old path / new path
4. 更新引用路径
5. 跑 CI
6. 生成 migration report
7. 用户确认后执行

不允许在功能任务中顺手搬目录。
