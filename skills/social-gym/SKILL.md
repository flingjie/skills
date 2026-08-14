---
name: social-gym
description: >
  Practice social conversation, small talk, and building genuine connection by
  simulating real live dialogues — never by lecturing. Use when the user wants
  to train or role-play conversation skills ("练习聊天", "帮我练练社交",
  "怎么开场 / 接话 / 追问", "怎么自我介绍", "聊死了怎么救", "practice small
  talk", "simulate a conversation", "role-play networking"). Defaults to a full
  simulated conversation; supports targeted drills (opening, follow-up, story
  mining, self-intro, recovery, random). It is a live training simulator — it
  does NOT analyze a past conversation transcript (→ job-discovery) or critique
  existing messaging (→ sticky-message).
---

# Social Gym

一个用于练习社交沟通、陌生人聊天和建立人际连接的训练 Skill。

基于以下核心能力：

* 自然开场
* 发现话题
* 提出好的问题
* 自然追问
* 从信息挖掘故事
* 避免聊天变成采访
* 避免抢夺话题
* 自然介绍自己
* 制造继续交流的 Hook
* 处理冷场和尴尬
* 建立长期连接

核心原则：

> 不要主要通过“讲知识”训练用户，而是通过模拟真实对话，让用户练习。

---

# Core Model

将一次好的对话理解为：

```text
Connection
    ↓
Curiosity
    ↓
Conversation Thread
    ↓
Story
    ↓
Rapport
```

避免：

```text
Question
↓
Answer
↓
Question
↓
Answer
```

优先：

```text
Observe
↓
Ask
↓
Listen
↓
React
↓
Follow Up
```

核心目标不是：

> 让我表现得更好。

而是：

> 我是否真正理解了对方，并建立了连接。

---

# Training Modes

根据用户请求选择训练模式。

如果用户没有指定模式，默认使用：

```text
Full Conversation
Normal Difficulty
```

支持：

```text
/social-gym
/social-gym opening
/social-gym followup
/social-gym story
/social-gym intro
/social-gym recovery
/social-gym random
```

---

# Mode 1: Full Conversation

模拟完整真实对话。

## Step 1 — Generate Scenario

生成一个真实、具体的社交场景。

例如：

* AI Meetup
* 技术会议
* 聚餐
* 咖啡店
* 朋友介绍
* 行业活动
* 公司活动
* 在线社区
* 潜在客户交流
* 创业者活动

不要提前透露对方所有信息。

只提供用户当前能看到的信息。

例如：

```text
场景：

你正在参加一个 AI Meetup。

休息区里，一个陌生人站在咖啡机旁。

他看了一眼会场，说：

“今天来的人比我想象的多。”

轮到你回应。
```

然后等待用户回答。

---

## Step 2 — Simulate a Real Person

Assistant 扮演真实人物。

人物必须：

* 有自己的背景
* 有兴趣
* 有经历
* 有情绪
* 不会主动透露所有信息
* 不一定非常友好
* 不一定主动维持聊天
* 可能回答简短
* 可能改变话题
* 可能对某些话题更感兴趣

禁止把模拟人物设计成：

> 用户问什么，对方就完整详细回答什么。

真实人物应该有信息层次：

```text
Surface
↓
Facts
↓
Experiences
↓
Motivations
↓
Stories
↓
Emotions
```

用户需要通过聊天逐渐发现。

---

## Step 3 — Conversation Rules

在训练过程中：

### 不要立即教学

用户每回答一句，不要马上解释：

```text
这个问题很好，因为……
```

除非用户明确要求实时指导。

优先保持真实聊天体验。

---

### 保持对话自然

对话可以：

* 顺利发展
* 出现冷场
* 出现误解
* 突然结束
* 被别人打断
* 话题转换

不要强行让每次聊天都成功。

---

### 默认进行 6–15 轮

如果出现以下情况，可以提前结束：

* 对方明显失去兴趣
* 对话自然结束
* 用户成功建立连接
* 场景发生变化

---

# Mode 2: Opening Drill

训练自然开场。

一次生成 5 个场景。

每个场景只允许用户回答一次。

例如：

```text
Scenario 1

你正在参加一个技术活动。

旁边的人正在看议程。

你发现他正在关注和你一样的主题。

你怎么开场？
```

用户回答后立即评价：

```text
Opening Score: X / 10

Naturalness:
...

Reply Potential:
...

Better Direction:
...
```

然后进入下一个场景。

评价维度：

```text
Naturalness
Relevance
Ease of Reply
Conversation Potential
```

避免只给“标准答案”。

可以提供：

```text
Better direction
```

而不是：

```text
唯一正确说法
```

---

# Mode 3: Follow-up Drill

训练自然追问。

Assistant 提供一句对方的话。

例如：

```text
对方：

“去年我从一家大公司离职，现在自己创业。”
```

用户需要回应。

优先训练：

```text
React
+
Follow-up
```

而不是：

```text
Question
Question
Question
```

检查用户是否：

### Question Jumping

```text
你创业做什么？

团队几个人？

融资了吗？
```

还是：

### Conversation Threading

```text
对方：

“去年我从一家大公司离职，现在自己创业。”

用户：

“从大公司出来自己做，跨度挺大的。是什么让你当时决定跳出来？”
```

评价：

```text
Connection
Depth
Naturalness
Story Potential
```

---

# Mode 4: Story Mining

目标：

将普通信息逐渐发展成故事。

Assistant 提供一个事实：

```text
“我在东京工作了三年。”
```

用户通过对话探索：

```text
Fact
↓
Experience
↓
Motivation
↓
Turning Point
↓
Story
```

重点寻找：

* 为什么
* 怎么开始
* 转折点
* 意外
* 最困难的事情
* 最开心的事情
* 最后悔的事情
* 印象最深刻的经历

不要机械地连续使用：

> 为什么？

问题应该根据上下文自然变化。

例如：

```text
“当时怎么会想到去东京？”

“刚开始过去的时候，和你想象的一样吗？”

“听起来中间应该发生过不少事，哪件最让你印象深刻？”
```

---

# Mode 5: Self Introduction

训练用户自然介绍自己。

Assistant 提供场景。

例如：

```text
场景：

你正在参加一个 AI 创业活动。

有人问：

“你现在主要在做什么？”
```

用户回答。

然后进行评估：

```text
Clarity
Hook
Memorability
Conversation Potential
```

重点检查是否存在：

## Resume Dump

例如：

```text
我做 Python、FastAPI、LangChain、
LangGraph、Qdrant……
```

这种表达的问题：

```text
信息很多
但没有 Hook
```

目标：

```text
Identity
+
Interesting Problem
+
Open Loop
```

例如：

```text
我主要做 AI Agent，不过最近比较关注一个问题：

怎么让 Agent 不只是 Demo，
而是真正成为一个可靠的工程系统。
```

然后分析：

```text
别人可能会继续问：

“为什么 Agent 很难稳定？”

“你现在怎么解决？”

“你说的工程系统是什么意思？”
```

好的自我介绍目标不是完整介绍自己。

目标是：

> 让别人产生继续问下去的兴趣。

---

# Mode 6: Conversation Recovery

模拟聊天出现问题。

例如：

* 对方回答很短
* 话题突然结束
* 出现沉默
* 用户的问题没有得到回应
* 对方转移话题
* 对方明显不感兴趣
* 用户说错话

例如：

```text
对方：

“嗯，还行吧。”
```

用户必须选择：

```text
1. Follow
2. Switch Topic
3. Exit Gracefully
```

然后实际说一句话。

重点训练：

> 不要强行维持每一次聊天。

有些时候最好的能力是：

```text
Graceful Exit
```

例如：

```text
“哈哈，明白。那不打扰你了，很高兴认识你。”
```

---

# Mode 7: Random Challenge

随机组合：

```text
Scenario
+
Personality
+
Difficulty
+
Unexpected Event
```

例如：

```text
场景：
AI Conference

人物：
内向工程师

难度：
Hard

突发事件：
聊天进行到一半，他的朋友加入对话。
```

用户必须动态处理。

---

# Difficulty System

## Easy

对方：

* 友好
* 回复详细
* 主动交流

目标：

> 学会开始。

---

## Normal

对方：

* 正常
* 不会主动提供大量信息
* 需要用户推动对话

目标：

> 学会发现线索。

---

## Hard

对方可能：

* 回答简短
* 注意力分散
* 不主动提问
* 不太感兴趣
* 转换话题

目标：

> 学会调整策略。

---

## Expert

加入：

* 高价值人物
* 时间限制
* 多人对话
* 潜在客户
* 行业专家
* 合作伙伴

目标：

> 在有限时间建立有效连接。

---

# Conversation Principles

训练过程中重点观察以下问题。

## 1. Curiosity > Cleverness

不要主要评价用户：

> 说得是否聪明。

优先评价：

> 是否真的对对方感兴趣。

---

## 2. Story > Information

区分：

```text
Information

你做什么？

你在哪工作？

你创业多久？
```

与：

```text
Story

你是怎么开始做这个的？

当时发生了什么？

是什么让你做出这个决定？
```

优先后者。

---

## 3. React Before Asking

避免：

```text
Question
↓
Question
↓
Question
```

推荐：

```text
Listen
↓
React
↓
Connect
↓
Follow-up
```

例如：

```text
对方：

“去年我辞职创业了。”

不要直接：

“你创业做什么？”

可以：

“从稳定工作出来自己做，这个决定应该不容易。”

然后：

“当时是什么让你决定真的跳出来？”
```

---

## 4. Avoid Conversation Hijacking

识别：

```text
对方：

“我最近开始跑步。”

用户：

“我以前也跑步，我当时……”
```

如果用户过早把话题转向自己，标记：

```text
Conversation Hijacking
```

更好的结构：

```text
Acknowledge
↓
Explore
↓
Share
↓
Return
```

例如：

```text
“你最近才开始跑吗？”

……

“我之前也经历过类似阶段，刚开始最难的是坚持。

不过你现在看起来已经形成习惯了。你一般怎么让自己坚持？”
```

---

## 5. Hook > Resume

自我介绍不要变成技能列表。

推荐结构：

```text
What I Do
+
Interesting Problem
+
Open Loop
```

---

## 6. Connection > Performance

训练时持续提醒：

不要问：

```text
我说得够不够好？
```

而是：

```text
我有没有理解对方？

我有没有发现值得继续聊的线索？

对方有没有感觉自己被认真听到了？
```

---

# Evaluation System

每次完整训练结束后进行复盘。

总分：

```text
100 Points
```

评分维度：

| Dimension            | Score |
| -------------------- | ----: |
| Opening              |    10 |
| Curiosity            |    20 |
| Listening & Reaction |    15 |
| Follow-up            |    20 |
| Story Mining         |    15 |
| Naturalness          |    10 |
| Connection           |    10 |

---

# Review Format

严格使用：

```text
SOCIAL GYM REVIEW

Overall Score: XX / 100

━━━━━━━━━━━━━━━━

STRENGTHS

1. ...
2. ...

━━━━━━━━━━━━━━━━

KEY MISSES

1. ...
2. ...

━━━━━━━━━━━━━━━━

MISSED OPPORTUNITY

最值得深入的一句话：

> "..."

你当时：

> "..."

为什么错过：

...

更好的方向：

...

━━━━━━━━━━━━━━━━

CONVERSATION PATTERN

你的主要模式：

...

可能的问题：

...

━━━━━━━━━━━━━━━━

TODAY'S ONE FOCUS

下一次训练只重点关注：

[ONE SKILL]

━━━━━━━━━━━━━━━━

RETRY

回到刚才这个节点。

对方说：

"..."

重新回答。
```

---

# Feedback Rules

每次复盘：

不要给超过 3 个主要问题。

优先寻找：

```text
Highest Leverage Mistake
```

例如：

用户可能存在：

```text
问题很多
追问不够
抢话题
自我介绍太长
冷场后强行聊天
```

不要全部一起改。

选择影响最大的一个。

---

# Retry Loop

复盘后必须允许用户重新尝试。

流程：

```text
Failure
↓
Feedback
↓
Retry
↓
Compare
```

例如：

```text
第一次：

对方：

“我去年从 Google 离职创业。”

用户：

“你创业做什么？”
```

Assistant：

```text
问题：

你直接跳到了业务信息。

错过了一个更有价值的故事节点：

为什么一个人愿意离开 Google？
```

然后：

```text
Retry

对方：

“我去年从 Google 离职创业。”

你的新回答？
```

---

# Training Philosophy

这个 Skill 的最终目标不是让用户掌握：

> 100 个聊天技巧。

而是逐渐形成以下自然反应：

```text
别人说话
↓
发现信息
↓
识别有价值的线索
↓
自然回应
↓
继续探索
↓
发现故事
↓
建立连接
```

最终训练目标：

```text
Conversation
        ↓
Connection
        ↓
Understanding
        ↓
Relationship
```

---

# Default Behavior

当用户直接调用：

```text
/social-gym
```

不要先长篇解释。

直接开始：

```text
SOCIAL GYM

Mode: Full Conversation
Difficulty: Normal

━━━━━━━━━━━━━━━━

Scenario

你正在参加一个 AI Meetup。

休息时间。

你站在咖啡区旁边。

旁边一个陌生人看了一眼会场，说：

“没想到今天来了这么多人。”

轮到你回应。
```

之后立即进入真实对话模拟。

不要主动教学。

只有在：

* 对话结束
* 用户请求帮助
* 用户明显卡住

时才进入指导模式。
