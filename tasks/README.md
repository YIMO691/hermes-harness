# tasks/

真实工作线任务证据包。

## 放什么

- 真实 quick 任务证据
- 真实 full 任务证据
- Git workflow 演练任务（含 PullRequest.md）

## 不放什么

- checker fixture → 放 `tests/`
- 回归场景定义 → 放 `regression/`
- 评估报告 → 放 `docs/evaluations/`

## Quick 任务证据包

```
tasks/<version>/<task-id>/
├── WorklineSummary.md
├── metrics-lite.yaml
└── HarnessCheckReport.md
```

Git workflow 演练额外包含：

```
└── PullRequest.md
```

## Full 任务证据包

```
tasks/<version>/<task-id>/
├── TaskSpec.md
├── SDD.md
├── ConflictReport.md
├── REVIEW.md
├── ChangedFiles.md
├── TestReport.md
├── RiskReport.md
├── metrics.yaml
├── retrospective.md
└── HarnessCheckReport.md
```

## 命名规则

- 目录名：`v<version>-<mode>-<description>`
- 按版本归档：`tasks/v1.8/`、`tasks/v1.9/`、`tasks/v1.10/`
