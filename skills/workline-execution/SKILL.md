---
name: workline-execution
description: "Execute workline methodology on real projects — analysis, SDD, implementation, review, verification"
version: 1.6.0
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

The SDD must include a **"非目标 / 本次不做"** section that explicitly scopes what the Agent should NOT touch:

```markdown
## 非目标 / 本次不做

本次任务明确不处理以下内容：

- 不重构无关模块
- 不修改未列入任务范围的系统
- 不顺手优化架构
- 不引入新的框架或依赖
- 不修改公共协议、公共接口或全局配置，除非 SDD 明确允许
- 不处理与当前 Bug / 当前需求无直接关系的问题

如 Agent 认为必须修改以上内容，必须先在 REVIEW.md 中说明原因，并等待人工确认。
```

Why: Without explicit scope boundaries, coding agents default to "improving" everything they see. The "非目标" section is the contract that limits their reach — and gives the review phase a concrete reference to flag [VIOLATION: scope-creep].

### Phase 3.5b: Conflict Gate — Requirement Feasibility Check

**BEFORE delegating to Codex**, check the SDD for internal contradictions. This is the Harness' "demand gatekeeper" — it prevents impossible tasks from reaching the execution layer.

Checklist — every item must be assessed:

```yaml
1. 功能目标之间是否冲突:
    例: "收藏状态持久化" vs "关闭后不保存"

2. 功能目标与非目标是否冲突:
    例: "点击收藏按钮" vs "不修改 UI Prefab / 不新增 UI 控件"

3. 验收标准与约束是否冲突:
    例: "输出 SDD/REVIEW 等报告文件" vs "不新增任何文件"

4. 持久化需求是否有合法存储位置:
    检查: ItemData字段 / 新数据结构 / PlayerPrefs / 文件存储 / 后端
    如果全部被禁 → 持久化不可执行

5. UI 交互需求是否有合法 UI 修改权限:
    检查: Prefab修改 / 动态创建控件 / 复用现有元素
    如果全部被禁 → UI 需求不可执行

6. 排序/筛选/状态需求是否允许修改对应逻辑:
    检查: RefreshList / OnFilterClicked / 排序方法
    如果被禁 → 排序需求不可执行

7. 输出文件要求是否与 "不新增任何文件" 冲突:
    约束是 "任何文件" 还是 "业务代码文件"？
    如果是前者 → 报告输出冲突
```

If ANY fatal conflict is found:

| Action | Detail |
|:---|:---|
| Status | Mark as **BLOCKED** |
| delegate_task | **DO NOT invoke** Codex or Claude Code |
| Output | `ConflictReport.md` — which requirements conflict, why they cannot coexist |
| Output | `ClarificationQuestions.md` — what the Mentor must answer before unblocking |
| Next | Wait for Mentor response. Do NOT proceed to Phase 4. |

If no conflicts: proceed to Phase 4 normally.

**Why**: A workline that blindly executes any task is a script. A workline that detects impossible demands and blocks execution is an engineering system. This gate was validated on 2026-06-21 with the backpack-favorite-sort conflict test: 4 fatal conflicts detected, Codex NEVER invoked.

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

