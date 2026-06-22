# WORKLINE_ARCHITECTURE_V1.7_STABLE

> 定稿日期：2026-06-22
> 状态：v1.7-stable（已通过三项验证）
> 替代：原 v1.7-core-freeze 草案（5 模式 + 8 Gate + 6 目录 — 经思考线审查后废弃）
> 运行时实现：`skills/workline-execution/SKILL.md` v1.7.0

---

## 1. 当前定位

工作线当前是**游戏客户端功能交付 Harness 的核心骨架**，不是完整游戏客户端研发平台。

### 覆盖范围

```
需求 / Bug
→ full 或 quick 模式判断
→ SDD 或 Lite Plan
→ Conflict Gate
→ Agent 执行（Hermes 调度 / Codex 编码 / Claude Code 审查）
→ Build / Review / Unity Verify
→ Metrics / Retro
```

### 当前不覆盖

- 策划评审全流程
- UI/UX 专业评审
- 美术资源生产与导入规范
- 动画 / 特效 / 音频制作流程
- 多端兼容测试体系
- 完整 QA 缺陷管理
- 自动化 CI/CD
- 灰度发布 / 发版管理
- 线上监控与热修回滚
- 多人协作项目管理

### 与完整游戏客户端生命周期的关系

工作线覆盖的是"需求到可验证代码变更"这一段。其余阶段不是当前版本的失败，而是未来可通过专项 Gate、模板与工具链逐步补充的扩展方向。

---

## 2. v1.7-stable 最终架构

```
                       ┌────────────────┐
                       │   用户需求/Bug  │
                       └───────┬────────┘
                               │
                       ┌───────▼────────┐
                       │  Mode Router   │
                       │  full / quick  │
                       └───┬───────┬────┘
                           │       │
              ┌────────────▼─┐  ┌──▼─────────────┐
              │  full 模式    │  │  quick 模式      │
              │              │  │                 │
              │ ContextAudit │  │ Minimal Audit   │
              │ SDD          │  │ Error/Log Fix   │
              │ ConflictGate │  │ Build/Test      │
              │ Codex Impl   │  │ WorklineSummary │
              │ Build/Test   │  │ metrics-lite    │
              │ Claude Review│  └────────────────┘
              │ 4 Reports    │
              │ Unity Verify │
              │ Metrics/Retro│
              └──────────────┘
                       │
              ┌────────▼─────────┐
              │  Evidence Layer  │
              │  git diff/log    │
              │  reports         │
              │  metrics         │
              │  screenshots     │
              └────────┬─────────┘
                       │
              ┌────────▼──────────┐
              │  Skill Evolution  │
              │  pitfall → patch  │
              │  regression check │
              │  commit+evidence  │
              └───────────────────┘
```

### 关键设计决策

| 决策 | 说明 |
|:---|:---|
| 单文件 Workline Core | `skills/workline-execution/SKILL.md` v1.7.0，不拆分目录 |
| full / quick 双入口 | 模式路由，非 5 模式 |
| 1 个 active hard gate | Conflict Gate（已验证 4 次） |
| 7 个 placeholder gate | 已定义，断裂后激活 |
| Full / Lite 报告体系 | full=9 产物，quick=2 产物 |
| Build / Review / Metrics 证据闭环 | git + reports + metrics.yaml |
| 不引入 LangChain/LangGraph | 决策记录在 `references/langgraph-evaluation.md` |

---

## 3. Mode Router

### 设计原则

- Hermes 内部判断模式，不需要用户选择
- 在首次响应中声明模式判断（如 "Mode: quick — 单文件修复"）
- 不要求用户确认模式

### full 模式

**适用条件**：
- 新功能开发
- 多文件修改
- 涉及 UI + 数据状态
- 需要完整 SDD、审查、报告、metrics 的任务

**流程**：
```
ENV Check → Context Audit → Analysis → SDD → Conflict Gate
→ Codex Implementation → Build/Test → Claude Review → Unity Verify → Metrics/Retro
```

**产物**：
```
tasks/<task-id>/
├── TaskSpec.md
├── SDD.md
├── ConflictReport.md
├── REVIEW.md
├── ChangedFiles.md
├── TestReport.md
├── RiskReport.md
├── metrics.yaml
└── retrospective.md
```

### quick 模式

