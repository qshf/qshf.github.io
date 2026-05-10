---
title: "Experiments"
date: 2026-05-10
draft: false
weight: 3
---

# MemGPT 论文总结（Experiments / 实验章节）

> 来源：arXiv:2310.08560v2

## 一、实验总览

MemGPT 在两个**长上下文**领域上做评估：

| 领域 | 核心挑战 | 本文任务 |
| --- | --- | --- |
| **对话 agent**（§5.1） | 跨多轮/多会话保持一致性与吸引力 | Deep Memory Retrieval (DMR)；Conversation Opener |
| **文档分析**（§5.2） | 单/多文档远超上下文窗口 | Multi-doc QA（基于 NaturalQuestions-Open）；Nested KV Retrieval（新任务，多跳） |

作者公开发布三份资源：扩展版 MSC 数据集、Nested KV 数据集、以及 20M 维基文档的预计算 embedding。

### 实现细节（模型版本）

| 别名 | 对应 endpoint | 上下文窗口 |
| --- | --- | --- |
| GPT-4 Turbo | `gpt-4-1106-preview` | 128k |
| GPT-4 | `gpt-4-0613` | 8k |
| GPT-3.5 Turbo | `gpt-3.5-turbo-1106` | 16k |

## 二、对话 Agent 实验

### 2.1 评测目标：一致性 + 参与度

1. **Consistency（一致性）**：新事实/偏好/事件要与历史陈述一致，不能自相矛盾。
2. **Engagement（参与度）**：主动调用长期知识，让对话更自然、更个性化。

### 2.2 数据集：Multi-Session Chat (MSC)

Xu et al. 2021 提出的多会话闲聊数据，每段由**同一组人物设定**下的 5 个 session 组成。作者额外构造了第 6 session 用于一致性实验。

### 2.3 任务 A：Deep Memory Retrieval (DMR) — 一致性

**构造方式**：用另一个 LLM 基于 session 1–5 的历史，生成一条只能**回看过去对话**才答得出的问题。

**评测指标**：ROUGE-L Recall + GPT-4 作 LLM judge。

**结果**（Table 1）：

| Model | Accuracy ↑ | ROUGE-L (R) ↑ |
| --- | --- | --- |
| GPT-3.5 Turbo | 38.7% | 0.394 |
| **+ MemGPT** | **66.9%** | **0.629** |
| GPT-4 | 32.1% | 0.296 |
| **+ MemGPT** | **92.5%** | **0.814** |
| GPT-4 Turbo | 35.3% | 0.359 |
| **+ MemGPT** | **93.4%** | **0.827** |

**结论**：MemGPT+GPT-4 Turbo 的 accuracy 比裸 GPT-4 Turbo 高了约 **58 个百分点**。递归摘要会有信息损失，而 MemGPT 通过分页检索**完整原文**，该记住的细节真的还在。

### 2.4 任务 B：Conversation Opener — 参与度

**评测指标**（CSIM 相似度）：SIM-1/SIM-3（vs gold persona）、SIM-H（vs 人类手写 opener）。

**结果**（Table 2）：

| Method | SIM-1 ↑ | SIM-3 | SIM-H |
| --- | --- | --- | --- |
| Human | 0.800 | 0.800 | 1.000 |
| MemGPT + GPT-3.5 Turbo | 0.830 | 0.812 | **0.817** |
| MemGPT + GPT-4 | **0.868** | **0.843** | 0.773 |
| MemGPT + GPT-4 Turbo | 0.857 | 0.828 | 0.767 |

**结论**：MemGPT 在 SIM-1/SIM-3 上**超过了人类 baseline**。把信息存进 **working context** 是写出高质量开场白的关键。

## 三、文档分析实验

### 3.1 为什么需要 MemGPT：上下文窗口对比

| 模型 | 开源? | Tokens |
| --- | --- | --- |
| Llama 2 | √ | 4k |
| Mistral 7B | √ | 8k |
| GPT-4 (release) | × | 8k |
| GPT-3.5 Turbo | × | 16k |
| GPT-4 Turbo | × | 128k |

引用 **Lost in the Middle**（Liu et al. 2023）：长上下文注意力分布不均，**中间位置的信息被严重遗忘**。

### 3.2 任务 A：Multi-Document QA

**检索底座**：`text-embedding-ada-002` + cosine similarity + **PostgreSQL + pgvector + HNSW**，Wikipedia 2018 快照预计算 embedding 入库。

![MemGPT 解决文档 QA 任务的示例](/images/memgpt/memgpt_docqa_example_2.png)

*图：MemGPT 通过函数调用查询 archival storage，把分页结果拉进 main context。*

![Document QA 准确率](/images/memgpt/docqa.png)

*图：MemGPT 的表现几乎**不随 K（上下文中文档数）变化**；固定上下文基线用 truncation 硬扩上下文后准确率随压缩程度下降。*

关键观察：
1. **固定上下文基线的上限被 retriever 卡死**：gold 文档没排进前 K 就永远看不到。
2. **MemGPT 可以多次分页翻**，不被单次排名限制。
3. 主要失效模式：MemGPT 会在翻完候选库之前自己停下。
4. GPT-3.5 上 MemGPT 显著变差，因为**函数调用能力太弱**。

### 3.3 任务 B：Nested Key-Value Retrieval（多跳检索）

**任务**：140 对 UUID（~8k tokens），value 本身可能是另一个 key，要求**多跳 lookup**，嵌套层数 0–4。

![MemGPT 解决 Nested KV 的示例](/images/memgpt/memgpt_nested_kv_example.png)

*图：MemGPT 逐跳查 `831..ea5 → 5b8..4c3 → f37..617`。*

![Nested KV 准确率 vs 嵌套层数](/images/memgpt/nested_kv.png)

*图：MemGPT 是**唯一**能稳定跨过 2 层嵌套的方法；MemGPT+GPT-4 反而比 MemGPT+GPT-4 Turbo 更好。*

| 模型 | 单跳（0 层） | 2 层 | 3+ 层 |
| --- | --- | --- | --- |
| GPT-3.5 / GPT-3.5+MemGPT | 能做 | 0% | 0% |
| GPT-4 / GPT-4 Turbo | 能做 | 掉得很厉害 | 0% |
| **MemGPT + GPT-4** | 能做 | **不降** | **几乎不降** |

## 四、整体结论

| 维度 | 主要证据 | 规律 |
| --- | --- | --- |
| 一致性 | DMR 大幅领先基线（+58pp on GPT-4 Turbo） | 完整原文 + 分页检索 > 递归摘要 |
| 参与度 | Opener 的 SIM-1/SIM-3 超人类 | 把 persona 固化进 working context 最有效 |
| 单文档扩容 | Doc QA 不随 K 衰减 | archival storage 让检索可**反复翻** |
| 多跳推理 | Nested KV 跨 2–4 层稳定 | 函数链 + main context 读写让多跳 lookup 天然落地 |
| 主要失效 | Doc QA / Nested KV 的弱底座 | **函数调用能力**决定 MemGPT 的上限 |

## 五、一句话总结

> **MemGPT 的收益来自"可翻页的外部存储 + 可读写的工作上下文 + 函数调用驱动的多跳"三者协同**：四类任务上都显著超越固定上下文基线，但**底座的函数调用能力是天花板**——GPT-4 上的 MemGPT 是最稳定的配置。