**For Unity projects (non-ET6)**: Before first compile, check `Packages/manifest.json` for `com.unity.ugui`. If missing and the code uses `UnityEngine.UI` (Text, Image, Button, Canvas), add `"com.unity.ugui": "1.0.0"` to the dependencies. Skip check for ET6/HybridCLR projects — they use their own UI framework (DlgSystem, not UGUI).

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

    ## 无关文件修改检查

    - [ ] Agent 是否只修改了 SDD 允许范围内的文件？

    ## 报告完整性检查（审查前必须确认）

    - [ ] REVIEW.md 存在
    - [ ] ChangedFiles.md 存在
    - [ ] TestReport.md 存在
    - [ ] RiskReport.md 存在
    - [ ] 如果缺任何一份 → NOT READY，先补全再审查
    - [ ] 是否存在顺手格式化、顺手重构、顺手优化？
    - [ ] 是否修改了与当前任务无关的模块？
    - [ ] 是否修改了公共接口、协议、配置、资源路径？
    - [ ] 是否新增了未声明依赖？
    - [ ] 是否删除了未声明文件？
    - [ ] 如果存在范围外修改，是否在 REVIEW.md 和 ChangedFiles.md 中解释？

    处理规则：
    - 如果 Agent 修改了无关文件 → 不允许直接通过审查
    - 必须要求 Agent 解释修改原因
    - 如果修改没有必要 → 要求回滚
    - 如果修改确实必要 → 必须补充到 SDD 范围说明中

    OUTPUT — produce ALL FOUR files in tasks/review/:

    1. REVIEW.md
    ```markdown
    # REVIEW.md

    ## 审查结论
    - [ ] 通过
    - [ ] 需要修复
    - [ ] 需要人工确认

    ## 本轮任务目标
    [简述本轮任务要解决的问题]

    ## 发现的问题
    | 编号 | 问题 | 严重程度 | 是否已修复 |
    |---|---|---|---|
    | 1 |  | Blocker / Major / Minor | 是 / 否 |

    ## 修复摘要
    [简述 Agent 做了哪些修复]

    ## 是否存在越权修改
    - [ ] 否
    - [ ] 是，说明如下：

    ## 是否需要人工确认
    - [ ] 否
    - [ ] 是，原因：
    ```

    2. ChangedFiles.md
    ```markdown
    # ChangedFiles.md

    ## 修改文件列表
    | 文件 | 修改类型 | 修改原因 | 是否属于 SDD 范围 |
    |---|---|---|---|
    | path/to/file.cs | 新增 / 修改 / 删除 |  | 是 / 否 |

    ## 关键修改说明
    ### 1. 文件：xxx.cs
    修改内容：...
    修改原因：...

    ## 无关文件检查
    - [ ] 未修改无关文件
    - [ ] 修改了无关文件，说明如下：

    ## 需要人工重点查看的文件
    ```

    3. TestReport.md
    ```markdown
    # TestReport.md

    ## 测试环境
    - 项目 / 分支 / 运行方式 / 测试时间

    ## 执行的验证
    | 验证项 | 结果 | 说明 |
    |---|---|---|
    | 编译检查 | 通过 / 失败 / 未执行 |  |
    | 启动检查 | 通过 / 失败 / 未执行 |  |
    | 相关功能检查 | 通过 / 失败 / 未执行 |  |
    | 日志 Error 检查 | 通过 / 失败 / 未执行 |  |
    | 回归风险检查 | 通过 / 失败 / 未执行 |  |

    ## 失败项
    | 失败项 | 错误信息 | 处理方式 |
    |---|---|---|

    ## 未执行项说明
    [列出为什么某些测试没有执行，禁止伪造测试结果]

    ## 最终测试结论
    - [ ] 通过
    - [ ] 未完全通过
    - [ ] 无法验证，需要人工介入
    ```

    4. RiskReport.md
    ```markdown
    # RiskReport.md

    ## 本轮风险等级
    - [ ] 低 / [ ] 中 / [ ] 高

    ## 主要风险
    | 风险 | 影响范围 | 可能后果 | 建议处理 |
    |---|---|---|---|

    ## 架构风险
    - 是否修改模块边界 / 引入新依赖 / 影响公共接口 / 影响协议/配置/资源加载

    ## 运行时风险
    - 是否可能引入空引用 / 影响生命周期 / 影响热更/HybridCLR / 影响性能

    ## 需要人工确认的风险
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

After verification, produce an Obsidian retrospective note. Include:

```markdown
## 面试表达

本次任务可以这样表达：

> 我在实现 / 修复这个功能时，先通过 SDD 明确了任务范围、非目标和验收标准，避免 AI Agent 越权修改无关模块。
>
> 在 Agent 执行后，我不会直接相信它的输出，而是要求它提供 ChangedFiles、TestReport 和 RiskReport，分别说明改了哪些文件、如何验证、还有哪些风险。
>
> 对于 Unity / ET6 / HybridCLR 项目，我会特别关注生命周期、热更边界、公共接口、资源路径和运行时日志，避免 AI 只追求"能编译"而忽略客户端工程风险。

## 可复用经验

- 本次遇到的问题：
- 下次遇到类似问题应优先检查：
- 可以沉淀为 Harness 规则的内容：
- 可以加入 SDD 模板的内容：
- 可以作为面试案例讲述的点：
```

### 8b. 产出结构化 metrics

After each task completes, produce `retrospectives/<task-id>-metrics.yaml` in the Harness repo:

```yaml
task: <任务名>
workline_version: <版本号>
started_at: <ISO时间>
phases:
  p0_gate:
    passed: true
  p4_implementation:
    delegated: true
    subagent_calls: 0
    subagent_interruptions: 0
  p5_compile:
    initial_errors: 0
    fix_loops: 0
  p7_review:
    initial_verdict: APPROVED
    reports_missing: 0
    rework_loops: 0
    bugs_found_by_review: 0
    final_verdict: APPROVED
  p8_verify:
    user_verified: true
    bugs_found_by_user: 0
violations:
  herm_write_code: 0
  skip_review: 0
  skip_audit: 0
  scope_creep: 0
total_duration_minutes: 0

mentor_verified:
  sdd_review_passed: false
  phase8_user_check_passed: false
  clarification_valid: false

evidence:
  commit_hash: ""
  outputs: []
  screenshots: []
```

This file enables Level 2 — metric-driven evolution. After 3+ tasks with metrics, Hermes can:
- Compare compile_errors trends (is Phase 5 getting better?)
- Detect if violations are recurring (same violation → escalate constraint)
- Identify slow phases (optimize the bottleneck)
- Decide which GATEs are mature enough to downgrade to auto-check

The metrics file goes alongside the markdown retrospective. Both are committed to the Harness repo.

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
