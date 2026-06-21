using System;
using System.Collections.Generic;

/// <summary>
/// T2.3: 简化版状态机
/// 参考: GameFramework.Procedure / GameFramework.FSM
/// 核心设计:
///   1. 状态接口 IState: Enter / Tick / Exit
///   2. 状态机只负责切换 + 驱动当前状态
///   3. 状态之间不知道彼此 — 由状态机统一管理
///
/// 适用场景:
///   - 游戏流程: Title → Loading → Lobby → Battle → Result
///   - 敌人 AI:  Idle → Patrol → Chase → Attack → Dead
///   - UI 面板:  Closed → Opening → Open → Closing → Closed
///
/// 用法:
///   var fsm = new StateMachine();
///   fsm.AddState(new IdleState());
///   fsm.AddState(new BattleState());
///   fsm.ChangeState<IdleState>();
///   fsm.Tick(Time.deltaTime);  // 每帧调用
/// </summary>

/// <summary>状态接口</summary>
public interface IState
{
    /// <summary>进入状态时调用一次</summary>
    void Enter();

    /// <summary>每帧调用</summary>
    void Tick(float deltaTime);

    /// <summary>离开状态时调用一次</summary>
    void Exit();
}

/// <summary>泛型状态机 — T 是状态类型（通常是枚举）</summary>
public class StateMachine
{
    private readonly Dictionary<Type, IState> _states = new();
    private IState? _current;
    private Type? _currentType;

    /// <summary>当前状态类型</summary>
    public Type? CurrentState => _currentType;

    /// <summary>注册状态</summary>
    public void AddState<T>(T state) where T : IState
    {
        _states[typeof(T)] = state;
    }

    /// <summary>切换状态</summary>
    public void ChangeState<T>() where T : IState
    {
        var newType = typeof(T);
        if (!_states.TryGetValue(newType, out var newState))
            throw new InvalidOperationException($"状态未注册: {newType.Name}");

        _current?.Exit();
        _current = newState;
        _currentType = newType;
        _current.Enter();
    }

    /// <summary>每帧驱动当前状态</summary>
    public void Tick(float deltaTime)
    {
        _current?.Tick(deltaTime);
    }
}

// ====== 使用示例: 游戏流程状态机 ======
public enum GameFlow { Title, Lobby, Battle, Result }

public class TitleState : IState
{
    public void Enter()  { /* 显示标题UI */ }
    public void Tick(float dt) { /* 检测点击开始 */ }
    public void Exit()   { /* 隐藏标题UI */ }
}

public class BattleState : IState
{
    public void Enter()  { /* 加载战斗场景、生成敌人 */ }
    public void Tick(float dt) { /* 更新战斗逻辑 */ }
    public void Exit()   { /* 清理战场 */ }
}

public class GameFlowController
{
    private StateMachine _fsm = new();

    public GameFlowController()
    {
        _fsm.AddState<TitleState>(new TitleState());
        _fsm.AddState<BattleState>(new BattleState());
    }

    public void Start()
    {
        _fsm.ChangeState<TitleState>();
    }

    public void Update(float dt)
    {
        _fsm.Tick(dt);
    }

    public void StartBattle()
    {
        _fsm.ChangeState<BattleState>();
    }
}

// ====== 进阶: 带参数的泛型状态机（支持上下文注入） ======
public interface IState<in TContext>
{
    void Enter(TContext context);
    void Tick(float deltaTime);
    void Exit();
}

public class StateMachine<TContext>
{
    private readonly Dictionary<Type, IState<TContext>> _states = new();
    private IState<TContext>? _current;
    private readonly TContext _context;

    public StateMachine(TContext context)
    {
        _context = context;
    }

    public void AddState<T>(T state) where T : IState<TContext>
    {
        _states[typeof(T)] = state;
    }

    public void ChangeState<T>() where T : IState<TContext>
    {
        var newType = typeof(T);
        _current?.Exit();
        _current = _states[newType];
        _current.Enter(_context);
    }

    public void Tick(float dt) => _current?.Tick(dt);
}
