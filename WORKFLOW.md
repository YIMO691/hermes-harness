# 管线设计

> Harness Engineering 的核心文档。不是"怎么做任务"，是"管线本身怎么进化"。

## 架构

```
任务需求
    │
    ▼
┌──────────────┐
│  workline    │ ← 状态机：分析→审计→SDD→编码→编译→审查→测试→复盘
│  (skill)     │
└──────┬───────┘
       │ 分配
       ▼
┌──────────────────────────────────┐
│  Hermes（调度）                   │
│  Codex（写代码 + 识图）           │
│  Claude Code（审查）              │
│  用户（Mentor审阅 + Play测试）    │
└──────────────────────────────────┘
       │
       ▼
   任务完成
       │
       ▼
┌──────────────┐
│  retrospectives/  │ ← 复盘：断裂点 → Skill 改进
│  (自动生成)       │
└──────┬───────┘
       │ patch
       ▼
┌──────────────┐
│  skills/     │ ← 约束更新（git commit + tag）
└──────────────┘
```

## 进化原则

### 只加固断裂点

> 约束 = 成本。只在某点「实际断裂过」时加约束。不提前建「可能需要的墙」。

| 版本 | 断裂点 | 加的约束 |
|:---|:---|:---|
| v1.3 | Hermes 越权写代码 | 编码阶段 Hermes 禁止写 .cs |
| v1.3 | Claude 审查被跳过 | 编译后强制审查 GATE |
| v1.3 | 代码审计缺失 | Phase 1.5 强制 find+读已有代码 |
| v1.3 | GM 知识每次重摸索 | et6-gm-testing skill + references |
| v1.3 | 没有 git | skills/ git init |
| v1.3 | 依赖 skill 未加载 | Phase 0a 自动加载 codex/subagent/claude |
| v1.3 | 环境未就绪就开干 | Phase 0b GATE 0 准入检查 |
| v1.4 | SDD 无作用域边界 | SDD 模板加「非目标」段 |
| v1.4 | 审查只有结论无证据 | Phase 7 输出升级为 4 份结构化报告 |
| v1.4 | Agent 可能越权改无关文件 | Phase 7 checklist 加「无关文件修改检查」 |
| v1.4 | 复盘无面试表达 | Phase 8 加「面试表达」模板 |
| v1.4 | Unity 新建项目缺 UGUI 包 | Phase 5 待加 manifest 检查 |

### Agent 能力退化链

分工不固定。按可用性降级：

```
Codex 可用   → Codex 写代码 + 识图
Codex 不可用 → Claude Code 接管
Claude 不可用 → Hermes 接管（标 [FALLBACK]）
```

降级一次 = 复盘标记一次。连续降级 = 升级为系统问题。

### 每改必 commit

```
git add skills/<name>/SKILL.md
git commit -m "patch: <skill> - <原因>"
# 引用: 复盘/2026-06-21-ET6.md §二.P0
```

## 版本标记

| tag | 含义 |
|:---|:---|
| `v1.4-stable` | SDD 非目标 + 4 份结构化报告 + 越权检查 + 面试复盘 |
| `v1.3-stable` | 依赖加载 + GATE 0 + 审查模板 + 回路机制 |
| `v1.2-stable` | Git 集成 + Agent 契约 + 代码审计 + 审查 GATE |
| `exp/*` | 实验分支，未验证 |
