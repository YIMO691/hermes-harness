# Regression 03：Python 修复（非 Unity）

类型：非 Unity 修复
项目：obsidian-normalizer
验证能力：跨技术栈通用性 + 文件安全

## 任务摘要
修复 obsidian_note_normalizer.py 中的 8 个 bug。

## 预期状态
- 0 第三方依赖
- 21 个 pytest 测试通过
- dry-run 验证不写文件
- 4 份报告齐全

## 退化检查点
- 是否处理非 .md 文件
- dry-run 是否真的不写文件
- 是否保护代码块内容
- pytest 是否真实执行

## 参考
项目：obsidian-normalizer
metrics：2026-06-21-obsidian-normalizer-metrics.yaml
