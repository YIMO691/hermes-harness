# Harness 发展路线图

> 当前：Level 1 Harness v1.4.1-stable
> 目标：Level 3（指标驱动 + 自动沉淀）

---

## 第一步：补数据基础

### 当前问题

3 次复盘全是 markdown 自由格式，无法对比。需要结构化。

### 操作

**Step 1.1 — 自动产出 metrics.yaml**

在 workline-execution skill 的 Phase 8 复盘段加一步：

```markdown
### 8b. 产出结构化 metrics

每次 Phase 8 完成后，Hermes 产出 `retrospectives/<task-id>-metrics.yaml`：

```yaml
task: <任务名>
workline_version: <版本号>
started_at: <ISO时间>
phases:
  - phase: P0
    passed: true/false
  - phase: P4
    delegated: true/false
    subagent_calls: <次数>
  - phase: P5
    compile_errors: <数量>
    fix_loops: <次数>
  - phase: P7
    verdict: APPROVED/CONDITIONAL/REJECTED
    reports_missing: <缺了几份>
    rework_loops: <次数>
  - phase: P8
    user_verified: true/false
    bug_found: true/false
violations:
  herm-write-code: <次数>
  skip-review: <次数>
  skip-audit: <次数>
total_duration_minutes: <分钟>
```

### 预计效果

攒够 3 份 metrics 后可以回答：
- 哪个阶段最慢？
- compile_errors 趋势下降？
- violations 归零了吗？

### 依赖

无。在已有复盘流程上多一步。

---

## 第二步：跑 2 个新任务

### 目标

攒够 3 份 metrics（已有 ET6 v3 + BackpackDemo，再跑 2 个）

### 任务建议

| 任务 | 类型 | 测试重点 |
|:---|:---|:---|
| Unity GC 优化小任务 | 修复类 | 回路机制（预测会触发 CONDITIONAL） |
| Unity UI 第二个功能 | 新建类 | 验证 v1.4.1 全部能力无退化 |

**不选大型任务** — Level 1 时期任务是手段，数据是目的。小任务更快出数据。

### 验收

每个任务跑完后同时产生：REVIEW / ChangedFiles / TestReport / RiskReport / ObsidianNote / metrics.yaml

---

## 第三步：首次指标分析

### 操作

攒够 3 份 metrics 后，Hermes 跑一次横向对比：

```yaml
对比维度：
  - compile_errors 趋势（上升/下降/稳定）
  - rework_loops 趋势
  - violations 是否清零
  - 每 task 耗时趋势
  - 审查发现 Bug 频率
```

产出：`retrospectives/LEVEL1_METRICS_REVIEW.md`

### 决策点

| 发现 | 行动 |
|:---|:---|
| 某 GATE 连续 3 次 100% 通过 | 降级为自动检查（不减质量，减人工等待） |
| 某 violation 连续 2 次出现 | 升级约束（从 skill 禁令 → 下次考虑系统级拦截） |
| compile_errors 趋势下降 | 说明 Phase 0/4 audit 有效 |
| 审查发现 Bug 数稳定 | 说明审查 GATE 必要，不降级 |

---

## 第四步：Level 2 → Level 3

### Level 2 就位条件

- 3+ 份 metrics.yaml
- 一次结构化的指标分析
- 基于指标做出至少一个 GATE 调整决策

### Level 3 需要什么

Level 3 = 自动沉淀。复盘自动 patch skill。需要：
- 断裂点与 skill 的映射表（哪个断裂→哪个 skill→哪个 section）
- patch 的 old_string/new_string 自动生成（基于固定的 skill 文本结构）
- 人工 review → merge 的流程

**这需要 schema 设计，不是当前能做的。** Level 2 跑稳了再开始。

---

## 时间线

```
现在 ── Step 1.1（patch workline 加 metrics）──── 10 分钟
     ↓
     Step 2（跑 2 个新任务）────────────────── 2 个 session
     ↓
     Step 3（指标分析）───────────────────────── 30 分钟
     ↓
     Step 4（Level 3 设计）──────────────────── 另议
```
