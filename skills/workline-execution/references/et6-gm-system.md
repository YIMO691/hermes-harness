# ET6 GM 系统

## 客户端 GM 面板

### UIGMRank（可用）
- 路径: `Unity/Codes/HotfixView/Client/UIGm/UIGMRankSystem.cs`
- 功能: 设置境界 + 升级
- 协议: `C2Game_GmSetRank` → `Game2C_GmSetRank`, `C2Game_GmRankLevelUp` → `Game2C_GmRankLevelUp`
- 入口: 游戏内 GM 面板 → Rank 页签

### UIGMTest（空壳）
- 路径: `Unity/Codes/HotfixView/Client/UIGm/UIGMTestSystem.cs`
- 状态: 5个测试按钮（OnClickTest1~5）+ 1个系统测试按钮（OnClickSystemTest）
- 所有 Test1~5 的请求代码被注释掉，仅 OnClickSystemTest 有实际逻辑（显示随机 Tips）
- 输入框: `EIf_Input1`（5个按钮共用同一个输入框）

### ModelView 层
- `Unity/Codes/ModelView/Client/UIGm/UIGMTest.cs` — 窗口 Entity
- `Unity/Codes/ModelView/Client/UIGm/UIGMRank.cs` — 窗口 Entity

## 服务端 GM Handler

### C2Game_GmBagAdd（可用）
- 路径: `Server/Hotfix/.../PlayerBagComponentSystem/PlayerBagComponent_GmLogic.cs`
- 功能: 向背包添加指定物品（ConfigId + Num）
- 权限: 需要 `player.m_bGm == true`
- 响应: `Game2C_GmBagAdd`

### C2Game_GmSetRank（可用）
- 路径: `Server/Hotfix/.../PlayerRankComponentSystem/PlayerRankComponentNetLogic.cs`
- 功能: 设置玩家境界（RankId）
- 调用: `pPlayerRankComponent.GmSetRankPeriod(request.nRankId)`

### C2Game_GmRankLevelUp（可用）
- 路径: 同上
- 功能: 境界等级+1

## Opcode 区间
- GM 协议 opcode 从 10162 开始（`C2Game_GmSetRank`）
- 定义在 `Server/Model/Generate/Message/OuterOpcode.cs`

## 神经/抽奖测试所需的 GM 能力

当前缺失:
1. 加钻石（用于抽奖消耗，钻石ID=1011）
2. 加神经材料（解锁材料ID=102，升级材料ID=101）
3. 直接触发神经解锁/升级/突破的网络请求
4. 直接触发抽奖的网络请求
5. 设置抽奖次数（保底测试）

可行的实现方式:
- 方案A: 在 UIGMTest 的 Test1~5 中填入神经/抽奖 GM 逻辑
- 方案B: 创建独立的 DlgGMNerveRaffle 窗口
- 方案C: 通过 C2Game_GmBagAdd 加材料 + 加钻石，然后用游戏UI正常操作
