"""
UniTask 等效 Python Demo
=========================
UniTask 的核心模式全部映射到 Python async/await。
这些模式在 C# UniTask 中写法几乎一样，只是关键字略有不同。

对照表:
  C# UniTask<T>      →  Python  async def → T
  C# UniTask          →  Python  async def → None
  C# UniTaskVoid      →  Python  asyncio.create_task()  fire-and-forget
  C# CancellationToken → Python  asyncio.CancelledError / Task.cancel()
  C# await UniTask.Delay(ms)           →  await asyncio.sleep(s)
  C# await UniTask.Yield()             →  await asyncio.sleep(0)
  C# await UniTask.WhenAll(a, b)       →  await asyncio.gather(a, b)
  C# await UniTask.WhenAny(a, b)       →  asyncio.wait(FIRST_COMPLETED)
  C# Progress.Create<T>               →  自实现 IProgress 等效回调
"""

import asyncio
import time
from typing import Optional, Callable, Any


# ============================================================
# Task 1.2: 三种返回类型 + 三种延迟
# ============================================================
async def demo_basic_returns():
    """对应 UniTaskBasicDemo.cs — 三种返回类型 + 三种延迟"""
    print("=" * 50)
    print("[Task 1.2] 基础替换演示")
    print("=" * 50)

    # 1. yield return null → await asyncio.sleep(0)
    await asyncio.sleep(0)
    print("[Demo] 等了一帧 (等价 yield return null / UniTask.Yield())")

    # 2. yield return new WaitForSeconds(1) → await asyncio.sleep(1)
    await asyncio.sleep(1)
    print("[Demo] 等了一秒 (等价 WaitForSeconds(1) / UniTask.Delay(1000))")

    # 3. 有返回值的异步方法 (Coroutine 做不到，UniTask 可以)
    name = await get_player_name_async()
    print(f"[Demo] 获取到玩家名: {name}")

    # 4. 无返回值异步方法
    await wait_until_ready(threshold=0.5)

    print("[Task 1.2] ✅ 完成\n")


# UniTask<string>  ← 有返回值
async def get_player_name_async() -> str:
    await asyncio.sleep(0.5)
    return "Player_0001"


# UniTask  ← 无返回值
async def wait_until_ready(threshold: float):
    start = time.time()
    while time.time() - start < threshold:
        await asyncio.sleep(0.1)
    print(f"[Demo] 已等待 {threshold}s，准备就绪")


# ============================================================
# Task 1.3: 场景异步加载 (带进度 + 超时)
# ============================================================
class ProgressReporter:
    """等价 C# Progress.Create<T>"""
    def __init__(self, on_progress: Callable[[float], None]):
        self.on_progress = on_progress

    def report(self, value: float):
        self.on_progress(value)


async def load_scene_async(
    scene_name: str,
    timeout: float = 30.0,
    on_progress: Optional[Callable[[float], None]] = None
) -> bool:
    """
    对应 SceneLoader.LoadSceneAsync()
    演示: 进度汇报 + 超时 + 取消
    """
    print(f"[SceneLoader] 开始加载场景: {scene_name}")

    try:
        # 模拟加载过程（Unity 中这是 LoadSceneAsync.progress）
        async def loading_process():
            for i in range(10):
                await asyncio.sleep(0.3)  # 每步0.3秒，总计3秒
                progress = (i + 1) / 10
                if on_progress:
                    on_progress(progress)
                print(f"  [SceneLoader] 进度: {progress*100:.0f}%")

        await asyncio.wait_for(loading_process(), timeout=timeout)
        # 注意: wait_for 包住整个 loading_process，所以总时长受 timeout 约束

        print(f"\n[SceneLoader] 场景 '{scene_name}' 加载成功 ✅")
        return True

    except asyncio.TimeoutError:
        print(f"[SceneLoader] 场景加载超时 ({timeout}s) ❌")
        return False
    except asyncio.CancelledError:
        print(f"[SceneLoader] 场景加载被取消 ❌")
        return False


async def demo_scene_loader():
    """对应 SceneLoader.cs 的 Start() 使用示例"""
    print("=" * 50)
    print("[Task 1.3] 场景异步加载")
    print("=" * 50)

    success = await load_scene_async(
        scene_name="BattleScene",
        timeout=5.0,
        on_progress=lambda p: None  # 实际项目中更新 UI
    )
    print(f"结果: {'进入战斗场景' if success else '加载失败'}\n")

    # 演示超时场景
    print("--- 超时场景 ---")
    success = await load_scene_async("SlowScene", timeout=1.0)
    print(f"结果: {'成功' if success else '失败（预期超时）'}\n")

    print("[Task 1.3] ✅ 完成\n")


