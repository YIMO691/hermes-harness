using System;
using System.Collections.Generic;

/// <summary>
/// T2.1: 简化版事件总线
/// 参考: GameFramework.Event
/// 核心设计:
///   1. 发布者不认识订阅者 — 通过事件类型解耦
///   2. 零依赖 — 不需要继承 MonoBehaviour 或任何基类
///   3. 类型安全 — 每个事件类型独立 channel
///
/// 用法:
///   EventBus.Subscribe<EnemyKilledEvent>(OnEnemyKilled);
///   EventBus.Fire(new EnemyKilledEvent { enemyId = 1, score = 100 });
///   EventBus.Unsubscribe<EnemyKilledEvent>(OnEnemyKilled);
/// </summary>
public static class EventBus
{
    // 每个事件类型 → 订阅者列表
    private static readonly Dictionary<Type, Delegate> _subscribers = new();

    /// <summary>订阅事件</summary>
    public static void Subscribe<T>(Action<T> callback)
    {
        var type = typeof(T);
        if (_subscribers.ContainsKey(type))
            _subscribers[type] = Delegate.Combine(_subscribers[type], callback);
        else
            _subscribers[type] = callback;
    }

    /// <summary>取消订阅</summary>
    public static void Unsubscribe<T>(Action<T> callback)
    {
        var type = typeof(T);
        if (_subscribers.TryGetValue(type, out var del))
        {
            del = Delegate.Remove(del, callback);
            if (del == null)
                _subscribers.Remove(type);
            else
                _subscribers[type] = del;
        }
    }

    /// <summary>触发事件 — 所有订阅者同步收到</summary>
    public static void Fire<T>(T args)
    {
        if (_subscribers.TryGetValue(typeof(T), out var del))
            (del as Action<T>)?.Invoke(args);
    }

    /// <summary>清空所有订阅（切换场景时调用）</summary>
    public static void Clear()
    {
        _subscribers.Clear();
    }
}

// ====== 使用示例 ======
public struct EnemyKilledEvent
{
    public int enemyId;
    public int score;
}

public struct ItemAcquiredEvent
{
    public int itemId;
    public int count;
}

public class ScoreManager
{
    private int _totalScore;

    public ScoreManager()
    {
        EventBus.Subscribe<EnemyKilledEvent>(OnEnemyKilled);
    }

    private void OnEnemyKilled(EnemyKilledEvent e)
    {
        _totalScore += e.score;
    }

    public void Dispose()
    {
        EventBus.Unsubscribe<EnemyKilledEvent>(OnEnemyKilled);
    }
}
