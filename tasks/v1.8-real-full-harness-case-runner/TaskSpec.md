# TaskSpec — v1.8 harness case runner

```yaml
task_id: v1.8-real-full-harness-case-runner
title: Add minimal test runner for v1.8 harness check fixtures
task_type: feature
project_type: python_tool
mode: full

context:
  project_root: C:\Users\20544\Desktop\hermes-harness
  related_files:
    - tools/check_workline_task.py
    - tests/harness_check/README.md

goal:
  summary: Add run_harness_check_cases.py to run 4 fixture cases and validate exit codes
  success_definition:
    - runner exits 0 when all 4 cases match expected exit codes
    - runner exits non-zero when any case fails
    - output shows "4/4 harness check cases passed"

non_goals:
  - 不修改 skills/
  - 不修改 regression/
  - 不修改 checker 核心规则
  - 不新增 GitHub Actions
  - 不接 LangChain/LangGraph

allowed_changes:
  ui: false
  protocol: false
  config: false
  asset: false
  public_api: false
  new_files: true
  unrelated_files: false

required_gates:
  - conflict
  - build
  - review

acceptance:
  - runner outputs 4/4 passed
  - runner exit code matches fixture expectations
  - full checker PASS on task directory
```
