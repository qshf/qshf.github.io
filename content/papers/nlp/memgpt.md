---
title: "MemGPT: Towards LLMs as Operating Systems"
date: 2026-05-10
tags: ["Agent", "Memory", "LLM", "RAG"]
categories: ["论文笔记"]
math: false
draft: false
summary: "MemGPT 借鉴操作系统虚拟内存分页机制，用函数调用让 LLM 在有限上下文窗口与外部存储之间自主分页，实现近乎无限的上下文管理。"
---

> 来源：arXiv:2310.08560v2

## 核心问题

大语言模型（LLM）受限于**固定长度的上下文窗口**，在长对话、长文档分析等任务中表现受限：

- 主流开源 LLM 通常只能处理几十轮对话或一篇短文档，超过最大输入长度后便失效。
- 直接扩展 Transformer 上下文长度会因自注意力机制带来**计算与显存的平方级增长**。
- 即便训练出更长上下文的模型，研究也表明它们**难以有效利用额外上下文**（"lost in the middle" 现象）。

## 核心思想：虚拟上下文管理

论文借鉴**操作系统的虚拟内存分页机制**：OS 通过在物理内存与磁盘之间换页，给应用"无限内存"的错觉。

| 操作系统 | MemGPT |
| --- | --- |
| 物理内存（main memory） | LLM 上下文窗口（main context） |
| 磁盘 / 外部存储 | 外部存储（archival & recall storage） |
| 分页、缺页中断 | 函数调用驱动的数据换入换出 |
| 进程与系统调用 | LLM agent 与函数调用 |

![MemGPT 在上下文不足时写入持久记忆](/images/memgpt/memgpt_diagrams_wide_memory_creation.png)

*图 1：MemGPT 收到上下文空间不足的系统告警后，将数据写入持久化记忆。*

## 方法

### 分层记忆架构

| 记忆类型 | OS 类比 | 含义 |
| --- | --- | --- |
| **Main context** | 主存 / RAM | LLM 的 prompt tokens，可直接被 LLM 访问 |
| **External context** | 磁盘 / 外存 | 位于上下文窗口之外，必须显式搬入才能被 LLM 看到 |

**Main context 三段结构：**

1. **System instructions**：只读、静态，包含控制流说明和所有可用函数的 schema
2. **Working context**：定长、可读写，仅能通过函数调用修改，保存用户关键事实和 agent 人设
3. **FIFO queue**：滚动的消息历史，队首放已驱逐消息的**递归摘要**

### Archival Storage vs Recall Storage

| 维度 | Archival Storage（归档） | Recall Storage（召回） |
| --- | --- | --- |
| 存什么 | 任意长度文本：长文档、LLM 主动提炼的要点 | 完整对话消息流水 |
| 谁写入 | LLM 主动调 `archival_storage.insert` | Queue Manager 自动落盘 |
| 典型后端 | PostgreSQL + pgvector + HNSW（余弦相似度） | 带搜索接口的消息库 |

一句话：**Archival = 你让它记的（主动笔记）；Recall = 它帮你记的（全量消息流水）。**

### 溢出控制：两级阈值

| 阈值 | 触发条件 | 系统行为 |
| --- | --- | --- |
| **Warning** | prompt tokens ≈ 70% | 注入"记忆压力告警"，提示 LLM 主动归档 |
| **Flush** | prompt tokens ≈ 100% | 驱逐最早 50% 消息，生成新递归摘要写回队首 |

**易误解点**：warning 不会动 FIFO 队列，只是提醒 LLM 备份；flush 才是强制清理。被驱逐的消息永久保留在 recall storage，随时可检索。

![MemGPT 检索外部数据换入当前上下文](/images/memgpt/memgpt_diagrams_wide_memory_search.png)

*图 2：MemGPT 可以搜索上下文外的数据，把相关信息换入当前上下文窗口。*

### Function Chaining（函数链）

LLM 在函数调用中附带 `request_heartbeat=true`，函数执行完后立即触发下一轮推理，实现多步检索/多步推理。不带标志（yield）则等待下一次外部事件。

![MemGPT 系统总体流程](/images/memgpt/memgpt_system_flow_2.png)

*图 3：固定上下文 LLM 处理器被分层记忆系统与一组"系统调用"函数扩展。*

### 五种典型场景

| 场景 | 触发源 | 函数调用 | 数据流向 | heartbeat |
| --- | --- | --- | --- | --- |
| 写事实 | 用户消息 | `working_context.append` | main→main | no |
| 归档 | warning 系统消息 | `archival_storage.insert` | FIFO→external | yes |
| flush | queue 溢出 | Queue Manager 自动 | FIFO→recall + 更新摘要 | — |
| 检索历史 | 用户消息 | `recall_storage.search` ×N | external→main | yes（链式翻页） |
| 自发行为 | 定时/外部事件 | 任意 | 视情况 | 视情况 |

![MemGPT 在对话中更新已存储信息](/images/memgpt/memgpt_diagrams_wide_memory_correction.png)

*图 4：MemGPT 正在更新存储在 working context 中的信息。*

## 评估场景

1. **文档分析**：处理远超 LLM 上下文长度的大型文档
2. **多轮会话**：在长时间交互中保持上下文感知、人设一致性、长期记忆

两个场景下 MemGPT 均超越现有基于 LLM 的方法。

## 一句话总结

> MemGPT 把 LLM 的 prompt 拆成「系统指令 + working context + FIFO 队列」三段，用 Queue Manager 做两级阈值的溢出控制和递归摘要，用函数调用 + 事件驱动 + 函数链让 LLM 自主地在 main context 与 archival/recall 存储之间"分页"，从而把有限上下文窗口扩展成一个自管理的多级记忆系统。
