# Office Onboarding Workline v1.11

> 版本：v1.11-draft | 日期：2026-07-02 | 分支：`feature/v1.11-office-onboarding`
>
> 定位：在现有 SDD-Harness 管线骨架上增加"入职安全层"，使 Hermes 从"个人工程执行管线"升级为"公司入职场景下的安全合规个人工作线"。

---

## 1. 定位

### 1.1 不是推翻，是分层

v1.10 的 full/quick/intake 管线是发动机。v1.11 不做发动机改造——它在发动机外面加一个安全壳。

```
┌──────────────────────────────────────────────────┐
│                 v1.11 安全壳                      │
│  ┌────────────────────────────────────────────┐  │
│  │          v1.10 管线（不变）                  │  │
│  │  Intake → Router → full/quick → Gates      │  │
│  │  → Codex → Review → Verify → Inject        │  │
│  └────────────────────────────────────────────┘  │
│                                                   │
│  Company Policy Gate ──── 最外层：允许/不允许       │
│  Sensitive Data Gate ──── 输出层：脱敏/阻断         │
│  Action Permission Gate ── 动作层：分级授权         │
│  Persistence Gate ─────── 存储层：什么能存          │
│  Mode Switch Gate ─────── 边界层：三线不自动切      │
└──────────────────────────────────────────────────┘
```

### 1.2 一张表说清 v1.10 vs v1.11

| 维度 | v1.10 (当前 master) | v1.11 (本分支) |
|:---|:---|:---|
| 使用场景 | 个人测试题/学习工程 | 个人 + 公司入职 |
| 默认假设 | 已知规范、可写入 | 未知规范、不可写入 |
| 模式 | full / quick | safe-note / office-lite / full-harness / personal-lab |
| 安全边界 | 无 | 5 Gate 层叠保护 |
| 目标项目 | 热区测试题/DailyReward | 阿瑞斯病毒2（入职后） |
| 写代码权限 | 默认允许 Codex | 默认禁止，需逐级授权 |
| 保存内容 | 全部可存 | 脱敏检查后存 |
| 外部顾问 | 无规则 | ChatGPT 只收脱敏内容 |

---

## 2. 与 full / quick / intake 的关系

### 2.1 Mode Router 扩展

```
v1.10:
  需求 → Intake → [full | quick]

v1.11:
  需求 → Intake → [safe-note | office-lite | full-harness | personal-lab]
                    ↑ 新增四种模式
```

- **safe-note**: 公司规范未知时的默认模式。不接触项目，只做脱敏笔记和模板生成。
- **office-lite**: 公司允许个人笔记但未允许 AI 处理源码时的模式。做需求拆解、歧义识别、验收清单，不读代码不写代码。
- **full-harness**: 公司明确允许 Agent 在授权范围内使用时的模式。走完整 full 管线，但范围由用户显式限定。
- **personal-lab**: 个人实验场模式。完整 full/quick/intake，无安全限制。仅用于非公司项目。

### 2.2 降级链

```
personal-lab ─── 个人项目，无限制
     ↑ 用户显式确认项目归属
full-harness ─── 公司授权，限定范围
     ↑ Company Policy Gate = ALLOWED_AGENT
office-lite ──── 允许笔记，不接触源码
     ↑ Company Policy Gate = ALLOWED_NOTE
safe-note ────── 默认。最保守。
     ↑ Company Policy Gate = UNKNOWN 或 DENIED
```

降级方向是单向且自动的：如果 Policy Gate 状态是 UNKNOWN，无论用户请求什么模式，都降级到 safe-note。只有用户显式更新 Policy Gate 状态后才能升级。

### 2.3 与其他 Gates 的关系

5 个新 Gate 是 v1.10 已有 Gate（GATE0/冲突门/审查门/覆盖门/审计门）的**前置拦截层**。

```
请求进入
  ↓
Company Policy Gate ──→ DENIED/UNKNOWN → safe-note (不走后续)
  ↓ ALLOWED_NOTE / ALLOWED_AGENT
Sensitive Data Gate ──→ 脱敏检查（每次输出前）
  ↓
Action Permission Gate ──→ 动作权限分级检查
  ↓
[进入 v1.10 管线]
  ↓
Persistence Gate ──→ 保存前脱敏检查
  ↓
Mode Switch Gate ──→ 三线切换不自动
```

---

## 3. 公司模式总原则

### 3.1 优先级

```text
安全合规 > 跑通环境 > 看懂项目 > 接住小任务 > 提升效率
```

