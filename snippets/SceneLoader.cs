using Cysharp.Threading.Tasks;
using UnityEngine;
using UnityEngine.SceneManagement;
using System;
using System.Threading;

/// <summary>
/// Task 1.3: 异步场景加载器
/// 演示: 进度汇报 + 超时 + 取消 + 返回值
/// </summary>
public class SceneLoader : MonoBehaviour
{
    /// <summary>
    /// 加载场景，返回是否成功
    /// </summary>
    /// <param name="sceneName">场景名</param>
    /// <param name="timeoutSeconds">超时秒数</param>
    /// <param name="onProgress">进度回调 0~1</param>
    /// <param name="cancellationToken">取消令牌</param>
    public async UniTask<bool> LoadSceneAsync(
        string sceneName,
        float timeoutSeconds = 30f,
        Action<float> onProgress = null,
        CancellationToken cancellationToken = default)
    {
        // 1. 开始异步加载（不允许自动激活场景）
        var asyncOp = SceneManager.LoadSceneAsync(sceneName);
        if (asyncOp == null)
        {
            Debug.LogError($"[SceneLoader] 场景 '{sceneName}' 不存在或无法加载");
            return false;
        }

        asyncOp.allowSceneActivation = false;

        // 2. 用 UniTask 的进度创建器汇报进度
        var progress = Progress.Create<float>(p =>
        {
            onProgress?.Invoke(p);
        });

        try
        {
            // 3. 等待加载到 90% 或超时
            //    Unity 的 LoadSceneAsync 在 allowSceneActivation=false 时会停在 0.9
            await UniTask.WaitUntil(
                () => asyncOp.progress >= 0.9f,
                PlayerLoopTiming.Update,
                cancellationToken
            ).Timeout(TimeSpan.FromSeconds(timeoutSeconds));

            // 4. 加载完成，激活场景
            onProgress?.Invoke(1.0f);
            asyncOp.allowSceneActivation = true;

            // 5. 等待场景真正激活（这一帧）
            await UniTask.Yield(cancellationToken);

            Debug.Log($"[SceneLoader] 场景 '{sceneName}' 加载成功");
            return true;
        }
        catch (OperationCanceledException)
        {
            Debug.Log($"[SceneLoader] 场景加载被取消: {sceneName}");
            return false;
        }
        catch (TimeoutException)
        {
            Debug.LogError($"[SceneLoader] 场景加载超时 ({timeoutSeconds}s): {sceneName}");
            return false;
        }
    }

    // ========== 使用示例 ==========
    private async void Start()
    {
        var token = this.GetCancellationTokenOnDestroy();

        var success = await LoadSceneAsync(
            sceneName: "BattleScene",
            timeoutSeconds: 15f,
            onProgress: p => Debug.Log($"[UI] 加载进度: {p * 100:F0}%"),
            cancellationToken: token
        );

        if (success)
            Debug.Log("进入战斗场景！");
        else
            Debug.Log("加载失败，停留在当前场景");
    }
}
