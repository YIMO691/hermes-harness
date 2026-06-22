# UNITY_CLIENT_LIFECYCLE_COVERAGE

> 版本：v1.0
> 状态：Draft
> 依赖：`docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md`
> 目的：定义工作线与完整游戏客户端开发领域之间的覆盖关系
> 原则：这是领域能力地图，不是当前运行流程；不新增 active Gate，不修改 workline 核心。

---

## 1. 文档目标

当前工作线已经能够覆盖"需求 / Bug → 技术拆分 → 实现 → 验证 → 审查 → 复盘"的功能交付核心段。

但完整游戏客户端开发不止这一段，还包括：

* 策划需求评审
* UI / UX 评审
* 美术资源导入
* 动画 / 特效 / 音频
* 配置 / 数值表
* 网络 / 协议 / 同步
* 性能 / GC / 渲染
* 多平台适配
* QA 缺陷管理
* CI / CD
* 发版 / 热更 / 回滚
* 线上监控

本文用于明确：

1. 当前工作线覆盖了什么；
2. 当前没有覆盖什么；
3. 哪些未来可以通过 Gate、Checklist、Regression、CI 补充；
4. 哪些现在只记录为 Backlog，不进入主流程；
5. 哪些触发条件满足后才允许升级为 active gate。

---

## 2. 当前定位

当前工作线定位为：

> 游戏客户端功能交付 Harness 的核心骨架。

当前覆盖的不是完整游戏客户端研发平台，而是：

```text
需求 / Bug
→ full / quick 判断
→ SDD / Lite Plan
→ Conflict Gate
→ Codex 实现
→ Build / Review / Unity Verify
→ Metrics / Retro
→ Git Evidence
```

它解决的是：

```text
如何让 AI Agent 参与游戏客户端功能开发时，不乱改、不漏审、不跳过验证，并留下可追踪证据。
```

---

## 3. 当前已覆盖环节

### 3.1 需求 / Bug 进入

当前已覆盖：

* 用户输入需求
* 用户输入 Bug
* 任务初步定型
* full / quick 模式判断
* 非目标定义
* 验收标准定义

当前产物：

* full：TaskSpec / SDD
* quick：WorklineSummary

---

### 3.2 技术拆分

当前已覆盖：

* 代码现状盘点
* 依赖关系分析
* 任务拆分
* 修改范围定义
* 验收清单定义
* Agent 分工

当前主要对应：

* full 模式
* SDD
* Conflict Gate

---

### 3.3 编码实现

当前已覆盖：

* Codex 根据任务计划实现
* Hermes 负责调度和验证
* Claude Code 负责审查
* 用户负责最终 Unity Play 验证

当前限制：

* Codex 不做架构决策
* Hermes 不在 full 模式下直接写核心业务代码
* Claude Code 不替代编译和用户验证

---

### 3.4 编译与测试

当前半覆盖：

* Unity 编译
* dotnet build
* Python pytest
* 基础手动验证
* Unity Play 验证记录

待强化：

* 自动检查 TestReport 是否完整
* 自动检查 build.passed 与 result 是否一致
* 自动检查 user_verified 是否被正确记录

---

### 3.5 代码审查

当前已覆盖：

* Claude Code 审查
* ChangedFiles
* REVIEW
* RiskReport
* scope creep 检查
* 空引用 / 生命周期 / 事件绑定等风险检查

待强化：

* 自动检查 full 任务是否缺 REVIEW
* 自动检查 REVIEW 是否有 verdict
* 自动检查 severe issue 是否阻断 result=approved

---

### 3.6 Metrics / Retro

当前已覆盖：

* metrics.yaml
* metrics-lite.yaml
* retrospective.md
* skill patch 进化机制
* regression 记录

待强化：

* 自动检查 metrics 字段完整性
* 自动检查 result 与 build / review / user_verified 是否一致
* 汇总趋势分析

---

### 3.7 Git Evidence

当前已覆盖：

* branch
* commit
* git diff
* git status
* tag
* rollback
* release / hotfix 文档规则

待强化：

* PR Template
* GitHub Actions
* pre-merge check
* stable tag 自动检查

---

## 4. 未完整覆盖环节

当前未完整覆盖的游戏客户端开发领域包括：

