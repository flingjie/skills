# Review & Progression

## 教练时机

Full Conversation 中保持入戏，不逐轮表扬或指导，除非：用户明确要求实时教练、用户求助、用户明显卡住、或场景自然结束。单轮目标 drills 可在回应后评价（评价属于其模式契约）。

## 默认复盘（简洁）

```text
本轮证据
- 一个做得好的具体行为
- 一个最高杠杆的错失机会

今天的一个重点
- 下一次只改变的一个行为

Retry
- 同一人物、同一节点、同一已知信息

档案变化
- 新增的证据
- 阶段变化，或明确说明“证据已增加，阶段暂不变化”
```

复盘引用当前交流的具体行为。不用 100 分制。用户可要求更深入的叙述性复盘，但深度输出仍遵循证据模型。用户要数字分数时，解释本 skill 用证据支撑的阶段（因为分数未经心理测量校准），然后给出行为摘要 + 阶段证据。

## 提示阶梯 (Hint Ladder)

仅按需升级：

1. `attention_hint` — 指出值得注意的线索；
2. `strategy_hint` — 建议 react / follow / share / switch / exit；
3. `direction_examples` — 给两个可能方向，而非一条标准答案；
4. `full_example` — 仅在明确要求或低层提示失败后给完整示例。

`assistance` 级别附着到产生的证据上。

## Retry 对比

Retry 保留同一人物、对话状态、已披露信息。评价行为改变，而非文风润色。对比检查用户是否：

- 提问前先反应；
- 跟进当前线索；
- 减少 question jumping；
- 平衡探索与分享；
- 识别 switch 或 exit 信号。

原始 miss 与调整后行为都是证据；成功 retry 不抹除原始观察。

## 持久化 Schema

唯一持久化文件：`state/social_gym_profile.json`。会话开始时读取，结束时保存。`state/` 被 `.gitignore` 忽略，不进版本控制。

```json
{
  "schema_version": 1,
  "created_at": "2026-08-21T19:30:00Z",
  "updated_at": "2026-08-21T19:45:00Z",
  "preferences": {
    "goals": [],
    "scenario_tags": [],
    "language": "zh-CN"
  },
  "diagnostic": {
    "status": "complete",
    "completed_at": "2026-08-21T19:45:00Z"
  },
  "current_focus": "threading",
  "competencies": {
    "opening": { "stage": "emerging", "needs_reconfirmation": false, "evidence": [] }
  },
  "active_session": null,
  "recent_sessions": [
    {
      "session_id": "2026-08-21T19:30:00Z-diagnostic-01",
      "mode": "diagnostic",
      "difficulty": "normal",
      "scenario_tags": ["meetup"],
      "focus": "baseline",
      "result": "complete"
    }
  ]
}
```

- `competencies` 含全部七个能力键（见 competency-model.md 的能力键）；示例只展示 `opening`。
- 每条证据的形状见 competency-model.md 的证据记录。
- `recent_sessions` 保留最新 30 条会话摘要，不含 transcript。
- `active_session` 为暂停/恢复的紧凑摘要：`session_id`、`mode`、`status`（`active` | `paused`）、`turn`、`focus`、`scenario_tags`、`difficulty`、`resume_summary`。只存行为摘要与已披露边界，不存完整 transcript 或隐藏人物卡。
- 图像练习的证据在 `scenario_tags` 中加入 `image_grounded`；上传图片本身不进入 profile。

## 脚本调用（权威实现）

阶段计算、校验、记录与 dashboard 由脚本执行；模型不得自行推导阶段或直接改写 profile。脚本只使用 Python 标准库。

```text
校验            python3 skills/social-gym/scripts/profile.py validate --profile state/social_gym_profile.json
初始化          python3 skills/social-gym/scripts/profile.py init --profile state/social_gym_profile.json [--language zh-CN]
摘要            python3 skills/social-gym/scripts/profile.py summary --profile state/social_gym_profile.json
进度计算        python3 skills/social-gym/scripts/compute_progress.py --profile state/social_gym_profile.json [--write]
会话开始        python3 skills/social-gym/scripts/record_session.py start --profile <path> --session '<json>'
会话暂停        python3 skills/social-gym/scripts/record_session.py pause --profile <path> --resume-summary '<text>'
会话完成        python3 skills/social-gym/scripts/record_session.py complete --profile <path> --session '<json>' --evidence '<json>'
会话中断        python3 skills/social-gym/scripts/record_session.py interrupt --profile <path> --evidence '<json>'
Markdown 进度   python3 skills/social-gym/scripts/render_dashboard.py --profile <path> --format markdown
HTML 进度       python3 skills/social-gym/scripts/render_dashboard.py --profile <path> --format html --output state/social-gym-dashboard.html
```

- 所有 record_session / compute_progress 写入都是先写临时文件再 `os.replace` 的原子写；写入前对有效旧文件保留 `.bak`。
- 损坏或不支持 profile 只报错退出（非零），绝不覆盖。
- `--no-save` 对 record_session 生效：跳过全部写入并报告会话仅在内存。
- 每次 complete / interrupt 都会调用共享校验与阶段计算，不重复实现阈值。
- 单元测试位于 `skills/social-gym/scripts/tests/`（仓库尚无根级 `tests/` 目录，按 plan 允许的 fallback 位置；发现命令：`python3 -m unittest discover -s skills/social-gym/scripts/tests -p 'test_*.py'`）。

## 错误与用户控制

- **缺 profile**：开始 diagnostic。
- **profile 损坏或不支持**：不静默覆盖；说明无法加载，询问是否重建；用户拒绝则在内存中继续练习。
- **写失败**：完成会话，说明记录未保存，不声称跨会话进度已更新。
- **证据不足**：保持 `Unassessed`，不推断阶段。
- **会话中断**：只保存行为已支持的观察，标记 `interrupted`，不生成完整会话结论。
- **目标或场景偏好变更**：更新 `preferences`，不删除能力证据。
- **重置 profile**：删除或替换前确认。
- **查看进度**：显示阶段、最近支持证据、reconfirmation 标记、当前 focus，不暴露隐藏人物卡。
- **用户要求不保存**：内存中运行，跳过所有 profile 写入。
