# LangChain / LangGraph Evaluation for Workline

> 日期: 2026-06-22 | 基于 v1.7 审查

## What They Are

| | LangChain | LangGraph |
|:---|:---|:---|
| Essence | LLM application framework | Stateful multi-agent orchestration framework |
| Core abstraction | Chain / Agent / Tool / Memory | StateGraph (nodes + conditional edges + checkpointing) |
| Best at | Rapid LLM app prototyping | Complex agent state machines + human-in-the-loop |
| Worst at | Complex multi-step state management | Simple one-shot tasks |

## What They CAN Help

1. **State machine formalization**: Replace markdown-described phases with executable StateGraph edges
2. **Human-in-the-loop**: `interrupt()` for Mentor gates (user must approve before continuing)
3. **Checkpointing**: SQLite/Postgres persistence for session recovery
4. **Observability**: Streaming node transitions for dashboard/monitoring

## What They CANNOT Help

| Problem | LangGraph solves? | Why |
|:---|:--:|:---|
| Codex unavailable | No | External API availability |
| Codex hallucinations | No | Model quality, not orchestration |
| Review misses bugs | No | Claude Code capability ceiling |
| User offline | Partial | Can pause, can't make user respond faster |
| Cross-platform compatibility | No | dotnet/Unity are project dependencies |

## When to Introduce

LangGraph should be considered when at least ONE of these fires:

1. CONDITIONAL loops fire 3+ times per task (manual management too complex)
2. User works asynchronously (start task → offline → resume hours later, needs checkpointing)
3. Multiple parallel worklines (2+ tasks, need state isolation)
4. Dashboard monitoring needed (real-time phase/throughput visibility)
5. Level 3 auto-patching needs stable state machine (deterministic node→output mapping)

## Current Verdict: NOT NOW

The Harness Engineering principle is "只加固断裂点" — only reinforce what has actually broken. No current fracture demands LangGraph. The existing markdown description + violation markers + git cover all known fracture points.

LangGraph is a v2.0+ consideration, not a v1.7 concern.