1. 策划评审流程
2. UI / UX 专业评审
3. 美术资源导入流程
4. 动画 / 特效 / 音频流程
5. 配置 / 数值表流程
6. 网络 / 协议 / 同步流程
7. 性能 / GC / 渲染流程
8. 多平台适配流程
9. QA 缺陷生命周期
10. CI / CD 自动化
11. 发版 / 热更 / 回滚
12. 线上监控与告警

这些不是当前版本的失败，而是未来领域扩展方向。

原则：

> 当前先建立覆盖地图，不把所有领域直接塞进主流程。

---

## 5. 游戏客户端生命周期覆盖矩阵

| 环节            | 当前状态  | 当前承载位置                        | 未来补充方式                    | 是否现在激活 |
| ------------- | ----- | ----------------------------- | ------------------------- | ------ |
| 需求 / Bug 进入   | 已覆盖   | Mode Router / TaskSpec        | 继续保持                      | 是      |
| 技术拆分          | 已覆盖   | full SDD                      | 强化模板                      | 是      |
| 小 Bug 修复      | 已覆盖   | quick / WorklineSummary       | v1.8 自动检查                 | 是      |
| 编码实现          | 已覆盖   | Codex                         | 保持 Agent 契约               | 是      |
| 编译验证          | 半覆盖   | TestReport / 用户记录             | v1.8 自动检查                 | 是      |
| Claude Review | 已覆盖   | REVIEW / RiskReport           | v1.8 检查缺失                 | 是      |
| Unity Play    | 半覆盖   | TestReport / user_verified    | v1.8 检查记录                 | 是      |
| Git Evidence  | 已覆盖   | Git Workflow                  | v1.9 CI 适配                | 是      |
| 策划评审          | 未完整覆盖 | 暂无                            | Requirement Checklist     | 否      |
| UI / UX 评审    | 未完整覆盖 | Future UI Gate                | Unity UI Gate             | 否      |
| 美术资源导入        | 未覆盖   | Future Asset Gate             | Asset Checklist           | 否      |
| 动画 / 特效 / 音频  | 未覆盖   | Future Presentation Checklist | Presentation Gate         | 否      |
| 配置 / 数值表      | 未完整覆盖 | Future Config Gate            | Config Gate               | 否      |
| 网络 / 协议 / 同步  | 未完整覆盖 | Future Network Gate           | Network Gate              | 否      |
| 性能 / GC / 渲染  | 未完整覆盖 | Future Performance Gate       | Performance Gate          | 否      |
| 多平台适配         | 未覆盖   | Future Platform Gate          | Platform Gate             | 否      |
| QA 缺陷流转       | 未完整覆盖 | Regression / Issue Flow       | QA / Regression Gate      | 否      |
| CI / CD       | 未覆盖   | Future CI Layer               | v1.9-ci-eval              | 否      |
| 发版 / 热更 / 回滚  | 半覆盖   | Git Workflow                  | Release / Hotfix Gate     | 否      |
| 线上监控          | 未覆盖   | Future Ops Layer              | Ops / Telemetry Checklist | 否      |

---

## 6. Future Gate Backlog

以下 Gate 仅作为未来 Backlog，不是当前 active gate。

当前唯一 active hard gate 仍然是：

```text
Conflict Gate
```

### 6.1 Unity UI Gate

触发场景：

* Panel
* Button
* ScrollView
* List Item
* Toggle
* Dropdown
* UI 状态刷新
* UI 与数据绑定

检查方向：

* 是否重复绑定事件
* 是否解绑事件
* 是否空引用保护
* 是否高频刷新
* 是否需要对象池
* 是否破坏已有筛选 / 排序
* 是否存在 UI 状态与数据状态不一致

当前状态：

```text
placeholder
```

---

### 6.2 Config Gate

触发场景：

* 配置表
* 数值表
* 静态数据
* ID 映射
* 活动参数
* 本地 JSON / ScriptableObject

检查方向：

* 字段是否存在
* 默认值是否合法
* 缺表 / 空表是否处理
* 非法 ID 是否处理
* 配置与代码逻辑是否一致
* 是否影响热更配置

当前状态：

```text
placeholder
```

---

### 6.3 Network Gate

触发场景：

* 协议
* 请求 / 响应
* Handler
* 状态同步
* 断线重连
* 登录 / 背包 / 战斗 / 聊天等网络模块

检查方向：

