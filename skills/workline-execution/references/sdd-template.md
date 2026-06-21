# SDD 需求拆分模板

> 设计文档已过（Mentor签字 ✅）后使用。目的：把功能描述转为可执行的任务列表。

---

## 当前代码盘点

| 层 | 文件 | 状态 |
|:---|:---|:--:|
| Server/Model | `PlayerXxxComponent.cs` | ❌/✅ |
| Server/Hotfix | `PlayerXxxComponentSystem.cs` | ❌/✅ |
| ... | ... | ... |

## 任务拆分（按依赖顺序）

### Task N: 任务名
**依赖**: Task X | **预估**: N文件

| # | 文件 | 内容 |
|:--|:---|:---|
| N.1 | `path/to/File.cs` | 该文件的核心职责 |

**验证**: 如何确认此 Task 完成。

---

## 依赖图

```
Task1 (底层依赖)
  ├── Task2
  │     └── Task3
  └── Task4
```

## 验收标准

- [ ] 编译：`dotnet build` 0 Error
- [ ] UI：Unity 无编译错误
- [ ] 功能：每个操作路径可走通
- [ ] GM：测试界面可操作

## 分工

- **Codex**: 写代码
- **Claude Code**: 审查
- **Hermes**: 调度 + 编译
- **User**: Unity Play + 截图
