# Phase 1: Existing Pipeline Inventory — v1.11-office-onboarding

> 日期：2026-07-02 | 上接 Phase 0

## 1. 仓库结构概览

```
hermes-harness/
├── .github/workflows/       CI — workline-check.yml
├── docs/                    架构/计划/评估/治理/证据
├── skills/                  Hermes runtime skill (workline-execution)
├── tools/                   check_workline_task.py
├── tests/                   可执行测试夹具
├── regression/              10 个回归场景
├── tasks/                   真实任务证据包 (v1.8/v1.10)
├── retrospectives/          复盘 + 7 份 metrics.yaml
├── scripts/                 check_workline_outputs.py
├── reports/                 ← Phase 0 报告已写入
└── snippets/                可复用代码片段
```

---

## 2. 已有能力清单（17 项）

### 2.1 模式路由系统

| 能力 | 状态 | 描述 |
|:---|:---:|:---|
| **full 模式** | ACTIVE | 12 Phase 完整 SDD 驱动管线：ENV Check → 文档吸收 → UI路由 → 分析 → SDD → 冲突门 → Codex实现 → 编译修复 → HybridCLR → 审查 → 覆盖门 → 验证/注入/metrics |
| **quick 模式** | ACTIVE | 5 Step 轻量修复管线：ENV Check → 最小上下文 → 错误分析 → Codex修复 → 验证 + lite报告 |
| **auto-upgrade** | ACTIVE | quick 模式在触及 UI/协议/配置/性能/资源/平台/Hotfix 时自动升级为 full |
| **Mode Router** | ACTIVE | Agent 内部判定（不询问用户），基于任务特征自动选 full/quick |

### 2.2 需求摄入系统 (v1.10)

| 步骤 | 产出 | 状态 |
|:---|:---|:---:|
| AmbiguityReport | 歧义分析 | ACTIVE |
| ModeRoutingDecision | 模式路由 | ACTIVE |
| TaskBreakdown | 任务拆分 | ACTIVE |
| AcceptanceCriteria | 验收标准 | ACTIVE |
| ClientImpactMap | 客户端影响面 | ACTIVE |
| ImplementationBrief | 实现摘要 | ACTIVE |
| RequirementDigest | 需求摘要 | ACTIVE |

### 2.3 质量门禁

| Gate | 位置 | 触发 | 状态 |
|:---|:---|:---|:---|
| **GATE 0** | Phase 0 | 环境就绪检查（工程可达/dotnet/GM/Agent可用性） | ACTIVE |
| **UI Routing Gate** | Phase 1.5 | 任务涉及UI时强制路由到UI工作流 | ACTIVE |
| **Conflict Gate** | Phase 3.5b | 7项冲突检查（功能目标互斥/与非目标冲突/持久化存储/UI权限/排序权限/报告输出冲突） | ACTIVE |
| **Code Review Gate** | Phase 7 | Claude Code 委托审查（模式一致性/空安全/IsCan+Do/Handler覆盖）+ 命名合规grep | ACTIVE |
| **Coverage Gate** | Phase 7.5 | full 模式 + 业务逻辑 → 白盒覆盖矩阵检查 | ACTIVE |
| **Audit Version Gate** | Phase 8.0 | git status/log 确认审计目标版本 | ACTIVE |

### 2.4 自动阻断规则 (AUTO-BLOCK)

| # | 规则 | Phase | 触发条件 |
|:--|:---|:---:|:---|
| 1 | .bak 检测 | 0 | `find *.bak` 非空 → 强制 git init |
| 2 | 学习产出清单 | 1 | 学了新知识 → 必须列明应用目标，不允许"下次再用" |
| 3 | 命名合规grep | 7 | `p_n/p_sz/p_b` 或 `p_` 下划线残留 → NEEDS_FIX |
| 4 | 审计版本确认 | 8 | `git status -s` 非空或未push → 先问用户审哪个版本 |

### 2.5 Agent 分工契约

| 角色 | 职责 | 禁止 |
|:---|:---|:---|
| **Hermes** | 调度/编译验证/分析/SDD/复盘 | 写 .cs 文件 |
| **Codex** | 写代码/识图 | 做架构决策 |
| **Claude Code** | 代码审查 | 写新代码 |
| **用户** | Mentor审阅/Unity Play测试 | — |

降级链: Codex → Claude Code → Hermes。每次降级 = 复盘标记。

### 2.6 经验注入框架

| 通道 | 检查 | 触发条件 |
|:---|:---|:---|
| Rule | 本次是否有 ≥2 次重复错误？ | 升级为 AUTO-BLOCK |
| Metric | 本次是否有可对比的量化数据？ | 建立/更新基线 |
| Template | 本次产出是否可复用为格式模板？ | 提取为强制模板 |
| Capability | 本次是否证明某 domain 能力？ | 更新 capability 矩阵 |

### 2.7 工程工具

| 工具 | 路径 | 功能 |
|:---|:---|:---|
| Harness Checker | `tools/check_workline_task.py` | 验证文件完整性/YAML字段/报告一致性 |
| Report Integrity | `scripts/check_workline_outputs.py` | 检查 4 份报告是否存在 + TestReport 真实性 |
| CI | `.github/workflows/workline-check.yml` | 自动运行 checker |

### 2.8 回归套件

10 例回归测试：01 Unity新建 / 02 Unity修复 / 03 Python修复 / 04 冲突门 / 05 回路压测 / 06 quick修复 / 07 quick作用域违规 / 08 full指标冲突 / 09 full报告缺失 / 10 quick自动升级

### 2.9 指标系统