* 请求响应是否成对
* 错误码是否处理
* 超时是否处理
* 重复点击是否防抖
* 断线重连后状态是否恢复
* 服务端非法数据是否保护
* Handler 是否完整记录日志

当前状态：

```text
placeholder
```

---

### 6.4 Performance Gate

触发场景：

* Update
* 大量对象
* 背包列表
* 排行榜
* 资源加载
* GC
* 渲染
* 高频交互

检查方向：

* Update 中是否分配 GC
* 是否使用 LINQ / 闭包造成分配
* 是否频繁 Instantiate / Destroy
* 是否重复 GetComponent
* 是否需要对象池
* 是否影响 DrawCall / SetPass
* 是否有 profiling 证据

当前状态：

```text
placeholder
```

---

### 6.5 Asset Gate

触发场景：

* Prefab
* Texture
* Audio
* Animation
* Resources
* AssetBundle
* Addressables

检查方向：

* 资源路径是否正确
* 引用是否可能丢失
* 是否同步加载卡顿
* 是否包体增大
* 是否重复资源
* 是否需要卸载
* 是否符合项目资源加载方式

当前状态：

```text
placeholder
```

---

### 6.6 Platform Gate

触发场景：

* Android
* iOS
* IL2CPP
* 分辨率适配
* 刘海屏 / 安全区
* 权限
* 触摸输入
* 移动端性能

检查方向：

* IL2CPP 反射 / 泛型风险
* 权限处理
* 分辨率适配
* 输入差异
* 移动端性能
* 包体限制

当前状态：

```text
placeholder
```

---

### 6.7 Release / Hotfix Gate

触发场景：

* release 分支
* hotfix 分支
* tag
* 版本号
* 热更
* 回滚

检查方向：

* 是否从正确分支拉出
* 是否合回 main / develop
* 是否打 tag
* 是否记录验证证据
* 是否存在未回灌 develop 的 hotfix
* 是否符合 release freeze 规则

当前状态：

```text
placeholder
```

---

### 6.8 QA / Regression Gate

触发场景：

* 真实 Bug 反复出现
* regression 新增
* release 前验收
* stable tag 前验收

检查方向：

* 是否有 regression case
* 是否记录复现步骤
* 是否记录修复验证
* 是否纳入回归套件
* 是否阻止同类问题复发

当前状态：

```text
placeholder
```

---

## 7. Future Gate 激活条件

任何 Future Gate 不允许因为"看起来专业"而激活。

必须满足至少一个条件：

1. 同类问题在真实任务中重复出现 2 次以上；
2. metrics 显示某类风险持续上升；
3. 某类问题造成已完成任务返工；
4. 某类问题导致 release / hotfix 风险；
5. 当前人工 Checklist 已无法稳定覆盖；
6. 对应 Gate 能定义明确输入、检查项、失败策略和输出证据；
7. 能至少设计 1 个 regression case 验证该 Gate。

激活流程：

```text
真实断裂点
→ retrospective 归因
→ Gate proposal
→ regression case
→ skill patch
→ 真实任务验证
→ active gate
```

---

## 8. 与 v1.8 的关系

v1.8 关注的是自动检查当前 full / quick 任务是否合规完成。

本文关注的是完整游戏客户端开发领域中，当前工作线覆盖了哪些环节，未来还要补哪些领域能力。

v1.8 不补完整客户端生命周期。本文也不改变 v1.8 的检查器范围。

---

## 9. 当前策略

当前最合理策略：

```text
先补地图，不补流程。
先记录缺口，不激活 Gate。
先看真实断裂，再做领域强化。
```

不要做：

* 一次性补齐所有客户端流程
* 一次性激活所有 Unity Gate
* 把 UI / Network / Performance 全塞进 full 模式
* 把工作线变成完整游戏研发平台
* 用文档复杂度代替真实验证

---

## 10. 结论

当前工作线已经覆盖游戏客户端功能交付的核心段：

```text
需求 / Bug
→ 技术拆分
→ 代码实现
→ 编译验证
→ 代码审查
→ Unity Play
→ Git Evidence
→ Metrics / Retro
```

但它不是完整游戏客户端研发平台。

未来游戏客户端完整领域能力应通过：

```text
Lifecycle Coverage Map
→ Future Gate Backlog
→ 真实断裂点
→ regression
→ active gate
```

逐步补充。

当前结论：

> 客户端完整流程先作为领域地图存在，不作为当前执行流程存在。