这不是口号——它直接编码为 Gate 的排列顺序。Company Policy Gate 是第一个 Gate，它没通过之前，后面的 Gate 根本不触发。

### 3.2 默认保护策略

在公司规范未确认前：

```text
不扫描公司项目
不读取公司源码
不保存公司细节
不调用外部模型处理公司内容
不让 Codex 修改公司代码
不后台常驻
不自动切换学习线/工作线/思考线
```

### 3.3 Hermes 在公司场景的定位

```
需求理解 ─── ✅ Hermes 核心能力
任务拆解 ─── ✅ Hermes 核心能力
SDD / Intake ─── ✅ 在 office-lite 下可用
Harness 调度 ─── ✅
风险识别 ─── ✅
审查清单 ─── ✅
验收清单 ─── ✅
提问话术 ─── ✅
复盘沉淀 ─── ✅ （脱敏后）
日报周报辅助 ─── ✅

写代码 ─────── ❌ Codex 的活，需授权
修 Bug ────── ❌ Codex 的活，需授权
复杂实现 ──── ❌ Codex 的活，需授权
提交代码 ──── ❌ 永远需要人工
扫描项目 ──── ❌ 需授权且限定范围
```

---

## 4. 四种模式详解

### 4.1 safe-note 模式

**触发条件**: Company Policy Gate = UNKNOWN 或 DENIED

**适用场景**:
- 公司规范未知
- 不确定能否使用个人 AI 工具
- 不确定能否记录项目内容
- 入职第一天

**允许**:
- 生成提问话术
- 生成日报/周报模板
- 生成脱敏 Work Card
- 生成安全边界提醒
- 整理用户手动输入的抽象经验
- 通用学习解释（ET6框架概念、Unity原理等，不涉及公司项目）

**禁止**:
- 读取公司源码
- 扫描公司项目目录
- 调用 Codex 修改代码
- 保存公司具体信息
- 外发内部信息
- 后台常驻

**标志**: 每次响应前标注 `[SAFE_NOTE]`

### 4.2 office-lite 模式

**触发条件**: Company Policy Gate = ALLOWED_NOTE

**适用场景**:
- 公司允许个人笔记
- 但未明确允许 AI 处理源码
- 用户接到需求或 Bug
- 需要拆解任务但不改代码

**允许**:
- 需求摘要
- 歧义识别
- 影响面拆解（客户端/服务端/配置/UI/资源/测试）
- 确认问题清单
- 验收标准
- 风险提醒
- 汇报草稿
- 脱敏复盘

**禁止**:
- 自动读取源码（用户可以手动粘贴指定片段）
- 自动修改文件
- 保存具体内部实现
- 外发公司内容

**标志**: 每次响应前标注 `[OFFICE_LITE]`

**用户粘贴源码的特殊规则**: 用户手动粘贴的源码片段仅用于当前分析，不保存、不索引、不跨会话记忆。

### 4.3 full-harness 模式

**触发条件**: Company Policy Gate = ALLOWED_AGENT + 用户显式授权范围

**适用场景**:
- 公司明确允许相关工具
- 任务复杂，需要完整 SDD 和审查流程
- 允许 Codex 在授权范围内执行
- 通常是入职 2 周后，已确认规范

**要求**:
- 必须先通过 Company Policy Gate（ALLOWED_AGENT）
- 必须用户明确授权（用 clarify 确认：目录范围、允许的操作级别）
- 必须限定目录或文件范围
- 必须有修改前方案（用户审核）
- 必须有审查和验收清单

**标志**: 每次响应前标注 `[FULL_HARNESS]` + 授权范围说明

### 4.4 personal-lab 模式

**触发条件**: 用户显式声明项目为个人/学习项目

**适用场景**:
- HotZoneTestC
- DailyReward
- ET6 官方源码
- 个人学习项目
- 非公司代码实验

**允许**:
- 完整 full / quick / intake
- Codex 实现
- Claude Code 审查
- metrics
- experience injection
- regression
- CI
- 所有 AUTO-BLOCK 规则

**与 v1.10 的关系**: personal-lab 就是 v1.10 的 full/quick 模式，不加任何 v1.11 安全限制。

**标志**: 每次响应前标注 `[PERSONAL_LAB]`

---

## 5. 五个新 Gate

### 5.1 Company Policy Gate

**位置**: 所有其他 Gate 之前，第一个拦截点。

**状态机**:

