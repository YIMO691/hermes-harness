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
git tag v2.0-stable -m "Git集成 + 硬约束 + 审查GATE，通过 ET6 全量验证"

# 回退
git checkout v1.0-stable
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
