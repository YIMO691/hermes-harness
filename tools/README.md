# tools/

长期维护的可执行工程工具。

## 放什么

- checker（`check_workline_task.py`）
- validator
- report generator

## 不放什么

- 一次性临时脚本 → 放 `scripts/`
- 辅助脚本 → 放 `scripts/`

## 当前工具

| 工具 | 用途 |
|:---|:---|
| `check_workline_task.py` | v1.8 harness checker — 检查 full/quick 任务合规性 |

## 规则

- 如果 `scripts/` 中的脚本被 CI 依赖或长期维护，应升级到 `tools/`
- 新增工具前先查 `docs/WORKLINE_REPOSITORY_STRUCTURE.md`