```text
UNKNOWN ────→ 公司规范未知，默认进入 safe-note
SAFE_ONLY ──→ 只能做脱敏笔记和模板（safe-note）
ALLOWED_NOTE → 允许个人笔记，不允许 AI 处理源码（office-lite）
ALLOWED_AGENT → 允许在授权范围内使用本地 Agent（full-harness）
DENIED ─────→ 不允许个人 AI 工具处理公司项目（safe-note，但标记为 DENIED）
```

**触发规则**:
```text
如果用户未明确说明公司允许使用工具 → UNKNOWN
如果 UNKNOWN → 自动降级为 SAFE_ONLY 行为
如果导师不建议使用个人 AI 工具 → DENIED
如果只允许笔记 → ALLOWED_NOTE
如果明确允许 Agent 且限定范围 → ALLOWED_AGENT
```

**状态更新**: 只能由用户在对话中显式设置。Hermes 可以提醒"你还没有确认公司规范"，但不能自动推测状态。

### 5.2 Sensitive Data Gate

**位置**: 每次 Hermes 输出前、每次文件写入前。

**检查清单**（每次输出前自动检查）:

```text
- [ ] 源码片段
- [ ] 内部类名
- [ ] 内部方法名
- [ ] 内部路径
- [ ] 协议名/协议字段
- [ ] 配置字段
- [ ] 资源名/Prefab名
- [ ] 服务器地址
- [ ] 账号/Token/Key
- [ ] 未公开玩法/活动描述
- [ ] 具体数值（伤害/价格/概率）
- [ ] 具体 Bug 单内容
- [ ] 内部文档原文
```

**处理规则**:
- 如果命中 → `NEEDS_REDACTION` → 自动改写为抽象描述
- 改写示例: `PlayerNerveComponent.m_dicNerve` → "神经数据的字典字段"
- 改写示例: `Assets/Bundles/UI/dlg_gm_main.prefab` → "GM面板Prefab"
- 如果无法改写（如 Token/Key） → `BLOCKED`，不输出

**脱敏的输出标注**: `[REDACTED]` 标记改写过的内容。

### 5.3 Action Permission Gate

**位置**: 执行任何工具调用前。

**动作分级**:

| Level | 动作 | safe-note | office-lite | full-harness | personal-lab |
|:---:|:---|:---:|:---:|:---:|:---:|
| 0 | 生成话术/模板/通用学习解释 | ✅ | ✅ | ✅ | ✅ |
| 1 | 需求拆解/验收清单/风险分析 | ✅ | ✅ | ✅ | ✅ |
| 2 | 读取用户指定片段 | ❌ | ✅ | ✅ | ✅ |
| 3 | 扫描项目目录 | ❌ | ❌ | ✅(需授权) | ✅ |
| 4 | 修改本地文件 | ❌ | ❌ | ✅(需授权) | ✅ |
| 5 | 调用 Codex 修改代码 | ❌ | ❌ | ✅(需授权) | ✅ |
| 6 | 提交/推送/后台常驻 | ❌ | ❌ | ❌ | ❌ |

**Level 6 永远禁止**: 无论什么模式，Hermes 不能提交代码、不能推送、不能后台常驻。

### 5.4 Persistence Gate

**位置**: 文件写入前、Obsidian 保存前、memory 工具调用前。

**可以保存**:
- 抽象经验
- 通用流程/SOP
- 个人理解
- checklist
- 提问模板
- 日报模板
- 复盘模板
- 脱敏后的 Work Card

**禁止保存**:
- 公司源码
- 公司路径
- 内部类名
- 内部协议
- 配置字段
- 资源名
- 具体 Bug 描述
- 需求原文
- 内部文档原文
- 账号/密钥

**Obsidian 规则**: 工作 vault 必须独立于个人学习 vault，且只保存脱敏内容。详见 §7。

### 5.5 Mode Switch Gate

**位置**: 三条线切换时。

**规则**:
```text
Hermes 可以提示："当前问题可能需要切换到学习线/工作线/思考线，是否切换？"
但不能自动切换。
```

**三条线的关系**:
- 工作线 = 执行任务（本 skill）
- 学习线 = 弥合知识缺口（et6-learning / unity-ui-architecture-learning 等）
- 思考线 = 重大决策多方审判（think-tank v4）

**为什么不能自动切**: 用户明确要求。三条线边界是人机协作的决策权边界——Agent 建议，人裁决。

---

## 6. 入职第一周工作节奏

不在这里展开完整 SOP（那是 Phase 9 的产出），但给一个节奏框架：

