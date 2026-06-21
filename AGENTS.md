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
