# WORKLINE_GIT_WORKFLOW

> 版本：v1.0 | 基于 v1.7-stable
> 状态：Active
> 依赖：`docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md`

---

## 1. 目标

本文件将工作线的 Git Evidence Layer 从"事后记录"扩展为 **Real Work Git Workflow**——模拟真实公司开发中的分支管理、PR/MR 审查、Release 流程和 Rollback 规则。

工作线本身不需要完整 CI/CD 或多人协作，但**流程结构应该与真实团队一致**。这样：
- 每个 task 有清晰的 Git 轨迹
- 每个 merge 经过审查
- 每个 release 有 tag 和验证证据
- rollback 有规则可循

---

## 2. 分支模型

```
main                    ← 生产就绪，只接受 release/hotfix merge
  │
  ├── develop           ← 日常集成分支，接受所有 feature/fix/docs merge
  │   │
  │   ├── feature/<task-id>     ← full 模式任务（新功能/多文件）
  │   ├── fix/<task-id>         ← quick 模式任务（Bug 修复）
  │   ├── docs/<topic>          ← 文档变更
  │   ├── skill/<version>       ← skill patch（管线自身进化）
  │   └── regression/<case-id>  ← 回归用例开发
  │
  ├── release/<version> ← 发布准备分支（从 develop 分出）
  │
  └── hotfix/<issue-id> ← 紧急修复（从 main 分出，合回 main + develop）
```

### 分支命名约定

| 前缀 | 模式 | 示例 |
|:---|:---|:---|
| `feature/` | full | `feature/backpack-favorite` |
| `fix/` | quick | `fix/double-refreshlist` |
| `docs/` | 文档 | `docs/git-workflow` |
| `skill/` | skill patch | `skill/v1.7.1` |
| `regression/` | 回归 | `regression/06-quick-bugfix` |
| `release/` | 发布 | `release/v1.8` |
| `hotfix/` | 紧急 | `hotfix/nullref-on-empty` |

---

## 3. full / quick 与分支映射

工作线模式与分支类型的对应关系：

| 工作线模式 | 分支前缀 | 说明 |
|:---|:---|:---|
| full | `feature/<task-id>` | SDD + Conflict Gate + 4 份报告 + metrics |
| quick | `fix/<task-id>` | WorklineSummary + metrics-lite |
| — | `docs/<topic>` | 仅文档，无 Gate |
| — | `skill/<version>` | Skill patch，走 regression 验证 |
| — | `regression/<case-id>` | 回归用例开发 |

Hermes 在 Mode Router 判断后，自动选择对应分支前缀。

---

## 4. 标准任务流程

```
                     ┌──────────────┐
                     │  Task 创建    │
                     │  (用户/系统)  │
                     └──────┬───────┘
                            │
                     ┌──────▼───────┐
                     │  Mode Router │
                     │  full/quick  │
                     └──┬─────────┬─┘
                        │         │
              ┌─────────▼─┐  ┌───▼──────────┐
              │ full mode  │  │ quick mode    │
              │            │  │               │
              │ git checkout│ │ git checkout   │
              │ -b feature/ │ │ -b fix/        │
              │   <task-id> │ │   <task-id>    │
              │            │  │               │
              │ Workline   │  │ Workline      │
              │ Tasks 1..N │  │ Fix → Commit  │
              │            │  │               │
              │ git commit │  │ git commit    │
              │ per task   │  │               │
              └──────┬─────┘  └──────┬────────┘
                     │               │
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │  PR/MR 到     │
                     │  develop      │
                     │  (审查)       │
                     └───────┬───────┘
                             │
                     ┌───────▼───────┐
                     │  Merge 到     │
                     │  develop      │
                     └───────────────┘
```

---

## 5. quick 流程

### 步骤

```bash
# 1. 从 develop 创建修复分支
git checkout develop
git pull
git checkout -b fix/<task-id>

# 2. 执行修复（Codex 或 Agent）
# ...

# 3. 提交（含 Workline 产物）
git add <modified-files>
git add tasks/<task-id>/WorklineSummary.md
git add tasks/<task-id>/metrics-lite.yaml
git commit -m "fix: <description>"

# 4. PR 到 develop
# PR body 使用模板（见第 7 节）

# 5. 审查通过 → Merge
```

### 产出检查

- [ ] 只修改目标文件，无无关变更
- [ ] WorklineSummary.md 存在且完整
- [ ] metrics-lite.yaml 存在且字段完整
- [ ] commit message 标注 mode: quick
- [ ] PR body 附 evidence