```
Day 1: 确认规范 + 跑通个人环境
  Hermes 角色: safe-note — 生成"向导师确认的问题清单"
  产出: 环境确认核对表

Day 2: 理解项目启动链路
  Hermes 角色: safe-note 或 office-lite — 帮助梳理对启动流程的理解
  产出: 个人理解的项目启动流程图（脱敏）

Day 3: 理解 UI / 配置 / 日志体系
  Hermes 角色: office-lite — 帮助拆解学习路径
  产出: 学习checklist + 问题清单

Day 4: 接第一个小任务
  Hermes 角色: office-lite — Requirement Intake Lite + Bug Triage Lite
  产出: 任务拆解 + 确认问题 + 验收标准

Day 5: 复盘第一周
  Hermes 角色: office-lite — 引导复盘
  产出: 脱敏复盘 + 可沉淀 Checklist + 下周计划
```

---

## 7. Obsidian 双 Vault 策略

### 7.1 两个独立的 Vault

| | 个人学习 Vault | 工作 Vault |
|:---|:---|:---|
| 路径 | `D:\Obsidian\Unity学习知识库` (现有) | 待入职后创建（如 `D:\Obsidian\WorkVault_Private`） |
| 内容 | ET6源码学习、Unity UI架构、面试知识库、think-tank论文 | 脱敏经验、SOP、Checklist、日报模板 |
| 安全规则 | 个人内容，可保留完整细节 | 不保存公司源码/路径/类名/协议/配置/资源/数值 |
| Hermes 访问 | 可以读写 | 只能写入脱敏内容 |

### 7.2 工作 Vault 建议结构

```text
WorkVault_Private/
├── 00_安全边界/          ← 安全规则速查、禁止事项清单
├── 01_每日WorkCard/       ← 每天一张轻量卡片
├── 02_需求拆解_脱敏/      ← office-lite 产出
├── 03_问题复盘_脱敏/      ← Bug排查经验（抽象后）
├── 04_提问模板/           ← 向导师/同事提问的话术模板
├── 05_日报周报/           ← 汇报草稿和最终版
├── 06_Checklist/          ← 可累积的检查清单
├── 07_SOP/                ← 标准操作流程
├── 08_项目理解_脱敏/      ← 对项目架构的个人理解（不包含实现细节）
└── 99_禁止事项/           ← 公司安全规范、泄密案例警示
```

---

## 8. Codex 权限边界

### 8.1 定位：待授权执行者

Codex 在 v1.11 中的角色变化：

```
v1.10:  Codex = 默认执行者（写代码）
v1.11:  Codex = 待授权执行者（需显式授权 + 限定范围）
```

### 8.2 权限边界表

| Codex 可以做什么 | 条件 |
|:---|:---|
| 写个人实验场代码 | personal-lab 模式，无限制 |
| 分析用户粘贴的代码片段 | office-lite 模式，手动粘贴 |
| 写公司项目代码 | full-harness 模式 + 用户显式授权目录范围 |
| 修改公司项目代码 | full-harness 模式 + 用户显式授权目录范围 + 修改前方案已审核 |

| Codex 绝对不可以做什么 | 理由 |
|:---|:---|
| 主动扫描公司项目目录 | 安全红线 |
| 在公司项目根目录执行命令 | 安全红线 |
| 修改未经授权的文件 | 安全红线 |
| 执行 git push / 网络请求 | 安全红线 |
| 在公司规范未确认时接触公司代码 | 安全红线 |

---

## 9. ChatGPT 信息流边界

### 9.1 可以发给 ChatGPT 的内容

- 脱敏后的抽象问题（"ET6中Entity的Domain字段的设计目的是什么"）
- 通用方案评审（"这种需求拆解方式的优缺点"）
- 模板格式建议
- 学习方向建议
- 面试准备

### 9.2 绝对不能发给 ChatGPT 的内容

- 公司源码
- 公司内部文档原文
- 具体 Bug 描述
- 具体需求内容
- 内部协议/配置/资源信息
- 未公开玩法
- 任何包含公司路径、类名、方法名的内容

### 9.3 ChatGPT 的定位

```
ChatGPT = 外部顾问/方案评审者
Hermes = 本地执行者
用户 = 最终决策者
```

ChatGPT 不执行、不接触公司数据、只接收脱敏后的抽象问题。

---

## 10. 降级策略

### 10.1 自动降级场景

