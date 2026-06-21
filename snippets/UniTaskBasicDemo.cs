using Cysharp.Threading.Tasks;
using UnityEngine;

/// <summary>
/// Task 1.2: UniTask 基础 Demo
/// 演示三种返回类型 + 三种延迟方式 = Coroutine → UniTask 的完整替换
/// </summary>
public class UniTaskBasicDemo : MonoBehaviour
{
    // ========== 方式 1: UniTaskVoid ==========
    // 替代: void Start() + StartCoroutine
    // 注意: MonoBehaviour 的 Start 返回 void 时 Unity 不会自动 await
    // 所以用 UniTaskVoid 时需要 .Forget() 或在内部 await
    private async void Start()
    {
        Debug.Log("[Demo] Start 开始");

        // 1. yield return null → UniTask.Yield()
        await UniTask.Yield();
        Debug.Log("[Demo] 等了一帧 (等价 yield return null)");

        // 2. yield return new WaitForSeconds(1) → UniTask.Delay(毫秒)
        await UniTask.Delay(1000);
        Debug.Log("[Demo] 等了一秒 (等价 WaitForSeconds(1))");

        // 3. yield return new WaitForEndOfFrame → UniTask.WaitForEndOfFrame
        await UniTask.WaitForEndOfFrame(this);
        Debug.Log("[Demo] 帧末执行 (等价 WaitForEndOfFrame)");

        // 演示有返回值的版本
        var result = await GetPlayerNameAsync();
        Debug.Log($"[Demo] 获取到玩家名: {result}");
    }

    // ========== 方式 2: UniTask<T> 有返回值 ==========
    // 替代: Coroutine + Action<string> 回调
    private async UniTask<string> GetPlayerNameAsync()
    {
        // 模拟"等待某帧才能拿到数据"的场景
        await UniTask.Delay(500);
        return "Player_0001";
    }

    // ========== 方式 3: UniTask 无返回值 ==========
    // 替代: IEnumerator 协程
    private async UniTask WaitUntilReady()
    {
        // 等待一个条件成立
        await UniTask.WaitUntil(() => Time.time > 3f);
        Debug.Log("[Demo] 游戏时间超过3秒，准备就绪");
    }

    // ========== 带 CancellationToken 的版本 ==========
    // 这才是生产级写法
    private async UniTask LoadWithCancellation()
    {
        // 获取绑定到 GameObject 销毁的取消令牌
        var token = this.GetCancellationTokenOnDestroy();

        // 模拟加载（如果物体被销毁，自动取消）
        await UniTask.Delay(3000, cancellationToken: token);

        if (token.IsCancellationRequested)
        {
            Debug.Log("[Demo] 物体已销毁，加载中止");
            return;
        }

        Debug.Log("[Demo] 加载完成");
    }
}
