# 管线进化规则

## 怎么改 Skill

```
1. 任务运行中 → 触发了 Skill 未覆盖的断裂
2. 复盘记录 → retrospectives/YYYY-MM-DD-<任务>.md
3. 从复盘提取 → 断裂点 + 证据 + 建议约束
4. patch skill → git checkout -b exp/<name>
5. 写约束 → 只修断裂点，不加多余约束
6. 下次任务验证 → 有效 → merge + tag
                   无效 → git revert
```

## commit 格式

```
patch: <skill名> - <原因>

证据: 复盘/2026-06-21-ET6.md §二.P0
```

## 不做的

- 不提前加固（问题没发生不加约束）
- 不重写（patch 不是 rewrite，改最小范围）
- 不猜测（复盘证据优先于想象）
- 不合并提交（每次 patch 一个独立 commit）

## 稳定版本

```bash
# 签稳定版
git tag v1.9-stable -m "CI + regression 10/10 + Git workflow execution evidence"

# 回退
git checkout v1.8-stable
```

## 实验版本

```bash
# 实验性改进
git checkout -b exp/delegate-enforcement
# ... 改 skill ...
# 下次任务验证
# 通过 → git checkout main && git merge exp/delegate-enforcement && git tag
# 失败 → git branch -D exp/delegate-enforcement
```

## 同步到运行时目录

改完 skill 后，必须同步到 `~/.hermes/skills/` 才能被 Hermes 加载：

```bash
# 从 harness repo 同步到运行时目录
cp -r skills/<name> ~/AppData/Local/hermes/skills/<name>/
```

**如果忘记同步**：下次任务加载旧版本 skill，管线退化到上一个 tag。commit 后立即 cp。

## CI

```bash
# 本地运行 checker
python tests/harness_check/run_harness_check_cases.py

# CI 自动触发：push / PR / workflow_dispatch
# 配置文件：.github/workflows/workline-check.yml
```

## 当前版本

- v1.10 intake trial：requirement intake (intake → breakdown → handoff)
- v1.9-stable：CI + regression 10/10 + Git workflow execution evidence
- v1.8-stable：minimal harness checker
- v1.7-stable：workline core freeze + mode router

---

## File Placement Rules

> 来源：`docs/WORKLINE_REPOSITORY_STRUCTURE.md`

新增文件前必须先查 `docs/WORKLINE_REPOSITORY_STRUCTURE.md`。

规则：

1. **不确定位置时开 placement decision** — 不得自行猜测
2. **不允许空建 future-only 目录** — `observability/`、`skills/workline-evaluation/`、`skills/workline-observability/` 只在实现启动后创建
3. **不允许把任务产物放进 `docs/`** — WorklineSummary、metrics-lite 属于 `tasks/`
4. **不允许把 runtime skill 当作普通文档改** — `skills/` 是运行时层
5. **不允许为了美观移动 stable evidence** — 迁移必须单独立项、单开分支、跑 CI
