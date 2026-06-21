using Cysharp.Threading.Tasks;
using UnityEngine;
using System.Threading;

/// <summary>
/// Task 1.4: CancellationToken 的三种用法
/// 这是 UniTask 最核心的安全机制
/// </summary>
public class CancellationDemo : MonoBehaviour
{
    // ========== 场景 1: 绑定 GameObject 生命周期 ==========
    // 物体销毁 → 异步自动取消，不会报 "物体已销毁" 错误
    private async UniTaskVoid AutoCancelOnDestroy()
    {
        // 方式 A: GetCancellationTokenOnDestroy (UniTask 提供，兼容旧版 Unity)
        var token1 = this.GetCancellationTokenOnDestroy();

        // 方式 B: Unity 2022.2+ 原生（推荐，如果你的 Unity 版本够新）
        var token2 = this.destroyCancellationToken;

        // 两种都可以，选一种
        while (!token2.IsCancellationRequested)
        {
            Debug.Log("[Demo] 心跳...");
            await UniTask.Delay(1000, cancellationToken: token2);
        }
        Debug.Log("[Demo] 物体已销毁，循环结束");
    }

    // ========== 场景 2: 手动取消（比如点击取消按钮） ==========
    private CancellationTokenSource _loadCts;

    public async UniTask StartLoading(CancellationToken userToken)
    {
        // 先取消上次的加载
        _loadCts?.Cancel();
        _loadCts?.Dispose();
        _loadCts = new CancellationTokenSource();

        // 合并：用户取消 OR 物体销毁 → 任一触发即取消
        var linkedToken = CancellationTokenSource
            .CreateLinkedTokenSource(userToken, _loadCts.Token);

        try
        {
            Debug.Log("[Demo] 开始加载...");
            await UniTask.Delay(5000, cancellationToken: linkedToken.Token);
            Debug.Log("[Demo] 加载完成！");
        }
        catch (OperationCanceledException)
        {
            Debug.Log("[Demo] 加载被取消");
        }
        finally
        {
            linkedToken.Dispose();
        }
    }

    public void CancelLoading()
    {
        _loadCts?.Cancel();
        Debug.Log("[Demo] 用户点击了取消");
    }

    // ========== 场景 3: 优雅取消（不抛异常） ==========
    private async UniTask GracefulCancellation(CancellationToken token)
    {
        // SuppressCancellationThrow: 返回 (是否被取消, 原始结果)
        // 优点: 不抛异常，零开销，逻辑分支清晰
        var (isCanceled, _) = await UniTask.Delay(3000, cancellationToken: token)
            .SuppressCancellationThrow();

        if (isCanceled)
        {
            Debug.Log("[Demo] 被取消了，做清理工作...");
            // 在这里做清理：隐藏加载 UI、恢复按钮状态等
            return;
        }

        Debug.Log("[Demo] 正常完成，做后续处理...");
    }

    // ========== 使用入口 ==========
    private void Start()
    {
        // 启动自动取消的循环
        AutoCancelOnDestroy().Forget();

        // 模拟：3秒后手动取消
        StartLoading(this.GetCancellationTokenOnDestroy()).Forget();
        Invoke(nameof(CancelLoading), 3f);
    }

    private void OnDestroy()
    {
        // 清理（UniTask 自动取消会处理大部分，但手动创建的 Cts 需要清理）
        _loadCts?.Dispose();
    }
}