**适用条件**：
- 小 Bug 修复
- 单点修复 / 单文件或极少文件修改
- 不涉及架构决策
- 不涉及 UI 结构、协议、配置、资源、平台、热更

**流程**：
```
ENV Check → Minimal Context Audit → Error/Log Analysis → Codex Fix → Build/Test → WorklineSummary + metrics-lite
```

**产物**：
```
tasks/<task-id>/
├── WorklineSummary.md
└── metrics-lite.yaml
```

### Auto-upgrade 规则

如果 quick 模式任务在诊断后发现触及以下任一范围 → 自动升级为 full：
- UI（Panel / Prefab / UGUI 控件）
- 协议（Handler / 请求响应 / 状态同步）
- 配置（配置表 / 表 ID / 静态数据）
- 性能（Update / GC / 大量对象 / 资源加载）
- 资源（AssetBundle / Addressables / Prefab 引用）
- 平台（IL2CPP / 移动端 / 输入 / 分辨率）
- 热更（HybridCLR / DLL bytes / BuildCodeDebug）

---

## 4. review / retro / research 的定位

review / retro / research **不是独立模式**，不进入 Mode Router，不制造额外架构层。

它们是 **Action（动作）**，在 full 或 quick 流程中按需调用：

| Action | 对应能力 | 使用场景 |
|:---|:---|:---|
| review | Phase 7 Claude Code 审查（独立运行） | 用户说"审查这个 PR" |
| retro | Phase 8 复盘 + skill patch 建议 | 用户说"复盘上次任务" |
| research | C2 SDD/Plan 不编码 | 用户说"分析这个方案" |

调用方式：Hermes 直接路由到 Core Pipeline 的对应 Phase(s)，不创建新架构层。

---

## 5. Gate 架构

### Active Hard Gate（已实现，强制）

#### Conflict Gate

- **类型**: peer_agent / hard
- **触发**: 所有 full 模式任务
- **检查**: 7 项冲突维度
- **失败**: BLOCKED → 停止，等待 Mentor 澄清；Codex 零调用
- **验证**: 4 次（regression 04 + 3 次真实 full 任务）

### Future Gate Placeholders（已定义，未实现）

| Gate | 触发条件 | 激活条件 |
|:---|:---|:---|
| Unity UI Gate | 涉及 Panel/Prefab/UGUI/列表/UI 状态 | 任务因 UI 事件泄漏或空引用失败 |
| Network Gate | 涉及协议/Handler/请求响应/状态同步 | 任务因缺 try/catch 或未 reply 失败 |
| Config Gate | 涉及配置表/表 ID/静态数据 | 任务因配置字段名错误或缺 null-ID guard 失败 |
| Performance Gate | 涉及 Update/GC/大量对象/资源加载 | 任务因 foreach 分配或 GetComponent-in-Update 失败 |
| Asset Gate | 涉及 Resources/AssetBundle/Addressables/Prefab | 任务因缺资源路径或同步加载卡顿失败 |
| Platform Gate | 涉及移动端/IL2CPP/输入/权限 | 任务因 IL2CPP 不兼容或触摸处理缺失失败 |
| Hotfix Gate | 涉及 HybridCLR/热更 DLL/热更资源 | 任务因 DLL bytes 过期失败 |

### Gate 激活规则

**仅当真实任务中出现断裂点后，才允许从 placeholder 升级为 active gate。**

升级步骤：
1. 任务失败 → 复盘记录断裂点
2. 对照 placeholder gate 的触发条件 → 匹配成功
3. 复制 placeholder → 新 Gate section → 标记 active
4. 加入对应模式的 required gates
5. 新增回归用例
6. git commit with evidence

---

## 6. Gate 执行力规则

Gate 的阻断能力取决于**审查者的独立性**：

| 审查者独立性 | 允许的 failure_policy | 示例 |
|:---|:---|:---|
| `peer_agent` — 不同于被检查者的 Agent | `hard`（阻断流程） | Claude Code 审查 Codex 输出 |
| `automated` — 脚本/编译器 | `hard` | `dotnet build` 错误、`check_workline_outputs.py` |
| `human` — 用户确认 | `hard` | Mentor 审阅 Gate 3/7 |
| `same_agent` — 同一 Agent 自检 | `warning` 仅 | Hermes 自检 SDD 完整性 |

