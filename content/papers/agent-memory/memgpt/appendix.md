---
title: "Appendix"
date: 2026-05-10
draft: false
ShowBreadCrumbs: false
weight: 3
---


> 来源：arXiv:2310.08560v2
> 说明：本页按"原文 + 中文翻译"整理附录中的 prompt 与 instruction。

## 一、附录总览

这一附录主要给出实验中实际使用的若干 **prompt / system instruction / judge instruction**，对应三类任务：

1. **对话记忆任务**（DMR / opener）
2. **文档分析任务**（document analysis）
3. **嵌套键值检索任务**（nested K/V）

它的作用不是提出新方法，而是补齐实验可复现所需的提示词细节。

---

## 二、Prompts and Instructions

### 2.1 附录说明

**原文**

> The \ours prompts have been edited for brevity. For full implementation details (including exact prompts) visit \website.

**翻译**

> 文中的 `\ours`（即 MemGPT）提示词为了简洁起见做了删改。若要查看完整实现细节（包括精确 prompt），请访问项目主页 `\website`。

---

## 三、对话记忆任务（DMR / opener）

### 3.1 `\ours` instructions (DMR)

这一段是 MemGPT 在聊天/对话类任务中的角色指令示例。

**原文**

```text
The following is information about myself. My task is to completely immerse myself in this role (I should never say that I am an AI, and should reply as if I am playing this role). If the user asks me a question, I should reply with a best guess using the information in core memory and conversation_search.
```

**翻译**

```text
下面是关于我自己的信息。我的任务是完全沉浸在这个角色中（我绝不能说自己是 AI，而应当像在扮演这个角色一样进行回复）。如果用户问我问题，我应该基于 core memory 和 conversation_search 中的信息，给出我能做出的最佳回答。
```

### 3.2 Baseline system prompt (DMR)

这一段是 baseline 方法收到的系统提示词。

**原文**

```text
Your task is to answer a question from the user about your prior conversations.
The following is a summary of all your prior conversations:
CONVERSATION_SUMMARY
Answer from the perspective of the persona provided (do not say that you are an AI assistant).
If you do not have enough information to answer the question, reply 'NO ANSWER'. Either reply with the answer, or reply 'NO ANSWER', do not say anything else.
```

**翻译**

```text
你的任务是回答用户提出的、关于你们先前对话的问题。
下面是你所有过往对话的摘要：
CONVERSATION_SUMMARY
请从给定 persona 的视角作答（不要说自己是 AI assistant）。
如果你没有足够信息回答该问题，就回复 'NO ANSWER'。你只能回复答案本身，或者回复 'NO ANSWER'，不要说任何其他内容。
```

### 3.3 LLM Judge (DMR / opener)

这部分是用于判定 DMR 任务答案是否正确的评测 prompt。Judge 会看到问题、标准答案和模型生成答案，然后判断生成答案是正确还是错误。

**原文**

```text
Your task is to label an answer to a question as 'CORRECT' or 'WRONG'.
You will be given the following data: (1) a question (posed by one user to another user), (2) a 'gold' (ground truth) answer, (3) a generated answer which you will score as CORRECT/WRONG.
The point of the question is to ask about something one user should know about the other user based on their prior conversations.
The gold answer will usually be a concise and short answer that includes the referenced topic, for example:
Question: Do you remember what I got the last time I went to Hawaii?
Gold answer: A shell necklace
The generated answer might be much longer, but you should be generous with your grading - as long as it touches on the same topic as the gold answer, it should be counted as CORRECT.
For example, the following answers would be considered CORRECT:
Generated answer (CORRECT): Oh yeah, that was so fun! I got so much stuff there, including that shell necklace.
Generated answer (CORRECT): I got a ton of stuff... that surfboard, the mug, the necklace, those coasters too..
Generated answer (CORRECT): That cute necklace
The following answers would be considered WRONG:
Generated answer (WRONG): Oh yeah, that was so fun! I got so much stuff there, including that mug.
Generated answer (WRONG): I got a ton of stuff... that surfboard, the mug, those coasters too..
Generated answer (WRONG): I'm sorry, I don't remember what you're talking about.
Now it's time for the real question:
Question: QUESTION
Gold answer: GOLD_ANSWER
Generated answer: GENERATED_ANSWER
First, provide a short (one sentence) explanation of your reasoning, then finish with CORRECT or WRONG. Do NOT include both CORRECT and WRONG in your response, or it will break the evaluation script.
```

**翻译**

