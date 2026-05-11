---
title: "实验结论与调参逻辑"
date: 2026-05-01
draft: false
ShowBreadCrumbs: false
hideMeta: true
weight: 4
---

> 这一章真正想说明的实验逻辑：**RAG 的效果不是只由 LLM 决定的，而是和 chunk、retriever、embedding、top-k 等组件强相关，并且不同任务的最优配置并不一样。**

---

## 0. 实验设置

**Baseline 配置**

| 参数 | 值 |
| --- | --- |
| chunk size | 128 |
| chunk overlap | 0% |
| embedding | bge-base |
| retriever | dense |
| top-k | 8 |
| LLM | GPT-3.5 |

每次只改一个组件，在四类 CRUD 任务上分别评测。为控制成本，实验只用总数据集的 1/5。

**评测指标**

- 整体相似度：BLEU / ROUGE-L / BERTScore（看"像不像参考答案"）
- 关键信息指标：RAGQuestEval Precision / Recall（看"关键信息有没有说到、说得对不对"）

---

## 1. 核心结论：RAG 是强任务依赖系统

**没有一套参数能打所有任务。**

| 任务 | 偏好配置 |
| --- | --- |
| Create（续写） | 大 chunk、大 overlap、大 top-k、Dense 检索 |
| Delete（摘要） | 平衡 precision/recall，BM25 有价值，chunk 不宜过大 |
| Read 单文档 QA | 中小 chunk，top-k 不能太小，Hybrid+Rerank 较稳 |
| Read 多文档 QA | 大 chunk、大 top-k、强烈建议 Hybrid+Rerank，更依赖强 LLM |
| Update（幻觉修改） | BM25，top-k 不敏感，overlap 影响不大 |

---

## 2. Chunk Size

- **续写、多文档 QA**：较大 chunk 更有利，保留原文结构，语义更连贯
- **单文档 QA、幻觉修改**：较小或中等 chunk 更合适，只需定位一句话或一个实体，太大会引入无关信息
- **摘要**：trade-off——大 chunk 召回更多关键信息，但也带来更多冗余

---

## 3. Chunk Overlap

**本质**：补偿切块带来的语义断裂，而不是"提升检索召回"的通用旋钮。

- **续写、摘要、问答**：较大 overlap 往往有帮助，越依赖上下文连贯性的任务收益越大
- **幻觉修改**：对 overlap 不敏感，局部纠错不依赖长程语义衔接
- **三文档 QA**：overlap 过大时，重复内容会占掉有效上下文容量，收益被部分抵消

代价：overlap 越大，chunk 间重复越多，真正新增的信息比例越低。

---

## 4. Retriever

作者比较了 BM25、Dense、Hybrid、Hybrid+Rerank。

| 检索器 | 擅长场景 |
| --- | --- |
| BM25 | 精确命中，适合摘要、幻觉修改等高精度匹配任务 |
| Dense | 语义理解，适合续写、多文档 QA |
| Hybrid+Rerank | 融合后再排序，在问答（尤其多文档 QA）上最稳 |

**MRR 单独评测**（仅在 QA 和幻觉修改上做，续写/摘要的"正确文档"边界模糊）：

| 任务 | Dense | BM25 | Hybrid+Rerank |
| --- | --- | --- | --- |
| QA 1-doc | 49.8 | 49.1 | **52.5** |
| QA 2-doc | 42.3 | 41.3 | **44.2** |
| QA 3-doc | 38.5 | 37.3 | **41.2** |
| Hallucination | 49.3 | **50.4** | 49.3 |

MRR 趋势与端到端实验一致，说明 Hybrid+Rerank 在多文档 QA 上的优势来自检索阶段本身，而不是 LLM 恰好发挥得好。

---

## 5. Embedding

作者比较了 m3e-base、bge-base、stella-base、gte-base。

**核心结论**：embedding 在检索 benchmark 上强，不代表在具体 RAG 任务里一定最好。

| 任务 | 表现 |
| --- | --- |
| 单文档 QA | m3e-base 明显较弱 |
| 幻觉修改 | m3e-base 反而表现最好（MRR 51.2，其他约 49） |

**Embedding MRR 数据**：

| 任务 | BGE | GTE | M3E | STELLA |
| --- | --- | --- | --- | --- |
| QA 1-doc | 49.8 | 49.4 | 47.2 | 48.3 |
| QA 2-doc | 42.3 | 42.0 | 41.8 | 42.3 |
| QA 3-doc | 38.5 | 38.0 | 38.1 | 38.4 |
| Hallucination | 49.3 | 49.2 | **51.2** | 50.6 |

所有 embedding 的 MRR 从 1-doc → 2-doc → 3-doc 系统性下降，说明多文档任务的困难是所有 embedding 共同面临的系统性挑战。

**不存在一个在所有 RAG 子任务上都绝对领先的向量模型，embedding 选择必须任务化。**

---

## 6. Top-k

- **续写**：更大 top-k 往往更好，信息来源更多，内容更丰富
- **多文档 QA**：更大 top-k 很重要，需要更高概率同时找回多篇互补文档
- **摘要**：trade-off，top-k 大则召回更高，但也更容易带来冗余和噪声
- **幻觉修改**：top-k 影响较小，通常只要少量精确信息就够纠错

---

## 7. LLM

作者比较了 GPT-3.5、GPT-4、GPT-4o、ChatGLM2、Baichuan2-13B、Qwen-7B、Qwen-14B、Qwen2-7B。

- **GPT-4** 整体最强，尤其在续写、摘要、多文档推理 QA、幻觉修改上
- **单文档 QA** 不一定是 GPT-4 最强——偏抽取，不太考验复杂推理，开源模型已能很好完成
- **多文档 QA** 差距拉开，更考验证据整合和长上下文理解
- **Qwen-14B** 在续写和摘要上有竞争力；**Baichuan2-13B** 在 QA 上表现不错

---

## 8. 一句话抓住实验章的中心思想

**RAG 优化不是单纯换更强 LLM，而是要根据生成、摘要、问答、纠错这些不同目标，分别设计 chunk、retriever、top-k 和模型组合。**
