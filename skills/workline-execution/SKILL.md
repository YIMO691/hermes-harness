---
name: workline-execution
description: "Execute workline methodology on real projects — analysis, SDD, implementation, review, verification"
version: 1.3.0
tags: [workline, sdd, agent-pipeline, et6, unity]
platforms: [windows, linux, macos]
triggers:
  - "开始工作线"
  - "按工作线执行"
  - "workline"
  - "拆分需求"
  - "独立重写"
  - "测试题"
  - "按照XX模块范式完成"
---

# Workline Execution

Execute the workline methodology for real projects: understanding requirements → analysis → SDD → independent implementation → compilation → review → verification.

## When to Use

- Game company coding tests that require independent reimplementation of reference modules
- Any task where you must understand a framework's pattern and write matching code
- Projects where the existing code is a previous attempt that needs rewriting

## Skill Dependencies (MUST LOAD FIRST)

Before executing ANY phase, load these skills. The workline's agent contracts depend on them:

```python
skill_view(name='codex')                        # Codex invocation patterns + image analysis
skill_view(name='subagent-driven-development')   # delegate_task patterns + 2-stage review
skill_view(name='claude-code')                   # Claude Code review invocation
```

**Why**: Without these loaded, Hermes defaults to writing code itself — see retrospective `2026-06-21-ET6.md §P0`. The constraint "Hermes does NOT write code" is in this skill, but the *how* (delegate_task patterns, codex exec flags, Claude Code prompts) lives in the dependency skills. Load them or the constraint is toothless.

If a dependency skill is unavailable: mark `[FALLBACK]` and Hermes handles that phase directly. But loading must be attempted first.

## Core Principles

1. **Compile before review.** API name mismatches are systematic. The compiler is the first reviewer.
2. **Hermes schedules, Codex writes, Claude Code reviews.** Hermes does NOT write code. Delegate coding to Codex (via `delegate_task` or `codex exec`). Hermes' job: analyze, plan, verify compilation, coordinate agents.
3. **Claude Code review is mandatory after every compilation pass.** Even 0-error builds. It catches pattern consistency, null safety, IsCan+Do completeness, and Handler coverage — things the compiler never will.
4. **Git is the harness backbone.** Every coding session starts with `git init` (if not already a repo) and a feature branch. Every atomic change is committed. Claude Code reviews run on `git diff`, not full files. The `.bak` file pattern is a symptom of missing git — if you see `.bak` files, `git init` immediately.

## Workline Phases

### Phase 0: GATE 0 — Environment Readiness Check

**MANDATORY.** Before any document reading or analysis, verify the environment can actually execute the workline.

Checklist — every item must be confirmed before proceeding:

```yaml
工程可达:
  - 确认项目根目录绝对路径
  - cd 到项目根目录 && pwd 验证

编译工具:
  - dotnet --version 确认可用
  - 确认 Server.sln 或等价入口文件存在

服务端:
  - 确认服务端启动脚本存在
  - 确认服务端口配置（默认 20001）

GM 权限:
  - 确认 GM 账号可用（数值面板 → 用户是否是 = 1）

Agent 可用性:
  - 确认 codex CLI 可用（codex --version）
  - 确认 delegate_task 工具可用
  - 确认 Claude Code / gh CLI 可用（claude --version 或 gh --version）

项目状态:
  - git status 确认工作区（如果是 git repo）
  - 如果存在 .bak 文件 → git init 立即执行
```

Output: `tasks/doing/ENV_CHECK.md` with each item marked ✅ or ❌.

**Items marked ❌ = blocking.** Do not proceed to Phase 1 until resolved or explicitly waived by the user.

### Phase 1: Full Document Absorption

Read EVERY document provided. Do not skip. This includes:
- Framework learning notes
- Coding standards
- UI framework docs
- File structure docs
- Reference module requirement docs (both client and server)
- Reference module source code (all layers: Model, Hotfix, View)

### Phase 2: ANALYSIS

Output: `tasks/doing/PROJECT-ANALYSIS.md`

Contents:
- Module architecture map (what exists, what needs to be built)
- Reference module pattern extraction
- Differences between reference and target modules
- Configuration table dependencies
- Protocol definitions needed

### Phase 3: Design Documents

Reference the exact format of the PROVIDED reference documents. Match:
- Section structure (H2/H3 levels)
- Table formats
- Code block styles
- Naming conventions

