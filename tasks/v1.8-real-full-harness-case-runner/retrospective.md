# retrospective — v1.8 harness case runner

## 面试表达
> 为 v1.8 harness checker 新增了测试运行器，自动运行 4 个 fixture case 并校验预期 exit code。这是一个典型的 full 模式任务——先写 SDD，通过 Conflict Gate 确认范围，再实现，最后用 checker 检查自己的产物。

## 可复用经验
- 4 个 fixture case 定义清晰，runner 实现简单
- full 任务产物被自己的 checker 验证通过