---

## 6. full 流程

### 步骤

```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull
git checkout -b feature/<task-id>

# 2. 执行工作线
# Phase 0-3.5: Hermes 产出 TaskSpec + SDD + ConflictReport
git add tasks/<task-id>/TaskSpec.md
git add tasks/<task-id>/SDD.md
git add tasks/<task-id>/ConflictReport.md
git commit -m "sdd: <task-id> — TaskSpec + SDD + Conflict Report"

# Phase 4-5: Codex 编码 + Build/Test
git add <modified-source-files>
git commit -m "feat: <task-id> — <description>"

# Phase 7: Claude Code 审查
git add tasks/<task-id>/REVIEW.md
git add tasks/<task-id>/ChangedFiles.md
git add tasks/<task-id>/TestReport.md
git add tasks/<task-id>/RiskReport.md
git commit -m "review: <task-id> — APPROVED/NEEDS_FIX"

# Phase 8: 验证 + Metrics + Retro
git add tasks/<task-id>/metrics.yaml
git add tasks/<task-id>/retrospective.md
git commit -m "test: <task-id> — user verified, metrics recorded"

# 4. PR 到 develop
# PR body 使用模板（见第 7 节）

# 5. 审查通过 → Merge
```

### 产出检查

- [ ] TaskSpec.md
- [ ] SDD.md
- [ ] ConflictReport.md（PASS 或 BLOCKED with evidence）
- [ ] REVIEW.md（含审查结论）
- [ ] ChangedFiles.md
- [ ] TestReport.md（含真实验证结果）
- [ ] RiskReport.md
- [ ] metrics.yaml（user_verified=true）
- [ ] retrospective.md
- [ ] 每个 task commit 独立，commit message 标注 mode: full

---

## 7. PR / MR 规范

### PR 模板

```markdown
## What changed
<简要描述修改内容，1-3 行>

## Why
<修改原因>

## Workline mode
- [ ] full
- [ ] quick
- Mode: <full/quick>
- Workline version: <v1.x.x>

## Evidence
- Commit range: <hash>..<hash>
- Reports: tasks/<task-id>/
- Files changed: <N> files

## Tests
- [ ] Build passed
- [ ] Unity Play verified
- [ ] No regressions in existing features

## Risks
- <none / 列出风险>

## Screenshots
<if UI changes — attach screenshots>

## Reviewer Checklist
- [ ] Branch naming matches task type (feature/fix/docs)
- [ ] No unrelated files changed
- [ ] Workline reports present and complete
- [ ] Metrics recorded
- [ ] Scope matches SDD (full) or task description (quick)
```

---

## 8. Merge 规则

| 规则 | 说明 |
|:---|:---|
| 禁止直接 push main | main 只接受 release/hotfix merge |
| develop 合入必须经过 PR/MR | 所有 feature/fix/docs/skill/regression 分支 |
| PR 审查通过后才能 merge | 审查者检查 PR template checklist |
| 禁止 force push 公共分支 | main / develop 不允许 `--force` |
| Squash merge 推荐 | 保持 main/develop 历史干净 |

### Merge 策略

```
feature → develop:  squash merge（功能为原子单位，分支内证据链由 PR/MR 和任务报告保留）
fix → develop:      squash merge（修复为原子单位）
release → main:     merge commit（保留 full history）
hotfix → main:      merge commit（保留 full history）
main → develop:     merge commit（同步 hotfix 回 develop）
```

full 分支内允许分阶段 commit（SDD → 实现 → 审查 → 验证），保留证据链。合入 develop 时推荐 squash merge，将多次 commit 压缩为一个原子功能提交——分支内的完整证据链由 PR/MR body 和 `tasks/<task-id>/` 目录保留。

---

## 9. Release 流程

```
develop ──────────────────────────────────────────────
  │
  │  准备发布
  ▼
git checkout -b release/v1.8 develop
  │
  │  QA / Unity Verify / Regression
  │  (只修 Bug，不加新功能)
  │
  ▼
git checkout main
git merge release/v1.8          # merge commit
git tag v1.8-stable
  │
  │  同步回 develop
  ▼
git checkout develop
git merge main                  # merge commit
```

### Release 验收清单

