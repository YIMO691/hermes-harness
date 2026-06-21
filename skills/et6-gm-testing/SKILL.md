---
name: et6-gm-testing
description: ET6 GM panel testing guide — item IDs, panel matrix, test patterns for nerve/raffle/DNA modules. Use when testing ET6 modules with insufficient in-game resources or when GM commands are needed to set up test conditions.
tags: [et6, gm, testing, unity]
triggers:
  - "GM测试"
  - "加材料"
  - "改钻石"
  - "改境界"
  - "GM面板"
  - "怎么测试"
platforms: [windows]
---

# ET6 GM Testing

Complete guide at: `workline-execution/references/et6-gm-testing.md`

## Quick reference

| 需求 | GM入口 | 操作 |
|:---|:---|:---|
| 加钻石（抽奖消耗） | 数值 | 普通钻石 → 20000 |
| 加神经解锁材料 | 添加物资 | ID=102, 数量=999 |
| 加神经升级材料 | 添加物资 | ID=101, 数量=999 |
| 满足解锁条件 | 境界 | 点高境界 → 升级 |
| 验证属性变化 | 属性 → 神经系统分类 | 看数值 |
| DNA参考 | DNA | 解锁/升级/升星按钮 |

## GM panel matrix

| 入口 | 功能 | 可用 |
|:---|:---|:--:|
| 数值 | 钻石/经验/标记 | ✅ |
| 属性 | 所有系统属性（含神经系统分类） | ✅ 只读 |
| 境界 | 改境界时期+升级 | ✅ |
| DNA | DNA解锁/升级/升星 | ✅ |
| 添加物资 | 输入ID+数量加物品 | ✅ |
| 系统测试 | Test1~Test5 | ❌ 空壳 |

## Test patterns

### Nerve: 境界 → 加材料(102+101) → 游戏UI → 属性验证
### Raffle: 数值(钻石20000) → 游戏UI → 单抽/十连/保底
### Boundary: 消耗材料到0 → 验证不足提示