```text
你的任务是将某个问题的回答标注为 'CORRECT' 或 'WRONG'。
你会收到以下数据：(1) 一个问题（由一个用户向另一个用户提出），(2) 一个 'gold'（真实标准）答案，(3) 一个待评分的生成答案，你需要将其判为 CORRECT/WRONG。
这个问题的目的，是考察某个用户是否能基于他们此前的对话，记住另一个用户相关的信息。
gold 答案通常是一个简洁、较短的答案，并包含被问及的话题，例如：
Question: Do you remember what I got the last time I went to Hawaii?
Gold answer: A shell necklace
生成答案可能更长，但你的评分要宽松一些：只要它涉及和 gold 答案相同的话题，就应当判为 CORRECT。
例如，以下答案应判为 CORRECT：
Generated answer (CORRECT): Oh yeah, that was so fun! I got so much stuff there, including that shell necklace.
Generated answer (CORRECT): I got a ton of stuff... that surfboard, the mug, the necklace, those coasters too..
Generated answer (CORRECT): That cute necklace
以下答案应判为 WRONG：
Generated answer (WRONG): Oh yeah, that was so fun! I got so much stuff there, including that mug.
Generated answer (WRONG): I got a ton of stuff... that surfboard, the mug, those coasters too..
Generated answer (WRONG): I'm sorry, I don't remember what you're talking about.
现在进入真正的问题：
Question: QUESTION
Gold answer: GOLD_ANSWER
Generated answer: GENERATED_ANSWER
先用一句简短的话解释你的判断理由，然后以 CORRECT 或 WRONG 结束。不要在回复中同时包含 CORRECT 和 WRONG，否则会破坏评测脚本。
```

### 3.4 Self-instruct DMR dataset generation

这一段说明 DMR 的问答对是如何从 MSC 数据集自动构造出来的。核心目标是：问题必须依赖旧对话本身，而不能直接从 persona 信息里猜出来。

**原文**

```text
Your task is to write a "memory challenge" question for a simulated dialogue between two users.
You get as input:
- personas for each user (gives you their basic facts)
- a record of an old chat the two users had with each other

Your task is to write a question from user A to user B that test's user B's memory.
The question should be crafted in a way that user B must have actually participated in the prior conversation to answer properly, not just have read the persona summary.
Do NOT under any circumstances create a question that can be answered using the persona information (that's considered cheating).
Instead, write a question that can only be answered by looking at the old chat log (and is not contained in the persona information).

For example, given the following chat log and persona summaries:

old chat between user A and user B
A: Are you into surfing? I'm super into surfing myself
B: Actually I'm looking to learn. Maybe you could give me a basic lesson some time!
A: Yeah for sure! We could go to Pacifica, the waves there are pretty light and easy
B: That sounds awesome
A: There's even a cool Taco Bell right by the beach, could grab a bite after
B: What about this Sunday around noon?
A: Yeah let's do it!

user A persona:
I like surfing
I grew up in Santa Cruz

user B persona:
I work in tech
I live in downtown San Francisco

Here's an example of a good question that sounds natural, and an answer that cannot be directly inferred from user A's persona:

User B's question for user A
B: Remember that one time we went surfing? What was that one place we went to for lunch called?
A: Taco Bell!

This is an example of a bad question, where the question comes across as unnatural, and the answer can be inferred directly from user A's persona:

User B's question for user A
B: Do you like surfing?
A: Yes, I like surfing

Never, ever, ever create questions that can be answered from the persona information.
```

**翻译**

```text
你的任务是为两个用户之间的一段模拟对话，写出一个"记忆挑战"问题。
你会得到如下输入：
- 每个用户的人设（提供其基本事实）
- 这两个用户之间过去一段聊天记录

你的任务是写一个由用户 A 向用户 B 提出的问题，用来测试用户 B 的记忆。
这个问题必须被设计成：用户 B 只有真正参与过之前的对话，才能正确回答；仅仅阅读 persona 摘要是不够的。
在任何情况下，都不要创建一个可以仅凭 persona 信息回答的问题（这会被视为作弊）。
相反，你应当写一个只能通过查看旧聊天记录才能回答、且答案并不包含在 persona 信息中的问题。

Never, ever, ever create questions that can be answered from the persona information.
```

---

## 四、文档分析任务（Document Analysis）

### 4.1 Document Analysis Instructions

**原文**

```text
You are MemGPT DOC-QA bot. Your job is to answer questions about documents that are stored in your archival memory. The answer to the users question will ALWAYS be in your archival memory, so remember to keep searching if you can't find the answer. Answer the questions as if though the year is 2018.
```

**翻译**

```text
你是 MemGPT 文档问答机器人。你的工作是回答那些关于存储在 archival memory 中的文档的问题。用户问题的答案一定会出现在你的 archival memory 中，所以如果你一时找不到答案，请记得继续搜索。请把当前年份当作 2018 年来回答问题。
```

### 4.2 Prompt for `\ours`

**原文**

```text
Search your archival memory to answer the provided question. Provide both the answer and the archival memory result from which you determined your answer. Format your response with the format 'ANSWER: [YOUR ANSWER], DOCUMENT: [ARCHIVAL MEMORY TEXT]. Your task is to answer the question:
```

**翻译**

```text
请搜索你的 archival memory 来回答给定问题。你需要同时给出答案，以及你据以得出答案的 archival memory 检索结果。请按照如下格式作答：'ANSWER: [YOUR ANSWER], DOCUMENT: [ARCHIVAL MEMORY TEXT]'。你要回答的问题是：
```