# ============================================================
# Task 1.4: 取消令牌
# ============================================================
async def demo_cancellation():
    """对应 CancellationDemo.cs — 三种取消模式"""
    print("=" * 50)
    print("[Task 1.4] 取消令牌")
    print("=" * 50)

    # --- 模式 1: 自动取消 (等价 GetCancellationTokenOnDestroy) ---
    print("--- 模式1: 自动取消 ---")
    task = asyncio.create_task(heartbeat_loop())
    await asyncio.sleep(2.5)
    task.cancel()  # ← 等价 GameObject.Destroy → 自动取消
    try:
        await task
    except asyncio.CancelledError:
        print("[Demo] 物体已销毁，循环结束 ✅")

    # --- 模式 2: 优雅取消 (等价 SuppressCancellationThrow) ---
    print("\n--- 模式2: 优雅取消 ---")
    result = await graceful_operation(timeout=3.0, cancel_after=1.0)
    print(f"结果: {result}")

    # --- 模式 3: 链接取消 (等价 CancellationTokenSource.CreateLinkedTokenSource) ---
    print("\n--- 模式3: 链接取消 ---")
    await linked_cancellation_demo()

    print("[Task 1.4] ✅ 完成\n")


async def heartbeat_loop():
    """等价于 Unity 中绑定 destroyCancellationToken 的循环"""
    count = 0
    while True:
        await asyncio.sleep(1)
        count += 1
        print(f"  [心跳] 第{count}次...")
        # Unity中: await UniTask.Delay(1000, cancellationToken: token)


async def graceful_operation(timeout: float, cancel_after: float):
    """
    等价: await UniTask.Delay(3000, token).SuppressCancellationThrow()
    返回 (isCanceled, result)
    """
    try:
        # 创建一个会在 cancel_after 秒后取消的任务
        async def work():
            await asyncio.sleep(timeout)
            return "正常完成"
        async def canceller():
            await asyncio.sleep(cancel_after)
            raise asyncio.CancelledError("模拟取消")

        # 竞速: 工作 vs 取消信号
        done, pending = await asyncio.wait(
            [asyncio.create_task(work()), asyncio.create_task(canceller())],
            return_when=asyncio.FIRST_COMPLETED
        )

        # 取消未完成的
        for t in pending:
            t.cancel()

        for t in done:
            if t.exception():
                raise t.exception()
            return ("成功", t.result())

    except asyncio.CancelledError:
        return ("已取消", None)


async def linked_cancellation_demo():
    """等价 CancellationTokenSource.CreateLinkedTokenSource"""
    # 模拟两个取消源
    async def download_with_cancel(user_cancelled: asyncio.Event, timeout: float):
        try:
            # 创建超时任务
            async def download():
                for i in range(10):
                    await asyncio.sleep(0.3)
                    print(f"  下载中... {(i+1)*10}%")
                    if user_cancelled.is_set():
                        raise asyncio.CancelledError("用户取消")
                return "下载完成"

            await asyncio.wait_for(download(), timeout=timeout)

        except asyncio.TimeoutError:
            print("  下载超时！")
        except asyncio.CancelledError as e:
            print(f"  下载取消: {e}")

    # 用户在2秒后点击取消
    user_cancel = asyncio.Event()
    asyncio.create_task(trigger_cancel(user_cancel, 2.0))
    await download_with_cancel(user_cancel, timeout=5.0)


async def trigger_cancel(event: asyncio.Event, delay: float):
    await asyncio.sleep(delay)
    event.set()
    print("  [用户点击了取消按钮]")


# ============================================================
# Task 1.8: WhenAll 并行加载
# ============================================================
async def demo_when_all():
    """对应 Task 1.8: WhenAll 并行加载"""
    print("=" * 50)
    print("[Task 1.8] WhenAll 并行加载")
    print("=" * 50)

    t0 = time.time()
    # C#: await UniTask.WhenAll(LoadA(), LoadB(), LoadC())
    results = await asyncio.gather(
        load_asset("Icon.png", delay=1.0),
        load_asset("BGM.mp3", delay=1.5),
        load_asset("Model.prefab", delay=0.8),
    )
    elapsed = time.time() - t0
    print(f"三个资源并行加载完成: {results}")
    print(f"耗时: {elapsed:.1f}s (串行需要 1.0+1.5+0.8=3.3s)")
    print("[Task 1.8] ✅ 完成\n")