**原因**：如果检查者和被检查者是同一个 Agent，Gate 只是 checklist——Agent 有激励给自己通过。真正有牙齿的 Gate 必须有独立审查者或自动化证据。

---

## 7. 为什么不拆 skill 目录

当前保持 `skills/workline-execution/SKILL.md` 单文件结构（~700 行）。

**理由**：

1. **单人系统** — 不存在多人维护场景，拆分协调税无收益
2. **Gate 未独立演进** — 只有 1 个 active gate，其他 7 个是 placeholder
3. **Gate 无独立测试** — 当前回归测试覆盖整个 Pipeline，非单个 Gate
4. **单文件是原子单元** — 修改时不存在跨文件版本漂移
5. **600-700 行可管理** — 不是技术债务

**拆分时机**：
- 某个 Gate 有独立测试用例
- 某个 Gate 有独立触发逻辑，不依赖 Pipeline 上下文
- 多维护者场景出现
- 上述任一条件满足 → 单文件内节结构 → 确认独立演进 → 拆分

---

## 8. 为什么不接 LangChain / LangGraph

**当前结论：NOT NOW**

**理由**：

1. **当前瓶颈是流程稳定性，不是编排框架** — v1.7 已通过 Hermes + Codex + Claude Code + Git + Metrics 验证
2. **引入 LangGraph 会增加复杂度** — 抽象层数翻倍，无新增执行能力
3. **无实际断裂点需要图状态机** — 无 CONDITIONAL 多轮触发、无异步工作、无并行多工作线

**引入条件**（至少一个成立）：
- CONDITIONAL 回路触发 3+ 次/任务
- 用户异步工作（发起 → 离线 → 数小时后继续）
- 多工作线并行（2+ 任务需要状态隔离）
- 管线监控仪表盘需求
- Level 3 自动沉淀需要稳定状态机

决策记录：`skills/workline-execution/references/langgraph-evaluation.md`

---

## 9. 游戏客户端开发覆盖关系

### 当前覆盖段

```
需求 / Bug
→ 技术拆分
→ 编码实现
→ 编译验证
→ 代码审查
→ Unity Play 验证
→ 复盘沉淀
```

这对应游戏客户端开发中的 **"功能交付核心段"**。

### 当前未覆盖段

- 策划评审全流程
- UI/UX 专业评审
- 资源生产与导入规范
- 动画 / 特效 / 音频制作流程
- 多平台适配测试
- QA 缺陷生命周期
- 自动化 CI/CD
- 发布与回滚
- 线上监控

### 结论

当前工作线是**客户端功能交付核心段**，不是完整客户端研发平台。未覆盖段不是失败——是未来扩展方向。

---

## 10. v1.7-stable 验证证据

三项验证均在 BackpackDemo（Unity）上完成。

### Step 1 — regression 06 quick bugfix

| 项目 | 值 |
|:---|:---|
| 任务 | 恢复 TypeDropdown.onValueChanged 监听绑定 |
| 模式 | quick |
| Commit | `3aa5655` fix + `dc9b938` verify |
| 文件 | InventorySearchPanel.cs（1 行恢复） |
| 产物 | WorklineSummary.md + metrics-lite.yaml |
| Unity 验证 | ✅ 编译通过，dropdown 筛选正常 |
| 违规 | 0 |

### Step 2 — 真实 quick bugfix

| 项目 | 值 |
|:---|:---|
| 任务 | 删除 Start() 中重复的 RefreshList() 调用 |
| 模式 | quick |
| Commit | `886a39d` fix + `dc9b938` verify |
| 文件 | InventoryPanel.cs（1 行删除） |
| 产物 | WorklineSummary.md + metrics-lite.yaml |
| Unity 验证 | ✅ 编译通过，列表正常，筛选正常 |
| 违规 | 0 |

### Step 3 — full 功能任务

| 项目 | 值 |
|:---|:---|
| 任务 | BackpackDemo 背包物品收藏功能 |
| 模式 | full |
| Commit | `730adf6` feat + `e4cc1cb` fix + `e642186` review + `64bc3d9` verify |
| 文件 | ItemData.cs + InventorySlotView.cs + InventoryPanel.cs |
| 产物 | TaskSpec / SDD / ConflictReport / REVIEW / ChangedFiles / TestReport / RiskReport / metrics / retrospective |
| Unity 验证 | ✅ 8/8 验收项通过（1 个 UI 修正） |
| 违规 | 0（herm-write-code: 0, skip-review: 0, scope-creep: 0） |
| subagent_calls | 3 |