For each module, produce:
1. Client design doc (UI list, data flow, event handling, protocols)
2. Server design doc (protocols, business logic, config tables)

**Mentor gate**: User reviews and approves design docs before proceeding.

### Phase 3.5: Requirements Decomposition (SDD)

After design docs are approved, produce a concrete task breakdown. Output: `tasks/doing/SDD-{项目}-需求拆分.md`

Structure (see `references/sdd-template.md`):
1. **Code inventory** — list every existing file, mark ✅/❌
2. **Gap analysis** — what's missing per layer (Model/Hotfix/HotfixView)
3. **Dependency-ordered tasks** — each with file list, content summary, verification criteria
4. **Dependency graph** — ASCII tree showing task ordering
5. **Acceptance checklist** — checkboxes for each verification gate

Key rule: **Task 1 must be the lowest-level dependency** — typically Model layer data definitions that Hotfix code references. If Hotfix code references a Component that doesn't exist, that's Task 1.

### Phase 4: Independent Implementation

**CRITICAL — Agent division of labor. Hermes does NOT write code in this phase.**

**Step 0: Git setup (mandatory, before any code is written)**

```bash
# If project is not a git repo yet
cd <project_root> && git init && git add -A && git commit -m "initial: project baseline"

# Create feature branch
git checkout -b feature/<module-name>

# Verify
git status   # must show clean working tree
```

Why: `.bak` files scattered across the project are evidence of missing version control. Git gives you diff-based Claude Code review, atomic rollback, and an immutable audit trail. Without it, the Harness cannot enforce any other gate — there's no way to see what changed or who changed it.

**After each coding task completes:**
```bash
git add -A && git commit -m "<task>: <description>"
```

**After compilation passes:**
```bash
git diff feature/<module-name> --stat   # verify change scope
```

The Claude Code review (Phase 7) runs against `git diff feature/<module-name>`, not against raw files — this makes review scope-relevant and prevents review fatigue.

The correct execution model:
1. Hermes splits the SDD tasks into self-contained work items
2. Hermes delegates each task to Codex via `delegate_task` (single task) or `delegate_task(tasks=[...])` (parallel batch)
3. Codex writes the files and returns a summary
4. Hermes verifies: reads the written files, checks against design doc
5. After all tasks complete, Hermes initiates compilation (Phase 5)
6. After compilation passes, Hermes delegates review to Claude Code (Phase 7)

Why: Hermes writing code itself creates single-point-of-failure — no peer review, pattern drift accumulates, and the agent coordination chain breaks. The value of the workline is the multi-agent quality gate, not raw code generation speed.

**DO NOT copy existing code.** Read ONLY reference module source code, then write.

**CRITICAL — Pre-coding gate**: Before writing ANY file, check what already exists in the deployed ET6 project (not the test workspace). Previous sessions may have already deployed files. Use `find`/`search_files` on the ET6 project root to verify each file's existence and content. Do not write a file that already exists in the project — skip it and move to the next task. See `references/et6-project-paths.md` for the exact directory structure.

If the project already has ALL files (Model, Hotfix, ModelView, HotfixView), the task is COMPILATION, not coding. Skip directly to Phase 5.

**Before writing Model files**: if Hotfix code exists but Model Component files are missing, reverse-engineer the fields first. See `references/model-reverse-engineering.md` for the subagent prompt template — never guess dictionary key types or Bson attributes.

Server:
- `PlayerXxxComponentSystem.cs` — IsCan + Do pairs, lifecycle, property calculations
- `PlayerXxxComponentNetLogic.cs` — Handler chain (C2G → validate → consume → execute → respond)
- `PlayerXxxComponentEvent.cs` — lifecycle events (OnCreate, OnExportLoginData, OnExportDBData)

Client (if needed):
- `DlgXxxSystem.cs` — UI refresh logic, click handlers
- `DlgXxxEvent.cs` — UI lifecycle

### Phase 5: Compilation Fix Cycle

1. Deploy code to project
2. `dotnet build` → collect all errors
3. Fix API mismatches systematically:
   - Method names: grep reference code for actual signatures
   - Field locations: check Proto/Config definitions
   - Error codes: grep ErrorCode.cs for available constants
4. Repeat until 0 errors

