# Harness Check — Test Fixtures

> 版本：v1.0
> 依赖：`tools/check_workline_task.py`
> 目的：`check_workline_task.py` 的最小验证夹具

## 目录结构

```
tests/harness_check/
├── valid_quick/              ← Case 1: 合法 quick 任务 → PASS
├── missing_metrics_lite/     ← Case 2: 缺 metrics-lite.yaml → BLOCKED
├── full_missing_review/      ← Case 3: full 缺 REVIEW.md → BLOCKED
├── result_conflict/          ← Case 4: result 与验证状态冲突 → BLOCKED
└── README.md                 ← 本文件
```

## Golden Reports

各 case 目录下的 `HarnessCheckReport.md` 是 checker 生成的预期输出示例（golden report）。

修改 checker 规则后，必须重新运行 4 个 case 并确认 reports 仍符合预期。如有变化，同步更新这些 reports。

## 运行

```bash
python tools/check_workline_task.py --task tests/harness_check/valid_quick --mode quick
python tools/check_workline_task.py --task tests/harness_check/missing_metrics_lite --mode quick
python tools/check_workline_task.py --task tests/harness_check/full_missing_review --mode full
python tools/check_workline_task.py --task tests/harness_check/result_conflict --mode full
```
