---
title: "CRUD-RAG: A Comprehensive Chinese Benchmark for Retrieval-Augmented Generation"
date: 2026-05-01
tags: ["RAG", "Benchmark", "Dataset", "Chinese NLP"]
categories: ["论文笔记"]
draft: false
summary: "CRUD-RAG 用 Create/Read/Update/Delete 四类任务全面评测中文 RAG 系统，覆盖文本续写、问答、幻觉修改和多文档摘要，并系统研究 chunk、retriever、embedding、top-k 等组件对不同任务的影响。"
---

> 来源：[arXiv:2401.17043](https://arxiv.org/abs/2401.17043)

## 章节导航

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:1.2em 0">

<a href="abstract/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">Abstract + 相关工作</div>
<div style="font-size:.85em;opacity:.7">RAG 评测现状与 CRUD 四类任务定义</div>
</a>

<a href="method/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">主要方法：数据集构建</div>
<div style="font-size:.85em;opacity:.7">新闻数据收集、四类任务数据构造流程、RAGQuestEval</div>
</a>

<a href="tasks/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">四类任务构造逻辑</div>
<div style="font-size:.85em;opacity:.7">Create / Read / Update / Delete 构造思路详解</div>
</a>

<a href="experiments/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">实验结论与调参逻辑</div>
<div style="font-size:.85em;opacity:.7">chunk、retriever、embedding、top-k、LLM 对比实验</div>
</a>

<a href="uhgeval/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">补充：UHGEval 数据集</div>
<div style="font-size:.85em;opacity:.7">幻觉评测数据集字段说明与在 CRUD-RAG 中的用途</div>
</a>

</div>

## 一句话概括

CRUD-RAG 把 RAG 的应用场景拆成 Create（续写）、Read（问答）、Update（幻觉纠错）、Delete（摘要）四类，针对每类场景专门设计数据构造方式，让模型不能只靠参数记忆答题，而必须依赖外部检索。实验还系统验证了 RAG 是强任务依赖系统——没有一套参数配置能打所有任务。
