---
title: "04 · 二刷问题清单（主动回忆）"
description: "《强化学习的数学原理》二轮总结"
weight: 50
math: true
mermaid: true
ShowToc: true
TocOpen: true
categories: ["书籍笔记"]
tags: ["强化学习", "数学原理"]
---

> **复习的正确姿势不是重读笔记，而是先盖住答案问自己。** 每章 5~8 题，能不看笔记答出 → 跳过；卡住 → 点链接回原章节。
> 题目多取自各章 Q&A 与「我应该能回答」节。入口见 [00 全书地图](/books/reinforcement-learning-math/summary/00_book-map/)。

用法：给每题标记 ✅能答 / 🟡含糊 / 🔴不会，只重看 🟡🔴 对应章节。

---

## Ch1 基本概念 → [笔记](/books/reinforcement-learning-math/notes/01_chapter1-basic-concepts/)
1. 为什么强化学习问题可以建模成 MDP？MDP 由哪几个要素组成？
2. 为什么转移、奖励、策略都要用「条件概率」而不是表格来描述？
3. state 和 observation 有什么区别？马尔可夫性质说的是什么？
4. reward（奖励）和 return（回报）有什么区别？
5. 折扣因子 $\gamma$ 的作用是什么？$\gamma=0$ 和 $\gamma\to1$ 分别会怎样？
6. 为什么「知道地图」时就不需要强化学习了？

## Ch2 贝尔曼方程 → [笔记](/books/reinforcement-learning-math/notes/02_chapter2-bellman-equation/)
1. 回报的自举关系 $G_t=R_{t+1}+\gamma G_{t+1}$ 怎么来的？
2. 贝尔曼方程的矩阵形式是什么？为什么 $(I-\gamma P_\pi)$ 一定可逆？
3. $v_\pi$ 和 $q_\pi$ 怎么互相表示？（两条关系式）
4. 闭式解和迭代解各自什么时候用？
5. 为什么说全期望公式是推导贝尔曼方程的关键一步？（见 [02_证明索引](/books/reinforcement-learning-math/summary/02_proof-index/) 条目1）

## Ch3 最优策略与 BOE → [笔记](/books/reinforcement-learning-math/notes/03_chapter3-optimal-policies-and-the-bellman-optimality-equation/)
1. BOE 和普通贝尔曼方程的根本区别是什么？为什么 BOE 不能求逆？
2. 压缩映射定理保证了什么？为什么 BOE 右侧 $f(v)$ 是压缩映射？
3. 解出 $v^*$ 后，怎么得到 $\pi^*$？为什么贪心就够了？
4. 折扣率变小，策略会变「短视」还是「远视」？为什么？
5. 给所有奖励做仿射变换 $r\to ar+b$，最优策略会变吗？

## Ch4 值迭代 / 策略迭代 → [笔记](/books/reinforcement-learning-math/notes/04_chapter4-value-iteration-and-policy-iteration/)
1. 值迭代和策略迭代的核心区别是什么？为什么说它们是 GPI 的两个端点？
2. 截断策略迭代「截」的是哪一步？
3. 为什么策略改进一定不会变差？（Lemma 4.1 的直觉）
4. 迭代中的 $v_k$ 为什么不是真正的状态值？
5. model-based 和 model-free 的分界在哪？本章属于哪类？

## Ch5 蒙特卡洛 → [笔记](/books/reinforcement-learning-math/notes/05_chapter5-monte-carlo-methods/)
1. MC 怎么把策略迭代里「需要模型的那一步」替换掉？
2. 为什么 MC 必须等 episode 结束？
3. exploring starts 是什么？为什么需要它？怎么用 ε-greedy 替代？
4. initial-visit / first-visit / every-visit 有什么区别？
5. ε 越大，探索越强但代价是什么？最优 ε-greedy 一定等于 greedy 最优吗？
6. MC Basic、MC Exploring Starts、MC ε-Greedy 三者什么关系？