Common ET6 API traps:
- `ConfigCategory.Instance.GetMould(id)` NOT `GetXxxByXxxId(id)`
- `ConditionFactory.isCan(player, id)` NOT 3-arg overload
- `PlayerLoginInfo.XxxComponent` wraps fields, NOT direct properties
- `ErrorCode` enum is limited — only `ERR_SystemError` and `ERR_GoodsNotEnough`

### Phase 6: HybridCLR DLL Cache Fix

After source changes:
```bash
rm -rf Unity/Library/ScriptAssemblies/
rm -f Unity/Assets/Bundles/Code/Code.dll.bytes
rm -f Unity/Assets/Bundles/Code/MonoHotUpdate.dll.bytes
```
Then in Unity Editor: **Tools → Build → BuildCodeDebug**

### Phase 7: Mandatory Code Review (Claude Code)

**This step is NOT optional. Run even after 0-error builds.**

Use Claude Code to review the implementation against reference modules. Check:
- Pattern consistency (does every method follow reference module's IsCan+Do, Handler chain, DlgSystem pattern?)
- Null safety (every `GetComponent<T>()` checked? every `GetComponentNotNull<T>()` appropriate?)
- IsCan+Do completeness (every Do method has a corresponding IsCan? every IsCan called before its Do in Handler?)
- Handler try-catch coverage (every network handler wrapped in try/catch with `reply()` in catch?)
- API correctness (method names, field names match actual definitions — grep reference code to verify)

#### Claude Code Invocation

If project is in git (Phase 4 Step 0):
```bash
git diff feature/<branch> --stat                    # confirm scope first
git diff feature/<branch> > /tmp/review-diff.patch  # feed diff to Claude
```

Then delegate via `delegate_task`:
```python
delegate_task(
    goal="Review implementation for pattern consistency, null safety, IsCan+Do completeness, and handler coverage",
    context="""
    REVIEW SCOPE: git diff of feature branch (attached)
    REFERENCE MODULES: [list reference source files]
    DESIGN DOCS: [list client/server design docs]

    CHECKLIST:
    - [ ] Every Do method has a corresponding IsCan
    - [ ] Every Handler calls IsCan before Do
    - [ ] Every Handler has try/catch with reply() in catch
    - [ ] Every GetComponent<T>() checked for null (or uses GetComponentNotNull)
    - [ ] API names match reference module (grep verified)
    - [ ] No pattern deviations from reference module

    OUTPUT: REVIEW.md in tasks/review/
    Format:
    ```markdown
    # Code Review: <module>

    ## Critical Issues (blocking)
    - [ ] ...

    ## Warnings (should fix)
    - [ ] ...

    ## Passed Checks
    - [x] ...

    ## Verdict: APPROVED / NEEDS_FIX / REJECTED
    ```
    """,
    toolsets=['terminal', 'file']
)
```

#### Loop-back Rules

| Verdict | Action |
|:---|:---|
| APPROVED | Proceed to Phase 8 |
| NEEDS_FIX | Fix issues → re-compile (Phase 5) → re-review (Phase 7). Max 3 loops. |
| REJECTED | Escalate to user. Do not proceed. |

**If delegate_task is unavailable**: Hermes reads the diff, checks against the checklist manually, and produces REVIEW.md. Mark `[FALLBACK: herm-review]` in retrospective.

If Claude Code returns issues, fix them and re-review before proceeding to Phase 8.

### Phase 8: Verification

User does Unity Play + screenshots. Hermes handles file deployment, compilation, and review.

## References

- `references/model-reverse-engineering.md` — Subagent prompt template for extracting Model fields from Hotfix code
- `references/sdd-template.md` — Template for requirements decomposition documents
- `references/et6-project-paths.md` — Complete file inventory and directory structure of the ET6 test project
## ET6 GM Testing Workflow

When testing requires currency, materials, or rank conditions, use the GM panel (not manual gameplay). See `references/et6-gm-testing.md` for the complete guide including item IDs, test patterns, and boundary checklists.

Quick reference:

| 需求 | GM入口 | 操作 |
|:---|:---|:---|
| 加钻石（抽奖消耗） | 数值 | 普通钻石 → 20000 |
| 加神经解锁材料 | 添加物资 | ID=102, 数量=999 |
| 加神经升级材料 | 添加物资 | ID=101, 数量=999 |
| 满足解锁条件 | 境界 | 点高境界 → 升级 |
| 验证属性变化 | 属性 → 神经系统分类 | 看数值 |
| DNA参考 | DNA | 解锁/升级/升星按钮可用作比对 |

GM 面板入口：九宫格（数值/属性/OSS/背包/境界/DNA/Organ/日期/系统测试）。UIGMTest 按钮是空壳（代码注释掉了），不要用。

## Pitfalls

- **Hermes writing code defeats the workline** — when Hermes writes code instead of delegating to Codex, the multi-agent quality gate collapses. Codex → Claude Code → Hermes verify is the chain. Hermes directly writing code skips both Codex's speed advantage and Claude Code's review perspective. If code needs writing, use `delegate_task` or `codex exec`. The only exception: single-line fixes during compilation cycles.
- **Check if project already has code before writing** — the ET6 test package may already have complete implementations. Use `find` to verify what exists before creating new files. Wasted hours writing 17 files that were already deployed.
- **Don't modify existing code** — write independently from reference patterns only
- **Don't skip document reading** — all 14+ docs must be read
- **Compile before review** — prevents wasting review time on API name mismatches
- **HybridCLR caching** — source changes alone don't update Play mode; must run BuildCodeDebug
- **Don't guess APIs** — grep reference source for actual method names and signatures
- **Server.sln is at ET6 root, not in Server/ directory** — run `dotnet build Server.sln` from the ET6 project root, not from the Server subdirectory
- **Model reverse-engineering from Hotfix** — when Hotfix code exists but its referenced Model Component doesn't, DON'T guess the fields. Read every Hotfix/NetLogic/Event file that references the Component, extract all field accesses (self.m_dicXxx, self.m_nXxx), and deduce the exact dictionary key types, scalar types, and Bson attributes. See `references/model-reverse-engineering.md` for the subagent prompt template.
- **Standalone code compilation deferral** — when writing code to a standalone test directory (not the full ET6 project), the compilation cycle (Phase 5) MUST be deferred. Mark that task as "pending — user side" in the SDD and move on to the next dependency-independent task. Never fabricate compilation results.
- **Pre-coding project audit** — before writing ANY file in Phase 4, first run find/search_files on the ET6 project root to discover what is already deployed. Previous Hermes sessions may have already written and deployed files. If files exist, read them before deciding whether to overwrite or skip. Writing files that already exist wastes time and creates stale duplicates in the test workspace. When in doubt, the compiled project is the source of truth, not the test workspace.
- **Completion gate: count files against design doc** — before claiming a coding phase is complete, read the design doc's file list section (e.g. "六、文件清单" or "界面列表") and count your actual output against it. If the design doc lists 7 HotfixView windows but you've only written 3, DO NOT claim completion. Tell the user honestly what's missing and let them decide whether to proceed or fill gaps. Claiming completion when the design doc shows missing files will result in the user calling you out ("我不清楚你是否完成了所有需求").
- **dotnet build path** — `dotnet build Server.sln` must run from the ET6 project ROOT (where Server.sln lives), NOT from the Server/ subdirectory. Running from Server/ produces MSB1003 ("未包含项目或解决方案文件"). The ET6 root contains: Server.sln, Robot.sln, Server/, Unity/, Tools/, etc.
- **GM system reality** — the ET6 project ships with two GM panels: `UIGMRank` (functional, can set rank/level via C2Game_GmSetRank) and `UIGMTest` (empty stubs — 5 test buttons with all handler code commented out). The server has `PlayerBagComponent_GmLogic.cs` with `C2Game_GmBagAdd` for adding items, but requires `player.m_bGm == true`. When the user needs to test nerve/raffle with insufficient in-game resources, they need functional GM commands — do not assume the existing GM panel covers their needs. See `references/et6-gm-system.md`.
- **`.bak` files are a red flag** — if you see `*.cs.bak`, `*.cs.bak2` scattered in the project, it means previous sessions modified code without git. The project has no version control. Run `git init` before any coding. The `.bak` pattern means every change is a gamble with no rollback.
- **Git is not optional** — a workline without git is a Harness without a backbone. Without `git diff`, Claude Code reviews entire files (waste). Without `git reset`, every mistake requires manual `.bak` restoration (slow). Without `git branch`, parallel work on different modules is impossible. `git init` is Phase 4 Step 0 — not a nice-to-have, a prerequisite.
