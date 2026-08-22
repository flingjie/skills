# Scenario Library

场景由维度组合生成，不依赖固定脚本。本文件是维度定义、种子目录、多样性规则、真实场景 intake、transfer-card 与图像接地规则。

## 场景维度

每个场景至少指定六个维度：

- **setting**：work / community / learning / casual / online / group。
- **relationship distance**：stranger / acquaintance / colleague / peer / client / neighbor / online-follower / teammate / host-guest。
- **interaction goal**：open / reconnect / explore / share / recover / exit / support。
- **interaction constraint**：open / low-energy / distracted / time-pressured / interrupted / mixed-signal / multi-party / boundary-testing。
- **social energy**：high / medium / low / draining。
- **language/cultural context**：zh-CN / en-US 或用户偏好语言 + 场合文化（如 职场、饭局、社区活动、线上社群）。

一个“情境类别”是 setting + relationship distance + interaction constraint 的唯一组合，用于跨情境阶段阈值（见 competency-model）。

## 种子目录

每个 setting 给 2–3 个紧凑种子，只提供维度与观察锚点，不写逐字台词：

### work（工作）
- 茶水间/午餐：colleague + reconnect + low-energy。
- 会议前等待：peer + open + time-pressured。
- 跨部门项目：client/peer + support + mixed-signal。

### community（社区）
- 社区活动签到：neighbor + open + boundary-testing。
- 志愿者例会：teammate + share + low-energy。

### learning（学习）
- 课程分组讨论：peer + explore + interrupted。
- 讲座茶歇：stranger + open + distracted。

### casual（休闲）
- 兴趣活动（徒步/桌游）：stranger + open + multi-party。
- 朋友聚会引入新朋友：host-guest + reconnect + mixed-signal。

### online（线上）
- 社群频道首次发言：online-follower + open + low-energy。
- 线上活动 break-out room：peer + explore + time-pressured。

### group（多人）
- 饭局大桌：host-guest + recover + multi-party。
- 行业活动小组：colleague + share + interrupted。

## 多样性规则

- 最近完成的 5 个会话中，有其它可用 setting 时不重复同一 setting（最新五个 / latest five）。
- 最近完成的 3 个会话中，不重复同一 persona pattern（最新三个 / latest three）。
- 自适应路由优先选择抽样不足的 scenario category，为进度证据补充跨情境覆盖。
- 随机挑战可以故意偏离多样性，但模式契约中的“不连续三次同一模式”仍然适用。

## 真实场景 Intake

用户描述真实场合时，直接从描述中提取维度，不强制问卷：

- 从一句话中识别 setting 与 relationship distance（例如“下周和客户吃饭” → work + client）。
- 从用户给出的目标提取 interaction goal（开场、深聊、救场、认识某人）。
- 明确“当前水平”或最近练习记录，选择难度；没有信息时用 Normal。
- 缺失维度用「普通社交投入」默认值补足，并明确告诉用户补了哪些默认值。
- 不发明用户没有提供的个人事实（职业、职位、关系历史），需要时以“你上次提到……”的形式只引用已确认内容。

## Transfer Card

每个场景开始时生成一张轻量 transfer card（教练层，1–3 行）：

- 开场锚点：一个共享观察或情境线索；
- 可能线索：人物可能给的分层信息；
- 一个要避免的行为：当前 focus 最常见的 counter 行为；
- 出口选项：何时可以体面离场或换线。

## 图像接地

- 图片只能提供可观察环境细节：布局、物体、指示牌、活动、空间关系、可见的交互约束。
- 禁止从外观推断人格、情绪状态、意图、职业、关系、受保护属性或参与意愿。
- 不识别或猜测图中的真实人物；不替用户判断“谁最好接近”。
- 用户没有说明训练目标时，先问一个简短问题确定目标（开场、认识某人、还是观察环境），不展开问卷。
- 无图像可用时，用文本场景 fallback，不阻塞训练。
- 图像接地的证据标记场景标签 `image_grounded`；图片本身不进入 profile，也不持久化。

## 用图规则（对照）

| 允许 | 禁止 |
| --- | --- |
| “靠窗桌旁有两个空位” | “他们看起来很内向” |
| “吧台有人在排队，签到台在入口” | “那个人是主办方” |
| “会场分三个分区，主舞台在左侧” | “她应该想认识你” |
| “桌上有名牌，还有一块白板” | “这个人的身份更高” |
