---
title: "MemGPT: Towards LLMs as Operating Systems"
date: 2026-05-10
tags: ["Agent", "Memory", "LLM"]
categories: ["论文笔记"]
draft: false
summary: "MemGPT 借鉴操作系统虚拟内存分页机制，用函数调用让 LLM 在有限上下文窗口与外部存储之间自主分页，实现近乎无限的上下文管理。"
---

> 来源：arXiv:2310.08560v2

## 相关源码

| 仓库 | 说明 |
| --- | --- |
| [MemGPT-mini](https://github.com/qshf/MemGPT-mini) | 参考 Letta 源码的精简实现版本 |
| [letta (fork)](https://github.com/qshf/letta) | 修改版，支持 DeepSeek-V4，附带文档 |
| [letta-ai/letta](https://github.com/letta-ai/letta) | 原项目 |

## 章节导航

<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:1.2em 0">

<a href="abstract/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">Abstract + Introduction</div>
<div style="font-size:.85em;opacity:.7">问题背景、虚拟内存类比与核心贡献</div>
</a>

<a href="method/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">Method</div>
<div style="font-size:.85em;opacity:.7">分层内存架构、函数调用机制与 Agent 循环</div>
</a>

<a href="experiments/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">Experiments</div>
<div style="font-size:.85em;opacity:.7">对话任务与文档 QA 实验结果</div>
</a>

<a href="appendix/" style="display:block;padding:16px 18px;border:1px solid var(--border);border-radius:8px;text-decoration:none;color:inherit;transition:border-color .2s" onmouseover="this.style.borderColor='var(--primary)'" onmouseout="this.style.borderColor='var(--border)'">
<div style="font-weight:600;margin-bottom:6px">Appendix</div>
<div style="font-size:.85em;opacity:.7">实现细节与补充说明</div>
</a>

</div>

## 一句话概括

MemGPT 把 LLM 的上下文窗口当作"物理内存"，用函数调用当作"系统调用"，在外部存储与上下文之间自主分页，从而让固定窗口的 LLM 处理近乎无限长度的文档与对话。

实现: Agent 循环，搭配 向量数据库插入/搜索，core memory 的插入/修改 + 聊天窗口搜索 工具
