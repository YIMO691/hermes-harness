# tests/

可执行测试夹具和 runner。

## 放什么

- checker fixtures（harness_check/）
- golden reports（HarnessCheckReport.md）
- test runner（run_harness_check_cases.py）

## 不放什么

- 回归场景定义 → 放 `regression/`
- 真实任务证据 → 放 `tasks/`

## 与 regression/ 的关系

```
tests/      = machine-executable verification (runner + fixtures)
regression/ = test specification (design documents)
```

## 运行

```bash
python tests/harness_check/run_harness_check_cases.py
```
