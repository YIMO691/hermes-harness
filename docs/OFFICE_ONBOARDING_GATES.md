# Office Onboarding Gates — Runtime Reference

> 版本：v1.11 | 来源：`docs/OFFICE_ONBOARDING_WORKLINE_V1.11.md` §5
>
> 本文档是 5 个 Gate 的运行时检查规则。按执行顺序排列。

---

## Gate Execution Order

每次请求处理中，Gate 的执行顺序是：

```text
请求进入
  ↓
[1] Company Policy Gate ─── 判定当前模式 (safe-note/office-lite/full-harness/personal-lab)
  ↓
[2] Action Permission Gate ─ 检查当前动作是否在当前模式下允许
  ↓
[3] Sensitive Data Gate ──── 输出前脱敏检查（每次响应、每次文件写入前）
  ↓
[如果进入 v1.10 管线...]
  ↓
[4] Persistence Gate ─────── 保存前脱敏检查（文件写入、memory、Obsidian）
  ↓
[5] Mode Switch Gate ─────── 三线切换时检查
```

---

## Gate 1: Company Policy Gate

### 状态定义

| 状态 | 含义 | 对应模式 |
|:---|:---|:---|
| `UNKNOWN` | 公司规范未确认 | safe-note |
| `DENIED` | 不允许个人 AI 工具处理公司项目 | safe-note (永久) |
| `ALLOWED_NOTE` | 允许个人笔记，不允许 AI 处理源码 | office-lite |
| `ALLOWED_AGENT` | 允许在授权范围内使用本地 Agent | full-harness |

### 默认状态

```text
新会话开始时: UNKNOWN
用户未提到"公司"时的任务: 按 personal-lab 判定
用户提到"公司项目"且状态为 UNKNOWN: 自动 safe-note
```

### 状态变更

- **只能由用户显式设置。** Hermes 可以提醒"你还没有确认公司规范"，但不能自动变更状态。
- 用户说"公司允许个人笔记" → `ALLOWED_NOTE`
- 用户说"导师不建议用个人AI" → `DENIED`
- 用户说"公司允许在指定目录用 Agent" → `ALLOWED_AGENT`
- `DENIED` 状态在当前会话中不可逆，需要新会话重新确认。

### 每次会话开始时的检查

```yaml
check:
  - 是否有来自 memory 的 Company Policy 状态？
  - 如果有且为 DENIED → 永久 safe-note
  - 如果有且为 ALLOWED_* → 使用该状态
  - 如果无 → UNKNOWN
```

**Memory 中的 Policy 状态存储规则**: 只存状态值（`company_policy: DENIED` 等），不存公司来源、原因等上下文。

---

## Gate 2: Action Permission Gate

### 动作分级表

| Level | 动作 | safe-note | office-lite | full-harness | personal-lab |
|:---:|:---|:---:|:---:|:---:|:---:|
| 0 | 生成话术/模板/通用学习 | ✅ | ✅ | ✅ | ✅ |
| 1 | 需求拆解/验收清单/风险分析 | ✅ | ✅ | ✅ | ✅ |
| 2 | 读取用户指定片段 | ❌ | ✅ | ✅ | ✅ |
| 3 | 扫描项目目录 | ❌ | ❌ | ✅(需授权) | ✅ |
| 4 | 修改本地文件 | ❌ | ❌ | ✅(需授权) | ✅ |
| 5 | 调用 Codex 修改代码 | ❌ | ❌ | ✅(需授权) | ✅ |
| 6 | 提交/推送/后台常驻 | ❌ | ❌ | ❌ | ❌ |

### 动作判定流程

```text
1. 识别当前动作的 Level
2. 查表：当前模式是否允许该 Level？
3. 允许 → 继续
4. 不允许 → BLOCKED + 回复模板
```

### Level 6 的回复模板

```text
❌ BLOCKED — Level 6 操作在所有模式下均被禁止。

不能被自动执行的操作：
- git commit / git push
- 启动后台常驻服务
- 在非 my 目录下创建计划任务/定时任务

如果你需要执行这些操作，请手动完成。
```

### 其他 Level 被阻止时的回复模板

```text
❌ BLOCKED — 当前模式 [SAFE_NOTE/OFFICE_LITE] 不允许 [动作描述]。

要升级模式，请先确认公司规范：
- 如果公司允许个人笔记 → 可以升级到 office-lite
- 如果公司允许在授权范围内使用 Agent → 可以升级到 full-harness
- 如果公司规范未确认 → 保持 safe-note
```