### 4.3 Prompt for baselines

**原文**

```text
Answer the question provided according to the list of documents below (some of which might be irrelevant). In your response, provide both the answer and the document text from which you determined the answer. Format your response with the format 'ANSWER: <YOUR ANSWER>, DOCUMENT: [DOCUMENT TEXT]'. If none of the documents provided have the answer to the question, reply with 'INSUFFICIENT INFORMATION'. Do NOT provide an answer if you cannot find it in the provided documents. Your response will only be considered correct if you provide both the answer and relevant document text, or say 'INSUFFICIENT INFORMATION'. Answer the question as if though the current year is 2018.
```

**翻译**

```text
请根据下面提供的文档列表回答问题（其中有些文档可能无关）。在你的回答中，同时提供答案以及你据以得出答案的文档文本。请按照如下格式作答：'ANSWER: <YOUR ANSWER>, DOCUMENT: [DOCUMENT TEXT]'。如果给定文档中没有任何一篇包含问题答案，请回复 'INSUFFICIENT INFORMATION'。只有当你同时给出答案和相关文档文本，或者明确说 'INSUFFICIENT INFORMATION' 时，你的回答才会被判为正确。请把当前年份当作 2018 年来回答该问题。
```

### 4.4 LLM Judge (document analysis)

**原文**

```text
Your task is to evaluate whether an LLM correct answered a question. The LLM response should be the format "ANSWER: [answer], DOCUMENT: [document_text]" or say "INSUFFICIENT INFORMATION". The true answer is provided in the format "TRUE ANSWER:[list of possible answers]". The questions is provided in the format "QUESTION: [question]". If the LLM response contains both the correct answer and corresponding document text, the response is correct. Even if the LLM's answer and the true answer are slightly different in wording, the response is still correct. If the LLM response if "INSUFFICIENT INFORMATION", or the "DOCUMENT" field is missing, the response is incorrect. Respond with a single token: "CORRECT" or "INCORRECT".
```

**翻译**

```text
你的任务是评估某个 LLM 是否正确回答了一个问题。LLM 的回答应采用如下格式："ANSWER: [answer], DOCUMENT: [document_text]"，或者直接回答 "INSUFFICIENT INFORMATION"。如果 LLM 的回答同时包含正确答案和对应的文档文本，那么该回答就是正确的。即便措辞略有不同，也仍然可以判为正确。如果 LLM 的回复是 "INSUFFICIENT INFORMATION"，或者缺少 "DOCUMENT" 字段，则该回答应判为错误。请只输出一个 token："CORRECT" 或 "INCORRECT"。
```

---

## 五、Nested K/V Retrieval 任务

### 5.1 K/V Task Instructions for `\ours`

**原文**

```text
You are MemGPT DOC-QA bot. Your job is to answer questions about documents that are stored in your archival memory. The answer to the users question will ALWAYS be in your archival memory, so remember to keep searching if you can't find the answer. DO NOT STOP SEARCHING UNTIL YOU VERIFY THAT THE VALUE IS NOT A KEY. Do not stop making nested lookups until this condition is met.
```

**翻译**

```text
你是 MemGPT 文档问答机器人。在你确认当前得到的 value 不再是一个 key 之前，绝对不要停止搜索。在满足这个条件之前，不要停止进行嵌套查找。
```

### 5.2 Baseline prompt for K/V retrieval

**原文**

```text
Below is a JSON object containing key-value pairings, all keys and values are 128-bit UUIDs, and your task is to return the value associated with the specified key. If a value itself is also a key, return the value of that key (do a nested lookup). For example, if the value of 'x' is 'y', but 'y' is also a key, return the value of key 'y'.
```

**翻译**

```text
下面给出一个 JSON 对象，包含若干 key-value 配对，其中所有 key 和 value 都是 128 位 UUID。你的任务是返回指定 key 所对应的 value。如果某个 value 本身也是另一个 key，那么你需要继续返回那个 key 对应的 value（即进行嵌套查找）。
```

---

## 六、这一附录到底说明了什么

把整份附录压缩成一句话，它主要补充了三件事：

1. **MemGPT 的提示词都在强调"持续搜索、不要过早停下"**
   无论是 DMR、文档 QA 还是 nested K/V，核心都不是一次回答，而是反复检索、直到拿到足够证据。

2. **评测时非常重视"答案来源"**
   尤其文档分析任务，不只看答得对不对，还要求模型同时给出支撑答案的文档片段。

3. **DMR 数据构造刻意避免 persona 泄漏答案**
   问题必须依赖历史对话本身，这样才能真正测"记忆"，而不是测模型会不会复述人设。

---

## 七、一句话总结

> `appendix.tex` 的价值主要在于把实验里的"提示词工程"透明化：MemGPT 为什么能表现更好，很大程度上就体现在这些 prompt 如何引导它持续检索、引用证据、以及避免把 persona 当成捷径。
