"""
P1/P2 补充概念验证 Demo
=========================
涵盖热更新、ML 基础、ECS/DOTS 思路
"""

import time
from abc import ABC, abstractmethod
from typing import List, Tuple, Callable
from dataclasses import dataclass


# ============================================================
# P2-2 ML-Agents 概念: 强化学习循环
# ============================================================
@dataclass
class Observation:
    ball_x: float
    ball_vx: float
    platform_angle: float

class BalanceEnv:
    """
    等价 3D Balance Ball 环境
    Agent 看球的位置和速度，决定平台倾斜角
    球不掉 = 得 Reward
    """
    def __init__(self):
        self.ball_x = 0.0
        self.ball_vx = 0.1
        self.platform_angle = 0.0
        self.steps = 0

    def reset(self) -> Observation:
        self.ball_x = 0.0
        self.ball_vx = 0.1
        self.platform_angle = 0.0
        self.steps = 0
        return self._observe()

    def step(self, action: float) -> Tuple[Observation, float, bool]:
        """
        action: 平台倾斜角变化 (-1 ~ 1)
        返回: (新观察, 奖励, 是否结束)
        """
        self.platform_angle += action * 0.1
        # 物理: 球受重力影响，倾向滚向平台倾斜方向
        self.ball_vx += self.platform_angle * 0.05
        self.ball_x += self.ball_vx
        self.steps += 1

        # Reward: 球靠近中心 = 正奖励
        reward = 1.0 - abs(self.ball_x)

        # 球掉出平台 = 结束
        done = abs(self.ball_x) > 2.0 or self.steps > 100

        return self._observe(), reward, done

    def _observe(self) -> Observation:
        return Observation(self.ball_x, self.ball_vx, self.platform_angle)


class SimpleBrain:
    """最简单的"AI"：球往右滚 → 平台往左倾斜（手工规则）"""
    def decide(self, obs: Observation) -> float:
        return -obs.ball_x * 0.5  # 反方向倾斜


def demo_ml_concept():
    """Task 8.2: ML-Agents 概念"""
    print("=" * 50)
    print("[ML-Agents] 强化学习循环演示")
    print("=" * 50)

    env = BalanceEnv()
    brain = SimpleBrain()

    obs = env.reset()
    total_reward = 0

    for step in range(100):
        action = brain.decide(obs)
        obs, reward, done = env.step(action)
        total_reward += reward
        if step % 20 == 0:
            print(f"  Step {step:3d}: ball_x={obs.ball_x:+.2f} "
                  f"angle={obs.platform_angle:+.2f} reward={reward:+.2f}")
        if done:
            break

    print(f"  总Reward: {total_reward:.2f}")
    print(f"  这个 brain 是手工规则。真正的 ML-Agents 用神经网络替代 brain.decide()")
    print("[ML-Agents] ✅ 概念验证完成\n")


# ============================================================
# P2-3 ECS/DOTS 概念: 数据导向 vs 面向对象
# ============================================================
def demo_ecs_concept():
    """Task 9.1: ECS 概念演示"""
    print("=" * 50)
    print("[ECS/DOTS] 数据导向设计概念")
    print("=" * 50)

    import random

    # === OOP 方式: 每个对象独立 Update ===
    class MonoProjectile:
        def __init__(self, x, y, vx, vy):
            self.x, self.y = x, y
            self.vx, self.vy = vx, vy
            self.life = 3.0

        def update(self, dt):
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.life -= dt

    N = 10000

    # OOP: 逐个调用虚方法
    t0 = time.perf_counter()
    monos = [MonoProjectile(random.random()*10, random.random()*10,
                            random.random()*3, random.random()*3)
             for _ in range(N)]
    for _ in range(100):  # 100帧
        for m in monos:
            m.update(0.016)
    oop_time = time.perf_counter() - t0

    # === ECS 方式: 数据连续存储，批量处理 ===
    # Component = 数组（Cache-friendly）
    xs = [random.random()*10 for _ in range(N)]
    ys = [random.random()*10 for _ in range(N)]
    vxs = [random.random()*3 for _ in range(N)]
    vys = [random.random()*3 for _ in range(N)]
    lifes = [3.0 for _ in range(N)]

    t0 = time.perf_counter()
    for _ in range(100):
        dt = 0.016
        # System: 同一个操作应用到所有数据（SIMD 友好）
        for i in range(N):
            xs[i] += vxs[i] * dt
            ys[i] += vys[i] * dt
            lifes[i] -= dt
    ecs_time = time.perf_counter() - t0

    print(f"  {N} 对象 × 100 帧:")
    print(f"    OOP (逐个对象):     {oop_time:.3f}s")
    print(f"    ECS (数组批量):     {ecs_time:.3f}s")
    print(f"    ECS 加速比:         {oop_time/ecs_time:.1f}x")
    print(f"  原因: ECS 数据连续排列 = CPU 缓存命中率高 + 无虚函数调用开销")
    print(f"  Unity 中 Burst 编译器还会额外再加速 10-50x")
    print("[ECS/DOTS] ✅ 概念验证完成\n")


# ============================================================
# P2-1 热更新概念: Lua 脚本动态加载
# ============================================================
def demo_hotfix_concept():
    """Task 7.1~7.2: 热更新概念"""
    print("=" * 50)
    print("[热更新] 动态脚本概念")
    print("=" * 50)

    # 模拟原始的 C# 函数（已打包进 APK）
    def original_damage_formula(base_atk: int, defense: int) -> int:
        return max(1, base_atk - defense)

    # 模拟热更新的 Lua（从服务器下载的新脚本）
    HOTFIX_SCRIPT = """
# 新公式: 增加暴击率
def damage_formula(base_atk: int, defense: int) -> int:
    import random
    base = max(1, base_atk - defense)
    if random.random() < 0.2:  # 20% 暴击
        print("  暴击!")
        return base * 2
    return base
"""

    print("  原始公式 (base=100, def=30):", original_damage_formula(100, 30))

    # 模拟 xLua: DoString 执行热更脚本
    local_vars = {}
    exec(HOTFIX_SCRIPT, {}, local_vars)
    hotfix_fn = local_vars["damage_formula"]

    results = [hotfix_fn(100, 30) for _ in range(5)]
    print(f"  热更公式 5次攻击: {results}")
    print(f"  (20%暴击率已生效，不用重装APP)")
    print("[热更新] ✅ 概念验证完成\n")


# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  P1/P2 补充概念验证")
    print("=" * 60 + "\n")

    demo_ml_concept()
    demo_ecs_concept()
    demo_hotfix_concept()

    print("=" * 60)
    print("  全部 P1/P2 概念验证完毕 ✅")
    print("=" * 60)
