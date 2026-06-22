# Hermes Harness Workline

> A personal AI Agent engineering harness for structured task execution, validation, review, evidence tracking, and governance.

![Version](https://img.shields.io/badge/version-v1.9--stable-blue)
![Status](https://img.shields.io/badge/status-Strong%20Personal%20Harness-green)
![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Scope](https://img.shields.io/badge/scope-no%20LangGraph%20%7C%20no%20Dashboard-lightgrey)

---

## 当前版本

```
v1.7-stable → Workline Core (Mode Router + Conflict Gate)
v1.8-stable → Harness Checker (full/quick compliance)
v1.9-stable → CI + Regression 10/10 + Git Workflow Evidence
```

**当前真实等级**：Strong Personal Harness Prototype（接近 Stable Personal Harness，尚未 Production-grade）。

---

## 核心能力

| 能力 | 状态 |
|:---|:--:|
| full / quick Mode Router | ✅ |
| Conflict Gate（唯一 active gate） | ✅ |
| v1.8 Harness Checker | ✅ |
| CI checker（GitHub Actions） | ✅ |
| Regression 10/10 | ✅ |
| Git Workflow 执行证据 | ✅ |
| 治理裁决 | ✅ |
| LangGraph / LangChain | ❌ 未引入 |
| Dashboard / 平台化 | ❌ 不做 |

---

## 仓库结构

```
.github/workflows/   CI — 自动运行 checker
docs/                architecture / plans / evaluations / governance
skills/              runtime skills
tools/               executable tools (checker)
tests/               executable fixtures
regression/          regression specs
tasks/               real task evidence
retrospectives/      retrospectives and metrics
scripts/             auxiliary scripts
snippets/            reusable snippets
```

→ 详细规则：`docs/WORKLINE_REPOSITORY_STRUCTURE.md`

---

## 快速开始

```bash
# 安装依赖
pip install -r requirements-dev.txt

# 运行 checker
python tests/harness_check/run_harness_check_cases.py

# CI 自动触发：push / PR / workflow_dispatch
# 配置：.github/workflows/workline-check.yml
```

---

## 使用流程

```
Task / Bug
  → Mode Router（full / quick）
    → Conflict Gate（仅 full）
      → Agent 执行（Hermes / Codex / Claude Code）
        → Build / Review / Verify
          → Metrics / Retro
            → Git Evidence
```

---

## 文档索引

| 文档 | 用途 |
|:---|:---|
| `docs/WORKLINE_REPOSITORY_STRUCTURE.md` | 仓库结构治理规则 |
| `docs/WORKLINE_ARCHITECTURE_V1.7_STABLE.md` | 稳定架构定义 |
| `docs/WORKLINE_GIT_WORKFLOW.md` | Git 工作流 |
| `docs/V1.8_HARNESS_CHECK_MINIMAL_PLAN.md` | v1.8 checker 方案 |
| `docs/V1.9_CI_REGRESSION_EVIDENCE_PLAN.md` | v1.9 计划 |
| `docs/UNITY_CLIENT_LIFECYCLE_COVERAGE.md` | 游戏客户端覆盖地图 |
| `docs/WORKLINE_FULL_ENGINEERING_EVALUATION.md` | 全量工程评估 |
| `docs/evaluations/v1.8-stable/WORKLINE_GOVERNANCE_VERDICT.md` | v1.8 治理裁决 |
| `docs/evaluations/v1.9-ci-regression-evidence/V1.9_EVIDENCE_REPORT.md` | v1.9 证据报告 |
| `regression/README.md` | 回归套件（10 cases） |
| `skills/workline-execution/SKILL.md` | 运行时 skill |

---

## 路线图

```
v1.7-stable — Workline Core                ✅
v1.8-stable — Harness Checker               ✅
v1.9-stable — CI + Regression + Git Evidence ✅
v1.10 candidate — Token Observability / Health Report
v2.0  — 真实断裂后激活第一个 future Gate
```

---

## 当前不做

- Production-grade Harness
- LangGraph / LangChain
- Dashboard / 平台化
- 新 active Gate
- token observability 实现
- 完整 Unity 客户端生命周期自动化

---

*最后更新：2026-06-22 · v1.9-stable*