## Ch6 随机近似 ★ → [笔记](/books/reinforcement-learning-math/notes/06_chapter6-stochastic-approximation/)
1. 增量均值公式 $w_{k+1}=w_k+\frac1k(x_k-w_k)$ 怎么推出来？它和 RL 更新式像在哪？
2. Robbins-Monro 算法解决什么问题？为什么要求 $\sum\alpha=\infty$ 且 $\sum\alpha^2\lt \infty$？
3. Dvoretzky 定理的「误差=被压缩的旧误差+小噪声」模板长什么样？
4. SGD 和 BGD、mini-batch 的区别？为什么 SGD「前期快、后期抖」？
5. 为什么说这一章是后面几章收敛性的地基？

## Ch7 时序差分 TD → [笔记](/books/reinforcement-learning-math/notes/07_chapter7-temporal-difference-methods/)
1. TD 更新式怎么从贝尔曼方程 + RM 推出来？TD error 是什么？
2. Sarsa 名字怎么来的？它在数学上求解什么方程？
3. n-step Sarsa 在 $n=1$ 和 $n=\infty$ 时分别退化成什么？
4. Sarsa、Expected Sarsa、Q-learning 的 target 各自怎么处理「下一动作」？
5. 为什么 Sarsa 是 on-policy、Q-learning 是 off-policy？
6. on-policy/off-policy 和 online/offline 有什么区别？
7. 为什么 Q-learning 目标策略可以纯 greedy，而 Sarsa 要 ε-greedy？

## Ch8 值函数近似 → [笔记](/books/reinforcement-learning-math/notes/08_chapter8-value-function-approximation/)
1. 从表格到函数近似，「读取价值」和「更新价值」各发生了什么变化？
2. 为什么表格法是函数近似的特例？
3. 平稳分布（stationary distribution）是什么？为什么 TD-Linear 的收敛分析需要它？
4. TD-Linear 实际最小化的是什么误差？（projected Bellman error）
5. DQN 为什么需要 target network？为什么需要 experience replay？
6. 训练 loss 为 0 是否意味着价值估计正确？

## Ch9 策略梯度 → [笔记](/books/reinforcement-learning-math/notes/09_chapter9-policy-gradient-methods/)
1. 策略梯度方法和值方法的根本区别？它适合什么场景？
2. policy gradient theorem 的主公式是什么？为什么会冒出 $\ln\pi$？
3. 定义最优策略的两个指标（$\bar v_\pi$、$\bar r_\pi$）各是什么？关系如何？
4. $d_0$、$d_\pi$、$\rho_\pi$ 这几个状态分布有什么区别？（见 [03 符号表](/books/reinforcement-learning-math/summary/03_pitfalls-symbols/)）
5. 为什么 $\nabla_\theta v_\pi(s)$ 会牵扯到未来所有可达状态？
6. REINFORCE 的更新为什么会「奖励好动作」？

## Ch10 Actor-Critic → [笔记](/books/reinforcement-learning-math/notes/10_chapter10-actor-critic-methods/)
1. actor 和 critic 分别做什么？actor-critic 和 policy gradient 是什么关系？
2. REINFORCE 和 QAC 的分叉点在哪？
3. 为什么可以给 actor 减一个 baseline？它改变梯度均值吗？advantage 是什么？
4. off-policy actor-critic 为什么需要重要性采样？权重是什么？
5. 确定性策略梯度为什么**不能**直接把随机公式里的 $A$ 换成 $\mu(S)$？
6. 为什么确定性 AC 天然是 off-policy，却不需要重要性采样？
7. QAC / A2C / off-policy AC / deterministic AC 一句话各自的特点？（见 [01 表10](/books/reinforcement-learning-math/summary/01_concept-comparison/)）

---

## 跨章「大问题」（真正消化的标志）
答得出这几个，说明你不是「读过」而是「消化」了这本书：
1. 整本书在解的那**一个**问题是什么？四个放松假设的维度各是什么？（见 [00](/books/reinforcement-learning-math/summary/00_book-map/)）
2. 为什么顺序是 DP → MC → TD？每一步补足了前一个的什么缺陷、又带来什么新问题？
3. 为什么 Q-learning 学的是 $q^*$，而 Sarsa/MC 学的是 $q_\pi$？这背后是 BE 还是 BOE？
4. 从 ch8 到 ch10 三步（近似价值 → 直接优化策略 → 两者合体）怎么串起来？
5. 这本书学完，你能用它的语言解释 PPO/SAC/DDPG 大致属于哪条线吗？
