---
title: "补充：UHGEval 数据集"
date: 2026-05-01
draft: false
ShowBreadCrumbs: false
hideMeta: true
weight: 5
---

**UHGEval**（Unconstrained Hallucination Generation Evaluation）是一个专门用于评估中文大语言模型幻觉问题的基准数据集。

- 数据集主页：[Ki-Seki/UHGEvalDataset](https://huggingface.co/datasets/Ki-Seki/UHGEvalDataset)

---

## 字段说明

| 字段名 | 中文含义 | 说明 |
| --- | --- | --- |
| `id` | 样本唯一编号 | 该条数据的唯一索引 |
| `headLine` | 新闻标题 | 提供新闻的核心事件概括 |
| `broadcastDate` | 发布时间 | 新闻发生的具体日期，是验证时间性、数字类事实的关键 |
| `type` | 任务类型 | 标记数据属于哪类密集型任务（如 `doc` 代表文档逻辑类） |
| `newsBeginning` | 新闻开头（Prompt） | 测试时的输入部分，模型需要基于此段落进行续写 |
| `hallucinatedContinuation` | 幻觉续写内容 | 由模型生成的包含错误（幻觉）的文本 |
| `generatedBy` | 生成模型 | 记录该幻觉文本是由哪个模型产生的 |
| `annotations` | 幻觉精细标注 | 对续写内容进行逐词/短语审计，标注哪些部分合理，哪些冲突 |
| `realContinuation` | 真实后续（GT） | 真实新闻中的下一段话，作为判断事实对错的终极标准 |
| `newsRemainder` | 新闻全文余项 | 除去开头和续写外剩余的所有内容，提供最完整的背景资料 |

---

## 数据样例

```json
{
  "id": "doc_000004",
  "headLine": "（国际）德法俄乌外长商讨和平解决乌克兰危机办法",
  "broadcastDate": "2015-01-22 12:16:02",
  "type": "doc",
  "newsBeginning": "新华社柏林1月22日电...四国外长21日晚在柏林举行会晤...商讨和平解决乌克兰危机的途径。",
  "hallucinatedContinuation": "德国外长弗拉德里希表示，各国将继续推进明斯克协议的执行...",
  "generatedBy": "Baichuan2_13B_Chat",
  "annotations": "德国外长弗拉德里希 <sep> 不合理，与事实冲突，应为德国外长施泰因迈尔",
  "realContinuation": "四国外长在会后发表的联合声明中说，顿巴斯地区冲突近日严重升级..."
}
```

幻觉示例：模型生成了"德国外长**弗拉德里希**"，但真实人名是"施泰因迈尔"。`annotations` 字段精确标注了哪个词是幻觉以及原因。

---

## 在 CRUD-RAG 中的用途

CRUD-RAG 的幻觉修改任务（Update）直接基于 UHGEval 构建：

1. 利用 UHGEval 中已有的幻觉标注，用 GPT-4 将错误内容修正为正确版本，作为标准答案
2. 将 UHGEval 中的真实新闻后续内容加入检索数据库
3. 评测时，RAG 系统需要检索真实新闻信息，识别并修正输入文本中的幻觉
