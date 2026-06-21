# ET6 Project Paths & Directory Structure

> Project root: `D:\Edge下载文件\【深圳热区网络】游戏开发工程师测试题\【深圳热区网络】游戏开发工程师测试题\project\ET6\`

## Quick Reference

| Component | Path |
|:---|:---|
| Server solution | `Server/Server.sln` |
| Server Model | `Server/Model/Server/GameServer/Player/<ComponentName>/` |
| Server Hotfix | `Server/Hotfix/Server/GameServer/PlayerSystem/<ComponentName>System/` |
| Client Model | `Unity/Codes/Model/Client/Player/<ComponentName>/` |
| Client Hotfix | `Unity/Codes/Hotfix/Client/PlayerSystem/<ComponentName>System/` |
| Client ModelView | `Unity/Codes/ModelView/Client/<DlgName>/` |
| Client HotfixView | `Unity/Codes/HotfixView/Client/<DlgName>/<DlgSubName>/` |
| Config (generated) | `Unity/Codes/Model/Generate/Config/<ConfigName>.cs` |
| ConfigPartial | `Unity/Codes/Model/Generate/ConfigPartial/<ConfigName>.cs` |
| Server Config | `Server/Model/Generate/Config/<ConfigName>.cs` |
| Server ConfigPartial | `Server/Model/Generate/ConfigPartial/<ConfigName>.cs` |

## Nerve Module File Inventory

### Server (5 files)
```
Server/Model/.../PlayerNerveComponent/PlayerNerveComponent.cs    ← Component (2 dicts)
Server/Hotfix/.../PlayerNerveComponentSystem/PlayerNerveComponentSystem.cs  ← IsCan+Do
Server/Hotfix/.../PlayerNerveComponentSystem/PlayerNerveComponentNetLogic.cs ← 3 handlers
Server/Hotfix/.../PlayerNerveComponentSystem/PlayerNerveComponentEvent.cs    ← lifecycle
```

### Client Hotfix (2 files)
```
Unity/Codes/Hotfix/.../PlayerNerveComponentSystem/PlayerNerveComponentEvent.cs
Unity/Codes/Hotfix/.../PlayerNerveComponentSystem/PlayerNerveComponentSystem.cs  ← client helpers
```

### HotfixView — 7 sub-windows (14 files)
```
Unity/Codes/HotfixView/Client/DlgNerve/
  DlgNerveMain/DlgNerveMainSystem.cs + DlgNerveMainEvent.cs
  DlgNerveLock/DlgNerveLockSystem.cs + DlgNerveLockEvent.cs
  DlgNerveActive/DlgNerveActiveSystem.cs + DlgNerveActiveEvent.cs
  DlgNerveInfo/DlgNerveInfoSystem.cs + DlgNerveInfoEvent.cs
  DlgNerveGrow/DlgNerveGrowSystem.cs + DlgNerveGrowEvent.cs
  DlgNerveLayeractivation/DlgNerveLayeractivationSystem.cs + DlgNerveLayeractivationEvent.cs
  DlgNerveFinish/DlgNerveFinishSystem.cs + DlgNerveFinishEvent.cs
```

### ModelView — 7 Entity files
```
Unity/Codes/ModelView/Client/DlgNerve/
  DlgNerveMain.cs, DlgNerveLock.cs, DlgNerveActive.cs,
  DlgNerveInfo.cs, DlgNerveGrow.cs, DlgNerveLayeractivation.cs, DlgNerveFinish.cs
```

### Config
```
Unity/Codes/Model/Generate/Config/NerveConfig.cs, NerveMouldConfig.cs, NerveTierConfig.cs
Unity/Codes/Model/Generate/ConfigPartial/NerveConfig.cs, NerveMouldConfig.cs, NerveTierConfig.cs
```

## Raffle Module File Inventory

### Server (4 files, note underscore naming)
```
Server/Model/.../PlayerRaffleComponent/PlayerRaffleComponent.cs
Server/Hotfix/.../PlayerRaffleComponentSystem/PlayerRaffleComponentSystem.cs
Server/Hotfix/.../PlayerRaffleComponentSystem/PlayerRaffleComponent_NetLogic.cs
Server/Hotfix/.../PlayerRaffleComponentSystem/PlayerRaffleComponentEvent.cs
```

### Client Hotfix
```
Unity/Codes/Hotfix/.../PlayerRaffleComponentSystem/PlayerRaffleComponentEvent.cs
Unity/Codes/Hotfix/.../PlayerRaffleComponentSystem/PlayerRaffleComponentSystem.cs
```

### HotfixView — 5 sub-windows (10 files)
```
Unity/Codes/HotfixView/Client/DlgRaffle/
  DlgRaffleMainSystem.cs + Event, DlgRafflePageSystem.cs + Event,
  DlgRaffleObtainSystem.cs + Event, DlgRafflePreviewSystem.cs + Event,
  DlgRaffleTipsSystem.cs + Event
```

### ModelView — 5 Entity files
```
Unity/Codes/ModelView/Client/DlgRaffle/
  DlgRaffleMain.cs, DlgRafflePage.cs, DlgRaffleObtain.cs,
  DlgRafflePreview.cs, DlgRaffleTips.cs
```

### Config
```
Unity/Codes/Model/Generate/Config/RaffleConfig.cs
Unity/Codes/Model/Generate/ConfigPartial/RaffleConfig.cs
```

## Compilation Commands

```bash
# Server (MUST run from project ROOT, not Server/ subdirectory)
cd "<PROJECT_ROOT>"
dotnet build Server.sln

# Correct output: "已成功生成。0 个警告 0 个错误"
# Wrong (MSB1003): cd "<PROJECT_ROOT>/Server" && dotnet build
#   → "请指定项目或解决方案文件。当前工作目录中未包含项目或解决方案文件"

# HybridCLR cache clear (after source changes, PowerShell syntax)
Remove-Item -Recurse -Force "<PROJECT_ROOT>/Unity/Library/ScriptAssemblies/" -ErrorAction SilentlyContinue
Remove-Item -Force "<PROJECT_ROOT>/Unity/Assets/Bundles/Code/Code.dll.bytes" -ErrorAction SilentlyContinue
Remove-Item -Force "<PROJECT_ROOT>/Unity/Assets/Bundles/Code/MonoHotUpdate.dll.bytes" -ErrorAction SilentlyContinue

# Then in Unity Editor: Tools → Build → BuildCodeDebug
```

## Test Workspace (DO NOT CONFUSE WITH PROJECT)
```
C:\Users\20544\Desktop\测试\  ← Analysis workspace, NOT the compiled project
C:\Users\20544\Desktop\测试\code\  ← Standalone code copies, may be stale
```

**Golden rule**: The compiled project is the source of truth. Before writing any file, verify whether it already exists in the project.
