"""
VContainer 等效 Python Demo
=============================
DI 容器的核心概念用 Python 实现：
- Register / Resolve
- Singleton / Transient / Scoped
- 构造注入
- 接口解耦

对应 C# VContainer 的核心 API
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Type, TypeVar, Callable
from enum import Enum


T = TypeVar('T')


# ============================================================
# 第一步：定义接口（等价 C# interface）
# ============================================================
class IInputService(ABC):
    @abstractmethod
    def get_move_direction(self) -> tuple:
        ...

class IWeapon(ABC):
    @abstractmethod
    def attack(self) -> int:
        ...

class ILogger(ABC):
    @abstractmethod
    def log(self, msg: str):
        ...


# ============================================================
# 第二步：实现类
# ============================================================
class KeyboardInput(IInputService):
    def get_move_direction(self) -> tuple:
        return (1.0, 0.0)  # 模拟键盘输入

class GamepadInput(IInputService):
    def get_move_direction(self) -> tuple:
        return (0.5, 0.5)  # 模拟手柄输入

class Sword(IWeapon):
    def attack(self) -> int:
        return 15

class Bow(IWeapon):
    def attack(self) -> int:
        return 10

class ConsoleLogger(ILogger):
    def log(self, msg: str):
        print(f"  [LOG] {msg}")


# ============================================================
# Task 2.2: 手动 DI（体会没有容器时的痛苦 vs 好处）
# ============================================================
class Player:
    """
    等价: C# PlayerController
    不 new 自己的依赖，而是通过构造函数接收
    """
    def __init__(self, name: str, input_svc: IInputService, weapon: IWeapon, logger: ILogger):
        self.name = name
        self._input = input_svc
        self._weapon = weapon
        self._logger = logger

    def update(self):
        direction = self._input.get_move_direction()
        damage = self._weapon.attack()
        self._logger.log(f"{self.name} 移动 {direction} 攻击 {damage}")


class GameRoot:
    """
    等价: 手动 Composition Root
    在程序入口处组装所有依赖
    """
    def __init__(self):
        # 组装依赖树
        logger = ConsoleLogger()
        input_svc = KeyboardInput()
        weapon = Sword()

        self.player = Player("Hero", input_svc, weapon, logger)

    def run(self):
        self.player.update()


# ============================================================
# Task 2.3~2.6: 简易 DI 容器（等价 VContainer 核心）
# ============================================================
class Lifetime(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"


class Container:
    """
    简化版 DI 容器 — 等价 VContainer 的 IContainerBuilder
    """
    def __init__(self, parent: "Container | None" = None):
        self._registry: Dict[Type, Dict[str, Any]] = {}
        self._singletons: Dict[Type, Any] = {}
        self._parent = parent

    def register(self, interface: Type, implementation: Type, lifetime: Lifetime = Lifetime.TRANSIENT):
        self._registry[interface] = {
            "impl": implementation,
            "lifetime": lifetime,
        }

    def register_instance(self, interface: Type, instance: Any):
        self._registry[interface] = {
            "impl": type(instance),
            "lifetime": Lifetime.SINGLETON,
        }
        self._singletons[interface] = instance

    def resolve(self, interface: Type) -> Any:
        if interface in self._singletons:
            return self._singletons[interface]

        if interface not in self._registry:
            if self._parent:
                return self._parent.resolve(interface)
            raise KeyError(f"未注册: {interface}")

        entry = self._registry[interface]
        instance = self._create_instance(entry["impl"])

        if entry["lifetime"] == Lifetime.SINGLETON:
            self._singletons[interface] = instance

        return instance

    def _create_instance(self, impl_type: Type) -> Any:
        """自动构造注入：看 __init__ 参数，逐个 resolve"""
        import inspect
        try:
            sig = inspect.signature(impl_type.__init__)
        except (ValueError, TypeError):
            return impl_type()

        kwargs = {}
        for name, param in sig.parameters.items():
            if name == "self":
                continue
            if param.annotation != inspect.Parameter.empty:
                kwargs[name] = self.resolve(param.annotation)

        return impl_type(**kwargs)


def demo_manual_di():
    """Task 2.2: 手动 DI — 没有容器时的装配"""
    print("=" * 50)
    print("[Task 2.2] 手动 DI 体验")
    print("=" * 50)

    game = GameRoot()
    game.run()

    # 想换成手柄+弓箭？
    print("\n--- 切换武器和输入 ---")
    # 只需要在这里改装配，Player 代码一行不动
    logger = ConsoleLogger()
    player = Player("Archer", GamepadInput(), Bow(), logger)
    player.update()

    print("[Task 2.2] ✅ 完成\n")


def demo_container_basic():
    """Task 2.3~2.4: 用容器注册/解析"""
    print("=" * 50)
    print("[Task 2.3] VContainer 核心: Register + Resolve")
    print("=" * 50)

    container = Container()

    # 注册（等价 builder.Register<X, Y>(Lifetime.Singleton)）
    container.register(ILogger, ConsoleLogger, Lifetime.SINGLETON)
    container.register(IInputService, KeyboardInput, Lifetime.SINGLETON)
    container.register(IWeapon, Sword, Lifetime.SINGLETON)

    # 解析（等价 Container.Resolve<Player>()）
    logger = container.resolve(ILogger)
    logger.log("容器已配置")

    input_svc = container.resolve(IInputService)
    print(f"  Input: {input_svc.get_move_direction()}")

    weapon = container.resolve(IWeapon)
    print(f"  Weapon 伤害: {weapon.attack()}")

    # 验证 Singleton：两次 Resolve 返回同一个实例
    w1 = container.resolve(IWeapon)
    w2 = container.resolve(IWeapon)
    print(f"  Singleton: w1 is w2 = {w1 is w2}")  # True

    print("[Task 2.3] ✅ 完成\n")


def demo_weapon_switch():
    """Task 2.6: 武器切换（重新注册即可，Player 不改）"""
    print("=" * 50)
    print("[Task 2.6] 武器系统练手: 不碰 Player 代码，切换武器")
    print("=" * 50)

    container = Container()
    container.register(ILogger, ConsoleLogger, Lifetime.SINGLETON)
    container.register(IInputService, KeyboardInput, Lifetime.SINGLETON)

    # --- 场景 1: 剑 ---
    print("--- 装备 Sword ---")
    container.register(IWeapon, Sword, Lifetime.SINGLETON)
    player = Player("Knight", container.resolve(IInputService),
                     container.resolve(IWeapon), container.resolve(ILogger))
    player.update()

    # --- 场景 2: 弓（新建容器，Player 代码完全不变） ---
    print("--- 装备 Bow ---")
    container2 = Container()
    container2.register(ILogger, ConsoleLogger, Lifetime.SINGLETON)
    container2.register(IInputService, GamepadInput, Lifetime.SINGLETON)
    container2.register(IWeapon, Bow, Lifetime.SINGLETON)

    player2 = Player("Archer", container2.resolve(IInputService),
                      container2.resolve(IWeapon), container2.resolve(ILogger))
    player2.update()

    print("[Task 2.6] ✅ 完成\n")


def demo_scoped_lifetime():
    """Task 2.5: Scoped 生命周期"""
    print("=" * 50)
    print("[Task 2.5] Scoped 生命周期模拟")
    print("=" * 50)

    # ApplicationScope: 全局单例
    app = Container()
    app.register(ILogger, ConsoleLogger, Lifetime.SINGLETON)

    # BattleScope: 战斗场景内的作用域（有 parent 引用）
    battle = Container(parent=app)
    battle.register(IInputService, KeyboardInput, Lifetime.SINGLETON)
    battle.register(IWeapon, Sword, Lifetime.SINGLETON)

    # BattleScope 可以 resolve 父容器中的类型
    logger = battle.resolve(ILogger)
    logger.log("战斗开始！(Logger 来自父容器)")

    # 离开战斗: battle 被丢弃，BattleScope 内的对象被 GC
    # Singleton（来自 app）保留
    print("离开战斗... BattleScope 被丢弃")
    del battle

    # 验证父容器不受影响
    logger2 = app.resolve(ILogger)
    logger2.log("标题画面 (Logger 仍存活)")

    print("[Task 2.5] ✅ 完成\n")


def demo_message_pipe():
    """Task 2.9: MessagePipe 发布/订阅"""
    print("=" * 50)
    print("[Task 2.9] MessagePipe: 发布/订阅模式")
    print("=" * 50)

    class EventBus:
        def __init__(self):
            self._subscribers: Dict[Type, list] = {}

        def subscribe(self, event_type: Type, callback: Callable):
            self._subscribers.setdefault(event_type, []).append(callback)

        def publish(self, event: Any):
            for cb in self._subscribers.get(type(event), []):
                cb(event)

    class EnemyKilledEvent:
        def __init__(self, enemy_name: str, score: int):
            self.enemy_name = enemy_name
            self.score = score

    bus = EventBus()

    # 订阅方1: 分数 UI
    score = [0]
    bus.subscribe(EnemyKilledEvent, lambda e: (
        score.__setitem__(0, score[0] + e.score),
        print(f"  [ScoreUI] 当前分数: {score[0]}")
    ))

    # 订阅方2: 特效系统
    bus.subscribe(EnemyKilledEvent, lambda e:
        print(f"  [FX] 播放击杀特效: {e.enemy_name}")
    )

    # 发布方: 敌人系统 — 完全不认识订阅方
    bus.publish(EnemyKilledEvent("Goblin", 100))
    bus.publish(EnemyKilledEvent("Dragon", 500))

    print("[Task 2.9] ✅ 完成\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  VContainer 核心概念 Python 等效验证")
    print("=" * 60 + "\n")

    demo_manual_di()           # Task 2.2
    demo_container_basic()     # Task 2.3~2.4
    demo_weapon_switch()       # Task 2.6
    demo_scoped_lifetime()     # Task 2.5
    demo_message_pipe()        # Task 2.9

    print("=" * 60)
    print("  VContainer 全部概念验证完毕 ✅")
    print("=" * 60)