### 汇总

```
指标           Step 1    Step 2    Step 3
模式           quick     quick     full
耗时           ~1 min    ~1 min    ~5 min
scope-creep    0         0         0
herm-write     0         0         0
skip-review    0         0         0
user bugs      0         0         1
```

- quick 模式比 full 快 ~5x
- full 模式无退化
- 所有违规归零

---

## 11. 后续升级规则

v1.8 **不允许凭想象启动**。只有出现真实断裂点，才允许升级。

### 可触发 v1.8 的情况

- quick 被滥用导致漏审（metrics 显示 quick 模式 bug 率上升）
- full 模式明显过重（连续 3+ 任务超过 30 分钟）
- Conflict Gate 漏掉真实冲突（本应 BLOCKED 但 PASS 了）
- 某类 Unity 问题重复出现 2 次以上（对应某个 placeholder gate）
- metrics 显示某个风险指标持续上升（连续 3+ 任务）

### 不可触发 v1.8 的情况

- 只是觉得架构不够漂亮
- 想提前实现全部 placeholder gate
- 想接 LangChain 证明标准化
- 想拆目录让结构更像工程项目
- 想一次性覆盖完整游戏客户端生命周期

### 升级流程

1. 复盘记录断裂点（retrospective.md）
2. 断裂点匹配升级触发条件
3. 如果匹配 → 创建 `docs/WORKLINE_ARCHITECTURE_V1.8_PROPOSAL.md`
4. 提交思考线审查
5. 审查通过 → 实施 → 验证 → tag

---

## 12. 最终结论

v1.7-stable 的价值不是"功能更多"，而是：

- ✅ full / quick 分流成立（~5x 速度差）
- ✅ quick 模式减负成立（小任务不跑全流程）
- ✅ full 模式未退化（质量保持不变）
- ✅ Conflict Gate 保持 active（已验证 4 次）
- ✅ Lite 报告可用（WorklineSummary + metrics-lite）
- ✅ 证据闭环可用（git + reports + metrics）
- ✅ 违规归零（0 herm-write-code, 0 skip-review, 0 scope-creep）
- ✅ 系统从膨胀转向收敛（5 模式→2 模式，8 Gate→1 Gate，6 目录→1 文件）
- ✅ 设计审查机制有效（思考线 v4 阻止了过度设计）
- ✅ 验证驱动 tag（3 个真实任务通过后才打 stable）

---

## 附录 A：相关文档索引

| 文档 | 路径 | 用途 |
|:---|:---|:---|
| 运行时 Skill | `skills/workline-execution/SKILL.md` | v1.7.0 完整实现 |
| 管线设计 | `WORKFLOW.md` | 进化原则 + 断裂点表 |
| Agent 契约 | `AGENTS.md` | 角色 + 约束 + 降级链 |
| 回归套件 | `regression/README.md` | 6 个用例 |
| 报告检查 | `scripts/check_workline_outputs.py` | 完整性验证 |
| LangGraph 评估 | `skills/workline-execution/references/langgraph-evaluation.md` | 决策记录 |
| 系统全貌 | `docs/工作线系统全貌.md` | v1.6 时期的全面分析（历史参考） |
| v1.7 反方审查 | `think-tank/studies/2026-06-22_工作线v1.7-core-freeze审查-v4/` | 设计审查记录 |
| v1.7 复盘 | `retrospectives/2026-06-22-v1.7-stable-retro.md` | 本次版本复盘 |

## 附录 B：版本历史

| 版本 | 主要变更 |
|:---|:---|
| v1.2 | Git 集成 + Agent 契约 + 代码审计 |
| v1.3 | 依赖加载 + GATE 0 + 审查模板 + 回路机制 |
| v1.4 | SDD 非目标 + 4 份报告 + 越权检查 |
| v1.4.1 | Unity manifest 检查 |
| v1.5 | Metrics 基础 |
| v1.6 | Conflict Gate + 三段式 metrics + Regression suite |
| v1.7 | Mode Router + Gate 执行规则 + Lite 报告 + 7 placeholder |
