# 管线演进规则

> v1.11-office-onboarding-stable

## 核心原则

任何修改都必须保持：

```
v1.10 canonical baseline
+
v1.11 Office Onboarding Safety Layer
```

不推翻既有基线。personal-lab 下行为必须与 v1.10 完全一致。

---

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

## Skill 同步铁律（GAP #4 修复）

```
1. 修改 SKILL.md 必须开分支
2. 修改前确认 repo skill 与 runtime skill 一致
3. 不能只改 runtime skill 不回写 repo
4. 不能只改 repo skill 不同步 runtime
5. 修改后必须执行审计（Phase 6.x 兼容性审计）
6. 如果发现 runtime→repo 分裂，先做 baseline sync 再继续
```

**教训**：v1.8/v1.9/v1.10 曾出现 runtime skill 更新但未回写 repo 的问题（GAP #4），导致 repo 停留在 v1.7。以后任何 skill 规则升级，repo 和 runtime 必须同步。

从 repo 同步到运行时：

```bash
cp -r skills/<name> ~/AppData/Local/hermes/skills/<name>/
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

## Office Mode 修改规则

任何涉及以下内容的改动，都必须走 `regression/office_onboarding/` 回归用例：

- safe-note / office-lite / full-harness / personal-lab
- Company Policy Gate / Sensitive Data Gate / Action Permission Gate / Persistence Gate / Mode Switch Gate
- Codex 权限边界
- ChatGPT 信息流规则
- Obsidian 工作 Vault 保存规则

## MANUAL_VERIFY 规则

`regression/office_onboarding/` 下的用例全部标记为 `[MANUAL_VERIFY]`。

- 不能把它们伪装成自动化测试通过
- 如果未来要自动化，必须单独设计 checker，不得直接改状态
- 每次修改涉及 Office Mode/Gate 时，必须手动验证这些 case

## 封版规则

稳定版本必须：

- [ ] Phase 9 最终审计 PASS
- [ ] Release notes 已生成
- [ ] git status clean
- [ ] stable tag 已打
- [ ] 零敏感信息
- [ ] CI 通过

```bash
# 签稳定版
git tag v1.XX-stable -m "..."

# 回退
git checkout v1.XX-stable
```

## 禁止事项

```
不允许跳过 Company Policy Gate
不允许绕过 Sensitive Data Gate
不允许把公司内容写入 reports/docs/templates
不允许让 Codex 默认接触公司项目
不允许让 ChatGPT 接收公司源码或内部文档
不允许空建 future-only 目录（observability/ 等）
不允许把任务产物放进 docs/
不允许为了美观移动 stable evidence
```

---

## 稳定版本历史

- `v1.11-office-onboarding-stable` — Office Onboarding safety layer (4 modes, 5 gates, 6 templates, 6 regression cases)
- `v1.9-stable` — CI + Regression 10/10 + Git Workflow
- `v1.8-stable` — Harness Checker
- `v1.7-stable` — Workline Core (Mode Router + Conflict Gate)

## File Placement Rules

> 来源：`docs/WORKLINE_REPOSITORY_STRUCTURE.md`

新增文件前必须先查 `docs/WORKLINE_REPOSITORY_STRUCTURE.md`。
不确定位置时开 placement decision — 不得自行猜测。