async def load_asset(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"[{name}]"


# ============================================================
# Task 1.9: WhenAny 竞速加载
# ============================================================
async def demo_when_any():
    """对应 Task 1.9: WhenAny 竞速加载 — 缓存 vs 网络，谁快用谁"""
    print("=" * 50)
    print("[Task 1.9] WhenAny 竞速加载")
    print("=" * 50)

    t0 = time.time()
    # C#: await UniTask.WhenAny(LoadFromCache(), LoadFromNetwork())
    done, pending = await asyncio.wait(
        [
            asyncio.create_task(load_from_cache("PlayerData")),
            asyncio.create_task(load_from_network("PlayerData")),
        ],
        return_when=asyncio.FIRST_COMPLETED,
    )

    # 拿到最先完成的
    for task in done:
        result = task.result()
        source, data = result
        print(f"竞速结果: 来自 [{source}], 数据={data}")

    # 取消慢的那个
    for task in pending:
        task.cancel()

    elapsed = time.time() - t0
    print(f"耗时: {elapsed:.1f}s")
    print("[Task 1.9] ✅ 完成\n")


async def load_from_cache(key: str):
    await asyncio.sleep(0.2)  # 缓存快
    return ("CACHE", f"{key}_cached_data")


async def load_from_network(key: str):
    await asyncio.sleep(2.0)  # 网络慢
    return ("NETWORK", f"{key}_network_data")


# ============================================================
# Task 1.10: AsyncReactiveProperty 响应式数据
# ============================================================
class AsyncReactiveProperty:
    """
    等价 C# AsyncReactiveProperty<T>
    值变化 → 自动通知订阅者
    """
    def __init__(self, initial_value):
        self._value = initial_value
        self._callbacks = []

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        old = self._value
        self._value = new_value
        if old != new_value:
            for cb in self._callbacks:
                cb(new_value)

    def subscribe(self, callback):
        self._callbacks.append(callback)

    def __repr__(self):
        return f"AsyncReactiveProperty({self._value})"


async def demo_reactive_property():
    """对应 Task 1.10: 血量变化 → UI 自动更新"""
    print("=" * 50)
    print("[Task 1.10] AsyncReactiveProperty 响应式数据")
    print("=" * 50)

    hp = AsyncReactiveProperty(100)

    # 订阅：血量变化 → 自动更新UI
    hp.subscribe(lambda v: print(f"  [UI] 血量变为: {v}"))

    # 模拟战斗
    print(f"初始血量: {hp.value}")
    await asyncio.sleep(0.5)
    hp.value = 80   # 受到伤害 → UI 自动刷新

    await asyncio.sleep(0.5)
    hp.value = 50   # 再次受伤

    await asyncio.sleep(0.5)
    hp.value = 0    # 死亡

    print("[Task 1.10] ✅ 完成\n")


# ============================================================
# Task 1.5: 带超时+重试的异步加载
# ============================================================
async def load_with_retry(address: str, max_retries: int = 3, timeout: float = 2.0):
    """
    等价: UniTask + Addressables 封装，带超时和重试
    对应 Task 1.5
    """
    print(f"[ContentLoader] 加载 '{address}' (最多重试{max_retries}次)...")

    for attempt in range(1, max_retries + 1):
        try:
            result = await asyncio.wait_for(
                simulated_asset_load(address, attempt),
                timeout=timeout
            )
            print(f"[ContentLoader] '{address}' 加载成功 (第{attempt}次尝试)")
            return result
        except asyncio.TimeoutError:
            print(f"[ContentLoader] 超时 (第{attempt}次), {'重试中...' if attempt < max_retries else '放弃'}")
        except Exception as e:
            print(f"[ContentLoader] 失败 (第{attempt}次): {e}")

    raise TimeoutError(f"加载 '{address}' 失败，已重试{max_retries}次")


async def simulated_asset_load(address: str, attempt: int) -> str:
    """模拟资源加载：第1次失败，第2次成功"""
    if attempt == 1:
        await asyncio.sleep(3)  # 模拟超时
    await asyncio.sleep(0.3)
    return f"Asset({address})"


async def demo_retry():
    """对应 Task 1.5"""
    print("=" * 50)
    print("[Task 1.5] 带超时+重试的异步加载")
    print("=" * 50)

    try:
        result = await load_with_retry("PlayerPrefab", max_retries=3, timeout=1.5)
        print(f"最终结果: {result}")
    except TimeoutError as e:
        print(f"最终失败: {e}")

    print("[Task 1.5] ✅ 完成\n")


# ============================================================
# 主函数: 依次运行所有 Demo
# ============================================================
async def main():
    print("\n" + "=" * 60)
    print("  UniTask 核心模式 Python 等效验证")
    print("  所有模式在 C# UniTask 中写法几乎一致")
    print("=" * 60 + "\n")

    await demo_basic_returns()       # Task 1.2
    await demo_scene_loader()        # Task 1.3
    await demo_cancellation()        # Task 1.4
    await demo_retry()               # Task 1.5
    await demo_when_all()            # Task 1.8
    await demo_when_any()            # Task 1.9
    await demo_reactive_property()   # Task 1.10

    print("=" * 60)
    print("  全部 Demo 运行完毕 ✅")
    print("  这些模式在 C# UniTask 中 API 不同，逻辑完全一样")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