- [ ] Regression 全量通过（当前 6 个用例）
- [ ] 至少 1 个真实 full 任务通过
- [ ] 至少 1 个真实 quick 任务通过
- [ ] 架构文档更新（如有架构变更）
- [ ] Git status clean
- [ ] Tag message 含验证证据摘要

---

## 10. Hotfix 流程

```
main ────────────────────────────────────
  │
  │  紧急 Bug
  ▼
git checkout -b hotfix/<issue-id> main
  │
  │  quick 模式修复
  │  WorklineSummary + metrics-lite
  │
  ▼
git checkout main
git merge hotfix/<issue-id>      # merge commit
git tag v1.7.1                   # patch version
  │
  │  同步回 develop
  ▼
git checkout develop
git merge main                   # merge commit
```

### Hotfix 规则

- 从 main 分出，不能从 develop 分出
- 修复后合并到 main + tag（patch 版本号）
- 必须合并回 develop，避免下次 release 丢修复
- 使用 quick 模式，产出 Lite 报告

---

## 11. Tag 规则

### Tag 命名

```
v<major>.<minor>.<patch>[-<modifier>]

示例：
  v1.7.0          ← 正式版本
  v1.7-stable     ← stable 标记（可与 minor 版本重叠）
  v1.7.1          ← hotfix patch
  v2.0.0-beta     ← 预发布
```

### Stable Tag 验收标准

| 条件 | 说明 |
|:---|:---|
| Regression passed | 所有回归用例通过（当前 6 个） |
| Real quick passed | 至少 1 个真实 quick 任务通过 |
| Real full passed | 至少 1 个真实 full 任务通过 |
| Architecture doc updated | `docs/WORKLINE_ARCHITECTURE_V<x.y>_STABLE.md` 存在 |
| Git status clean | 无未提交变更，无未追踪文件（未追踪文件必须 commit / archive / ignore / 删除，不允许模糊保留） |

### Tag Message 格式

```
v1.7-stable

- Introduce minimal full/quick mode routing
- Keep Conflict Gate as the only active hard gate
- Add quick-mode WorklineSummary and metrics-lite
- Validate regression 06 quick bugfix
- Validate one real quick bugfix
- Validate one full feature task
- No skill directory split
- No LangGraph/LangChain runtime dependency
```

---

## 12. Rollback 规则

### 原则

| 规则 | 说明 |
|:---|:---|
| 优先 git revert | 不直接 reset 公共分支（main / develop） |
| 记录回滚原因 | commit message 说明 why 和 affected commits |
| 回滚后验证 | 跑回归套件确认未引入新问题 |
| 复盘记录 | retrospective 记录回滚原因和预防措施 |

### Rollback 流程

```bash
# 1. 确定要回滚的 commit
git log --oneline main

# 2. Revert 普通 commit（保留历史）
git revert <commit-hash>

# 如果需要自定义 message：
git revert --no-commit <commit-hash>
git commit -m "rollback: <reason> — reverts <commit-hash>"

# 如果是 revert merge commit：
git revert -m 1 <merge-commit-hash>

# 3. 验证
# 跑 regression

# 4. 记录
# 在 retrospective 中记录回滚原因
```

### 禁止操作

- `git reset --hard` 到公共分支（main / develop）
- `git push --force` 到公共分支
- 不回滚直接覆盖修复（hotfix 也要走正常流程）

---

## 13. 与 v1.7-stable 的关系

本文件是 **v1.7-stable 的协作适配层**，不改变任何核心机制：

| 核心机制 | 状态 |
|:---|:--:|
| Mode Router（full / quick） | 不变 |
| Conflict Gate | 不变 |
| Gate 执行规则 | 不变 |
| Lite 报告 | 不变 |
| Metrics 系统 | 不变 |
| Skill 单文件结构 | 不变 |
| LangGraph 决策 | 不变 |

Git Workflow 只是把现有的 `git commit` 操作组织成标准的分支/PR/Release 流程——让工作线的 Git Evidence Layer 从"记录"升级为"流程"。

---

## 附录：分支速查

```bash
# 开始 full 任务
git checkout develop && git pull && git checkout -b feature/<task-id>

# 开始 quick 任务
git checkout develop && git pull && git checkout -b fix/<task-id>

# 开始文档
git checkout develop && git pull && git checkout -b docs/<topic>

# 开始回归用例开发
git checkout develop && git pull && git checkout -b regression/<case-id>

# 查看所有活跃分支
git branch -a

# 查看 release 标签
git tag -l 'v*'
```
