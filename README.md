# Hermes Harness — Personal SDD-Harness Workline

> A personal AI Agent engineering harness for structured task execution, safe office onboarding, and evidence-driven governance.

![Version](https://img.shields.io/badge/version-v1.11--office--onboarding--stable-blue)
![Status](https://img.shields.io/badge/status-Stable%20Personal%20Harness-green)
![CI](https://img.shields.io/badge/CI-passing-brightgreen)
![Scope](https://img.shields.io/badge/scope-no%20LangGraph%20%7C%20no%20Dashboard-lightgrey)

---

## Current Stable Version

```
v1.11-office-onboarding-stable
```

## What This Is

这是一个个人 Agent Engineering / SDD-Harness 工作线仓库。它不是一个公司工具，不是自动化开发替代品，而是一套**帮助你安全、结构化地执行开发任务的个人管线**。

v1.10 形成了 canonical baseline（Intake / AUTO-BLOCK / Coverage / Experience Injection）。v1.11 在 v1.10 外面增加 **Office Onboarding 安全壳**，解决公司入职场景下"规范未知、权限未知、信息安全未知"的问题。

## Why v1.11

| 场景 | v1.10 | v1.11 |
|:---|:---|:---|
| 个人测试题（HotZoneTestC） | ✅ 完整管线 | ✅ 与 v1.10 兼容 |
| 公司入职第一周 | ❌ 假设已知规范/可写入 | ✅ safe-note：脱敏笔记 + 提问 |
| 公司允许个人笔记 | ❌ 无中间模式 | ✅ office-lite：需求拆解，不触代码 |
| 公司明确允许 Agent | — | ✅ full-harness：限定范围，需授权 |

## Architecture

```
┌──────────────────────────────────────┐
│  v1.11 Office Onboarding Safety Layer │  ← 新（4 modes + 5 gates）
│  ┌────────────────────────────────┐  │
│  │  v1.10 Canonical Baseline      │  │  ← 已完整回填
│  │  Intake / AUTO-BLOCK / Coverage │  │
│  │  / Experience Injection / Core  │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

## Modes

| Mode | Trigger | What You Can Do |
|:---|:---|:---|
| **safe-note** | Company policy unknown | 脱敏笔记、提问话术、日报模板 |
| **office-lite** | Company allows personal notes | + 需求拆解、影响面、验收标准（不触代码） |
| **full-harness** | Company + user authorized | 完整 v1.10 管线（限定目录范围） |
| **personal-lab** | Personal projects | 完整 v1.10 管线（无安全限制） |

## Gates

| Gate | Purpose |
|:---|:---|
| **Company Policy Gate** | Unknown policy → safe-note by default |
| **Sensitive Data Gate** | Auto-redact source code/paths/class names before output |
| **Action Permission Gate** | 6-level action control — L6 (commit/push) always blocked |
| **Persistence Gate** | Block saving company-specific data to files/Obsidian/memory |
| **Mode Switch Gate** | Work/Learn/Think line switching requires manual confirmation |

## Quick Start

### Personal Lab

For ET6 source, HotZoneTestC, DailyReward, personal demos. Full v1.10 capability.

### Office Onboarding

For your first week at a company. Start here:

→ `docs/OFFICE_ONBOARDING_FIRST_WEEK_SOP.md`

### Daily Usage

For everyday lightweight use:

→ `docs/OFFICE_ONBOARDING_DAILY_USAGE_GUIDE.md`

## Key Documents

| Document | Purpose |
|:---|:---|
| `docs/INDEX.md` | Full documentation index |
| `docs/OFFICE_ONBOARDING_WORKLINE_V1.11.md` | v1.11 design rationale |
| `docs/OFFICE_ONBOARDING_FIRST_WEEK_SOP.md` | Day 1–5 onboarding roadmap |
| `docs/OFFICE_ONBOARDING_DAILY_USAGE_GUIDE.md` | Daily template guide |
| `docs/OBSIDIAN_WORK_VAULT_SAFE_STRUCTURE.md` | Obsidian vault safety rules |
| `reports/v1.11/v1.11_office_onboarding_release_notes.md` | Release notes |
| `skills/workline-execution/SKILL.md` | Runtime skill (v1.11.0) |

## Safety Notice

**When company policy is unknown or not confirmed:**

- ❌ Do not scan company project directories
- ❌ Do not read company source code
- ❌ Do not invoke Codex to modify company code
- ❌ Do not send company details to ChatGPT
- ❌ Do not save company-specific information

**Default mode in company context: safe-note.**

## Repository Status

```
v1.11-office-onboarding-stable — 4 modes, 5 gates, 6 templates, 6 regression cases
              ↓
v1.10 canonical baseline — Intake / AUTO-BLOCK ×4 / Coverage / Experience Injection
              ↓
v1.9-stable — CI + Regression 10/10
v1.8-stable — Harness Checker
v1.7-stable — Workline Core (Mode Router + Conflict Gate)
```

- Office onboarding regression cases are `[MANUAL_VERIFY]`
- Full audit chain: Phase 0 → Phase 9 (BLOCKED → fix → re-audit PASS)
- CI passes: `python tests/harness_check/run_harness_check_cases.py`
