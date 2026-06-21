# Workline Regression Suite

每次升级 workline skill 后，跑一遍确认已有能力不退化。

## 运行方式

```text
1. git checkout <new-version-branch>
2. 按顺序跑以下 5 个任务
3. 每个任务的标准不是"一次通过"而是"达到预期状态"
4. 全部通过 → merge + tag 稳定版
5. 任一退化 → 修复后再升
```

## 用例

| # | 名称 | 类型 | 预期结果 | 验证能力 |
|:--|:---|:---|:---|:---|
| 01 | `unity-new-feature` | Unity 新建 | APPROVED | SDD + 编码 + 越权检查 |
| 02 | `unity-gc-fix` | Unity 修复 | APPROVED | 修复类 + 作用域约束 |
| 03 | `python-normalizer` | 非 Unity 修复 | APPROVED | 非 Unity 通用性 |
| 04 | `conflict-gate` | 冲突检测 | BLOCKED | Phase 3.5b 拦截 |
| 05 | `conditional-loop` | 回路压测 | CONDITIONAL→APPROVED | Loop 机制 |
