# Regression 06：Quick Bugfix

类型：quick 模式 Bug 修复
项目：BackpackDemo（或等价 Unity 项目）
验证能力：Mode Router 分流 + Lite 报告 + quick 模式流程

## 任务摘要
给一个已运行的 Unity 项目中的小 Bug——例如：背包排序按钮的 OnClick 事件绑定错误，导致点击无响应。

## 预期状态
- Hermes 内部判断为 quick 模式（单文件修复、无架构决策）
- Hermes 不在回复中要求用户"确认模式"
- 不生成 SDD / PROJECT-ANALYSIS / 4 份完整报告
- 生成 WorklineSummary.md + metrics-lite.yaml
- Codex 修改 1 个文件
- 编译通过
- 功能验证通过（按钮可点击）

## 退化检查点
- TaskSpec 是否未被用户感知（Agent 内部判断，不要求用户交互）
- WorklineSummary.md 是否包含所有必需段
- metrics-lite.yaml 是否完整
- 是否未生成 full 模式的产物
- quick 模式是否明显快于 full 模式
- 如果 Bug 实际上触及以下范围外 → 是否触发 auto-upgrade 到 full：
  - UI（Panel / Prefab / UGUI 控件）
  - 协议（Handler / 请求响应 / 状态同步）
  - 配置（配置表 / 表 ID / 静态数据）
  - 性能（Update / GC / 大量对象 / 资源加载）
  - 资源（AssetBundle / Addressables / Prefab 引用）
  - 平台（IL2CPP / 移动端 / 输入 / 分辨率）
  - 热更（HybridCLR / DLL bytes / BuildCodeDebug）

## 状态
⚠️ NEW — v1.7 新增回归用例，待首次运行
