---
title: "Abstract + 相关工作"
date: 2026-05-01
draft: false
ShowBreadCrumbs: false
hideMeta: true
weight: 1
---

> 来源：[arXiv:2401.17043](https://arxiv.org/abs/2401.17043)

## 图 1：CRUD 四类任务示例

![CRUD 四类任务示例](/papers/dataset-eval/crud-rag/img-20260501123632.png)

## 1. 图 1 的含义

作者将 RAG 的应用分成四个方面：

- **Create：生成**
  利用检索到的外部信息，辅助模型进行文本续写、创作等生成任务。

- **Read：读取 / 问答 / 理解**
  系统通过外部知识检索来回答问题、解决问答、对话和推理任务，并增强对输入文本的理解。

- **Update：更新 / 纠错**
  系统使用检索到的内容修正输入文本中的错误，包括拼写、语法和事实错误，使文本更准确。

- **Delete：删除 / 压缩 / 摘要**
  系统通过去除不必要细节、简化内容，完成摘要、文本简化等任务。

这里的 **CRUD** 借用了数据库中的四个操作：Create、Read、Update、Delete，用来概括 RAG 的四类能力。

---

## 2. 作者为什么提出 CRUD-RAG？

作者认为，现有很多 RAG 评测只关注**问答**，但 RAG 的能力不止问答，还包括生成、纠错、摘要等。

CRUD-RAG 包含四类评测任务：

1. **文本续写**：对应 Create
2. **问答**：对应 Read，包括单文档问答和多文档问答
3. **幻觉修改**：对应 Update，即纠正模型生成中的事实错误
4. **开放域多文档摘要**：对应 Delete，即从多个文档中提炼核心内容

---

## 3. 数据集构建概览

作者从中国主流新闻网站抓取最新、高质量新闻数据，目的是降低这些数据已经出现在大模型训练集中的可能性。然后基于这些新闻数据，用 GPT-4 自动构建不同任务的数据集。

---

## 4. 论文贡献

1. **提出全面的评测基准**：不只评估问答，还覆盖 RAG 的创建、读取、更新、删除四类应用。
2. **构建高质量评测数据集**：针对文本续写、多文档摘要、问答、幻觉修改等任务分别构建数据。
3. **进行了大量实验**：使用多种指标评估 RAG 系统，并为后续研究者和系统开发者提供实践建议。

---

## 2.2 RAG Benchmarks

现有 RAG 评测主要关注如何判断系统性能，包括答案准确性、检索内容相关性、回答是否忠实于上下文，以及是否存在幻觉。

已有 benchmark 包括：

- **RGB**：基于最新新闻构造问题和答案，评估模型是否能利用外部文档准确回答。评测指标：accuracy、rejection rate、error detection rate、correction rate。
- **ARES**：生成合成问题和答案，并用专门的 LLM judge 评估 RAG 的不同环节（context relevance、answer faithfulness、answer relevance），还会给评分提供统计保证（置信区间）。
- **TruLens-Eval**：提出 RAG Triad（context relevance、groundedness、answer relevance），主要用于评估幻觉问题。
- **RAGAS**：无参考答案评测框架，关注检索系统是否找到相关上下文，以及 LLM 是否忠实利用上下文生成答案。

评测方法大致分两类：

1. **需要标准答案**：accuracy、exact match、ROUGE、rejection rate 等。
2. **不需要标准答案**：直接评估检索内容和生成答案的质量（上下文相关性、答案忠实性、答案相关性）。

---

## 2.3 Citation-Enhanced RAG

传统 RAG 不一定明确标注引用来源，加入 citation 的好处是提高透明度、减少幻觉、增强可追溯性。相关研究代表方法：**AIS**、**SCIFI**、**ALiiCE**。

---

## 总结

现有 RAG benchmark 多数集中在**问答能力、检索质量、答案忠实性和引用质量**上。CRUD-RAG 用 Create、Read、Update、Delete 四类任务来更全面评估 RAG 系统。
