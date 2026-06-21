using UnityEngine;

/// <summary>
/// 统一资源加载接口 — 业务代码不直接依赖 Addressables 或 YooAsset。
/// 目标：切换底层资源系统时，只需替换实现，业务代码零改动。
///
/// 来源: [[Addressables-vs-YooAsset]] 对比笔记中提炼
/// </summary>
public interface IAssetLoader
{
    /// <summary>异步加载资源</summary>
    Cysharp.Threading.Tasks.UniTask<T> LoadAssetAsync<T>(string address) where T : Object;

    /// <summary>异步加载场景</summary>
    Cysharp.Threading.Tasks.UniTask LoadSceneAsync(string sceneAddress);

    /// <summary>异步实例化 GameObject（自动追踪引用计数）</summary>
    Cysharp.Threading.Tasks.UniTask<GameObject> InstantiateAsync(string address, Vector3? position = null, Quaternion? rotation = null, Transform parent = null);

    /// <summary>释放资源引用</summary>
    void Release(string address);

    /// <summary>获取需要下载的大小（字节）</summary>
    Cysharp.Threading.Tasks.UniTask<long> GetDownloadSizeAsync();

    /// <summary>下载所有远程资源</summary>
    Cysharp.Threading.Tasks.UniTask DownloadAsync(IProgress<float> progress = null);
}

/// <summary>
/// 用于 Addressables 的实现，见 AddressablesDemo/AssetLoaderService.cs
/// 用于 YooAsset 的实现，见 YooAssetDemo/AssetLoaderService.cs
/// </summary>
