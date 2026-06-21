using System.Collections.Generic;
using System;

/// <summary>
/// T2.5: 简化版 UI 管理器
/// 参考: GameFramework.UI
/// 核心设计:
///   1. 面板注册制 — 每个面板有唯一名称
///   2. 层级管理 — 背景/普通/弹窗/顶层
///   3. 打开/关闭 — 支持参数传递和返回值
///   4. 栈式管理 — 关闭当前面板时自动回到上一个
///
/// 用法:
///   UIManager.Open("ShopPanel");
///   UIManager.Open("ConfirmDialog", new DialogArgs { message = "确定购买?" });
///   UIManager.Close("ConfirmDialog");  // 自动回到 ShopPanel
/// </summary>

/// <summary>面板层级</summary>
public enum UILayer
{
    Background = 0,  // 背景（HUD等）
    Normal = 100,     // 普通（背包、商店）
    Popup = 200,      // 弹窗（确认框、提示）
    Top = 300,        // 顶层（Loading、网络提示）
}

/// <summary>面板基类</summary>
public abstract class UIPanel
{
    public string Name { get; set; } = string.Empty;
    public UILayer Layer { get; set; } = UILayer.Normal;
    public bool IsOpen { get; private set; }

    /// <summary>打开时调用</summary>
    public virtual void OnOpen(object? args = null) { IsOpen = true; }

    /// <summary>关闭时调用</summary>
    public virtual void OnClose() { IsOpen = false; }

    /// <summary>每帧更新（仅当前最上层面板）</summary>
    public virtual void OnUpdate(float dt) { }
}

/// <summary>UI 管理器</summary>
public class UIManager
{
    private readonly Dictionary<string, UIPanel> _panels = new();
    private readonly Stack<string> _panelStack = new();  // 打开历史

    /// <summary>注册面板</summary>
    public void Register(UIPanel panel)
    {
        _panels[panel.Name] = panel;
    }

    /// <summary>打开面板</summary>
    public void Open(string name, object? args = null)
    {
        if (!_panels.TryGetValue(name, out var panel))
            throw new KeyNotFoundException($"面板未注册: {name}");

        if (panel.IsOpen)
        {
            // 已打开 → 提到最前
            BringToFront(name);
            return;
        }

        panel.OnOpen(args);
        _panelStack.Push(name);
    }

    /// <summary>关闭面板</summary>
    public void Close(string name)
    {
        if (!_panels.TryGetValue(name, out var panel)) return;
        if (!panel.IsOpen) return;

        panel.OnClose();

        // 从栈中移除
        var tempStack = new Stack<string>();
        while (_panelStack.Count > 0)
        {
            var top = _panelStack.Pop();
            if (top == name) break;
            tempStack.Push(top);
        }
        while (tempStack.Count > 0)
            _panelStack.Push(tempStack.Pop());
    }

    /// <summary>关闭最上层面板</summary>
    public void CloseTop()
    {
        if (_panelStack.Count > 0)
            Close(_panelStack.Peek());
    }

    /// <summary>将已打开的面板提到最前</summary>
    private void BringToFront(string name)
    {
        var tempStack = new Stack<string>();
        while (_panelStack.Count > 0)
        {
            var top = _panelStack.Pop();
            if (top == name) break;
            tempStack.Push(top);
        }
        while (tempStack.Count > 0)
            _panelStack.Push(tempStack.Pop());
        _panelStack.Push(name);
    }

    /// <summary>每帧更新最上层面板</summary>
    public void Tick(float dt)
    {
        if (_panelStack.TryPeek(out var name) && _panels.TryGetValue(name, out var panel))
            panel.OnUpdate(dt);
    }
}

// ====== 使用示例 ======
public class ShopPanel : UIPanel
{
    public ShopPanel() { Name = "ShopPanel"; Layer = UILayer.Normal; }

    public override void OnOpen(object? args = null)
    {
        base.OnOpen(args);
        // 显示商店UI、加载商品列表
    }

    public override void OnClose()
    {
        base.OnClose();
        // 隐藏商店UI
    }
}

public class ConfirmDialog : UIPanel
{
    public ConfirmDialog() { Name = "ConfirmDialog"; Layer = UILayer.Popup; }

    public override void OnOpen(object? args = null)
    {
        base.OnOpen(args);
        // 显示确认文案和按钮
    }
}

public class ExampleUIUsage
{
    public void Demo()
    {
        var ui = new UIManager();
        ui.Register(new ShopPanel());
        ui.Register(new ConfirmDialog());

        // 打开商店
        ui.Open("ShopPanel");

        // 购买时弹出确认框
        ui.Open("ConfirmDialog", new { message = "确定购买？", price = 100 });

        // 玩家点确认 → 关闭弹窗 → 自动回到商店
        ui.Close("ConfirmDialog");

        // 关掉商店
        ui.Close("ShopPanel");
    }
}