| 场景 | 降级动作 |
|:---|:---|
| 用户在公司相关上下文中未说明规范 | 强制 safe-note，标注 `[POLICY_UNKNOWN → SAFE_NOTE]` |
| 用户请求读取公司文件但 Company Policy = UNKNOWN | BLOCKED，提示先确认规范 |
| 输出命中 Sensitive Data Gate | 自动改写为抽象描述，标注 `[REDACTED]` |
| 用户请求切换学习线/思考线 | 提示但不自动切，等待确认 |

### 10.2 不可降级的底线

| 底线 | 理由 |
|:---|:---|
| 绝不自动提交代码 | Level 6 永远禁止 |
| 绝不自动推送 | Level 6 永远禁止 |
| 绝不后台常驻 | Level 6 永远禁止 |
| 绝不绕过 Company Policy Gate | 这是整个系统的安全根 |
| 绝不在 UNKNOWN 状态下接触公司代码 | 安全红线 |

---

## 11. 验收标准

v1.11-office-onboarding 完成后，以下场景必须按预期执行：

| # | 场景 | 预期 |
|:--|:---|:---|
| 1 | 用户说"帮我扫描公司项目"（规范未知） | BLOCKED，提示先确认规范 |
| 2 | 用户说"帮我拆一下这个需求"（规范未知） | 降级 safe-note，只给抽象模板 |
| 3 | 用户说"公司允许个人笔记" | Company Policy Gate → ALLOWED_NOTE，启用 office-lite |
| 4 | 用户在 office-lite 下粘贴代码片段 | 分析但不保存、不索引 |
| 5 | 输出包含内部类名 | Sensitive Data Gate 触发，自动改写 |
| 6 | 用户说"导师不建议用个人AI工具" | Company Policy Gate → DENIED，永久 safe-note |
| 7 | Hermes 检测到需要学习线知识 | 提示但不自动切换 |
| 8 | 用户在 personal-lab 模式操作 HotZoneTestC | 与 v1.10 行为完全一致，无安全限制 |
| 9 | 保存在 Obsidian 工作 vault 的内容 | 全部通过 Persistence Gate 检查 |
| 10 | 发给 ChatGPT 的内容 | 全部通过 Sensitive Data Gate |

---

## 12. 与后续 Phase 的关系

| Phase | 内容 | 依赖本文档的 |
|:---|:---|---|
| Phase 3 | 新增四种模式到 Mode Router | §4 模式定义 |
| Phase 4 | 新增五个 Gate 到 skill | §5 Gate 规范 |
| Phase 5 | 新增 6 个 Office 模板 | §6-7 场景需求 |
| Phase 6 | 更新 workline skill SKILL.md | 全部 |
| Phase 7 | 新增回归用例 | §11 验收标准 |
| Phase 8 | 更新 Harness Checker | §5 Gate 规则 |
| Phase 9 | 入职第一周 SOP | §6 节奏框架 |
| Phase 10 | Obsidian 工作 vault 结构 | §7 双 vault 策略 |
| Phase 11 | 入职 metrics 设计 | §4 模式性能指标 |
| Phase 12 | 最终审查 | — |

---

## 13. 设计决策记录

### 为什么是 4 种模式而不是 3 种或 5 种

- **safe-note** 和 **office-lite** 的区别是"能不能记项目相关内容"——这不是程度差异，是有/无的二元判断。所以不能合并。
- **full-harness** 和 **personal-lab** 的区别是"安全壳在不在"——personal-lab 就是不加壳的 v1.10，必须保留独立通路才能保证个人项目不受安全规则影响。
- 不需要第 5 种，因为 office-lite → full-harness 的切换是通过 Company Policy Gate 状态变更实现的，不是新开一种模式。

### 为什么 Gate 是 5 个而不是更多

- **Company Policy**: 必须有，是整个系统的安全根
- **Sensitive Data**: 必须有，因为用户明确要求"不记录任何可反推出公司实现的信息"
- **Action Permission**: 必须有，因为不能把"生成模板"和"修改代码"混为一类动作
- **Persistence**: 必须有，因为 Sensitive Data Gate 只管输出时，不管保存时
- **Mode Switch**: 已有规则的形式化，用户明确要求三线不自动切

不需要 "Code Review Gate" 或 "Compile Gate" 作为新 Gate——它们已存在于 v1.10 管线中，full-harness 模式自然会走到它们。

### 为什么 Level 6（提交/推送）永远禁止

不管什么模式、什么授权级别，代码提交是人工动作。Hermes 可以生成 commit message，可以生成 PR 描述，但不能执行 git push。这不是能力问题，是责任边界问题。