- **full 模式**: `metrics.yaml` — 8个phase指标 + 3类violation + mentor_verified
- **quick 模式**: `metrics-lite.yaml` — 轻量版（build/review/scope/duration）
- **累计**: 7 份已有 metrics，Level 1 趋势分析已完成

### 2.10 三条线切换协议

- 工作线 / 学习线 / 思考线
- 切换机制: Hermes 检测缺口 → `clarify()` 提议 → 用户裁决
- 绝不自动切换

### 2.11 ET6 领域知识 (skill内嵌)

- 命名规范（Hungarian notation）
- GM 面板系统（物品ID/操作路径）
- 编译路径陷阱（Server.sln位置）
- HybridCLR DLL缓存机制
- SDK模板（客户端+服务端）
- API名称陷阱（GetXxxByYyyId → GetXxx）

---

## 3. 可复用能力 vs 不能直接用于公司场景

### 3.1 可直接复用的能力

| 能力 | 复用方式 |
|:---|:---|
| Requirement Intake 链路 | 7文档模板 + 分析逻辑，不依赖项目代码 |
| Mode Router 分类逻辑 | 新增 office 模式即可，路由骨架不变 |
| Conflict Gate 方法论 | 7项冲突检查逻辑通用 |
| Experience Injection 框架 | Rule/Metric/Template/Capability 四通道完全通用 |
| Metrics 系统结构 | yaml 格式 + 趋势分析逻辑通用 |
| 三条线切换协议 | 完全通用 |
| Harness Checker 模式 | 验证逻辑可复用，规则需新增 |
| SDD 模板思路 | 需适配公司格式，但方法论不变 |
| Agent 分工契约 | 需新增"待授权执行者"角色 |

### 3.2 需要适配的能力

| 能力 | 入职场景问题 | 需要什么 |
|:---|:---|:---|
| **Phase 0 环境检查** | 检查 dotnet/Unity/GM/Codex 路径和权限，全项目特定 | 改为检查"什么允许/什么不允许"而非"什么可用" |
| **Phase 1 文档吸收** | 读取公司 .docx/.cs 文件 | 需要接收文档内容为字符串，不自动扫描 |
| **Phase 4-8 编码→验证链** | 写入公司项目代码 | 需要隔离工作区 + 人工merge |
| **ET6 命名规范** | 硬编码为热区网络规范 | 改为从目标项目提取规范（Pattern Extraction） |
| **Claude Code 审查** | 审查公司代码需要外发 | 需要在安全边界内或完全禁用 |
| **HybridCLR 缓存** | 公司项目未必用 HybridCLR | 改为通用Unity DLL缓存 |

### 3.3 入职场景缺失的能力

| 缺失 | 为什么需要 |
|:---|:---|
| **安全模式路由** | 当前没有"规范未知时默认禁用写入"的模式 |
| **敏感信息门** | 当前所有输出未经脱敏检查 |
| **公司规范确认门** | 当前假设已知项目规范 |
| **动作权限分级** | 当前所有动作要么允许要么禁止，没有灰度 |
| **持久化边界** | 当前可以保存任何内容到 Obsidian |
| **入职轻量模板** | 当前只有 SDD 模板和测试模板，无 Work Card/Bug Triage/日报模板 |
| **Obsidian 双 vault 策略** | 当前只有一个个人学习 vault |
| **个人实验场隔离** | 当前个人项目和公司项目无边界 |
| **规范吸收流程** | 当前规范是手动指定的，非从代码中提取 |

---

## 4. v1.11 需要新增的能力

基于以上 GAP 分析：

| 新增 | 类型 | 优先级 |
|:---|:---|---|
| **safe-note 模式** | 新模式 | P0 |
| **office-lite 模式** | 新模式 | P0 |
| **full-harness 模式** | 现有 full 模式的入职适配版 | P0 |
| **personal-lab 模式** | 现有 personal 项目的显式边界 | P0 |
| **Company Policy Gate** | 新 Gate | P0 |
| **Sensitive Data Gate** | 新 Gate | P0 |
| **Action Permission Gate** | 新 Gate | P0 |
| **Persistence Gate** | 新 Gate | P0 |
| **Mode Switch Gate** | 新 Gate | P0 |
| **Office 模板包** | 新模板 | P1 |
| **入职第一周 SOP** | 新文档 | P1 |
| **Obsidian 双 vault 策略** | 新文档 | P1 |
| **入职阶段 metrics** | 新指标 | P1 |

---

## 5. 管线能力总图（v1.10 现状）

```
需求输入
  ↓
[Intake] AmbiguityReport → ModeRouting → TaskBreakdown → AcceptanceCriteria →
         ClientImpactMap → ImplementationBrief → RequirementDigest
  ↓
[Mode Router] full / quick
  ↓
full:  Phase0→Phase1→Phase1.5→Phase2→Phase3→Phase3.5(Conflict)→Phase4(Codex)→
       Phase5(Compile)→Phase6(HybridCLR)→Phase7(Review)→Phase7.5(Coverage)→
       Phase8(Verify+Inject+Metrics)
quick: Phase0→MinimalContext→Analysis→CodexFix→Verify→Summary+metrics-lite
  ↓
[Gates] GATE0 / UI Routing / Conflict / Naming / Review / Coverage / Audit Version
  ↓
[Injection] Rule / Metric / Template / Capability
```

---

## 6. 结论

✅ Phase 1 完成。现有管线 17 项能力已盘点，可复用 10 项，需适配 6 项，缺失 13 项。v1.11 需要新增 4 模式 + 5 Gate + 4 模板 + 3 文档 + 1 指标体系。

**Phase 2 可以开始**：Office Onboarding 总设计文档的核心挑战是——在现有管线骨架上增加"入职安全层"，而不是重写整个管线。