---

## Gate 3: Sensitive Data Gate

### 触发时机

- **每次 Hermes 响应输出前**
- **每次 write_file 写入前**
- **每次 memory 保存前**

### 检测清单

```yaml
sensitive_patterns:
  source_code:
    - C# 源码片段（class/method 完整定义）
    - 超过 3 行的连续代码引用
  identifiers:
    - 内部类名（特征：Player + 业务名 + Component/System/Event）
    - 内部方法名（特征：IsCan/Do/On + 业务名）
    - 内部接口名
  paths:
    - 公司项目绝对路径
    - 公司项目相对路径（包含 Assets/Scripts/等）
    - 公司服务器路径
  protocols:
    - Proto 消息名（C2Game_/Game2C_）
    - Proto 字段名
    - RPC 方法签名
  configs:
    - 配置表名
    - 配置字段名
    - 配置数值
  assets:
    - Prefab 名
    - 资源路径
    - AssetBundle 名
  secrets:
    - Token/Key/Secret
    - 服务器地址
    - 账号
  internal:
    - 未公开玩法描述
    - 未公开活动信息
    - 具体 Bug 单内容
    - 内部文档原文段落
```

### 改写规则

| 原始（不能输出） | 改写为（可以输出） |
|:---|:---|
| `PlayerNerveComponent.m_dicNerve` | "神经数据的字典字段" |
| `Assets/Bundles/UI/dlg_gm_main.prefab` | "GM面板的Prefab" |
| `C2Game_DNAUnlockHandler` | "基因解锁的网络处理" |
| `D:\公司项目\Assets\Scripts\Player.cs` | "玩家脚本文件" |
| `NerveMouldConfig.Id` | "神经配置表的主键字段" |

### 无法改写的情况

- **Token/Key/Secret** → `BLOCKED`，不输出
- **服务器地址 + 端口** → `BLOCKED`，不输出

### 输出标记

改写过内容的响应在末尾标注: `[REDACTED — 已脱敏 N 处]`

---

## Gate 4: Persistence Gate

### 触发时机

- **write_file 写入 Obsidian 工作 vault 时**
- **memory 工具调用时（记录涉及公司项目的内容时）**
- **任何涉及持久化公司相关信息的操作**

### 允许持久化的内容

```yaml
allowed:
  - 抽象经验（"ET6 中 Component 和 System 的分工是..."）
  - 通用流程/SOP（"排查网络同步问题的标准流程"）
  - 个人理解（"我对 Actor 模型的理解是..."）
  - Checklist（"提交前检查清单"）
  - 模板（"日报模板"、"Bug Triage 模板"）
  - 脱敏后的 Work Card
```

### 禁止持久化的内容

```yaml
blocked:
  - 公司源码（任何 C#/proto/xml 文件内容）
  - 公司路径
  - 内部类名/方法名
  - 内部协议定义
  - 配置字段/数值
  - 资源名/Prefab名
  - 具体 Bug 描述
  - 需求原文
  - 内部文档原文
  - 账号/密钥/服务器地址
```

### 双 Vault 策略

| Vault | 路径 | 可存内容 |
|:---|:---|:---|
| 个人学习 | `D:\Obsidian\Unity学习知识库` | 所有 personal-lab 内容 + 通用学习 |
| 工作 Vault | 待入职后创建 | 仅脱敏内容（通过 Persistence Gate） |

**写入工作 Vault 前必须通过 Persistence Gate 检查。**

---

## Gate 5: Mode Switch Gate

### 三条线定义

| 线 | 目的 | 对应 skill |
|:---|:---|:---|
| 工作线 | 执行任务 | workline-execution（本 skill） |
| 学习线 | 弥合知识缺口 | et6-learning, unity-ui-architecture-learning 等 |
| 思考线 | 重大决策多方审判 | dialectical-thinking (think-tank v4) |

### 规则

```text
Hermes 可以提示："当前问题可能需要切换到 [学习线/工作线/思考线]，是否切换？"

但不能自动切换。
```

### 提示格式

```text
💡 三线切换提示

检测到 [知识缺口/结构变更/重大决策需求]：[具体描述]

建议切换到 [学习线/工作线/思考线]，原因：[...]

切换后：[当前工作线状态是否可恢复的说明]

是否切换？[切换 / 稍后 / 忽略]
```

使用 `clarify()` 工具询问用户。

### 自动切换禁止原因

用户明确要求。三条线边界是人机协作的决策权边界——Agent 建议，人裁决。
