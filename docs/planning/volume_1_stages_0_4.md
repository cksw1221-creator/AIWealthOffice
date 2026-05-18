# Multica + GenericAgent AI 财富办公室：详细实现路径

> 目标：实现一个有组织结构、有责任链、有质检、有复盘、有资产沉淀的 AI 财富办公室。
> 用户=董事长；GenericAgent=AI CEO；Multica=协作/执行层；AI workers=PM/Coder/投研/投顾/质检/秘书等员工。

---

## 0. 总体路线

不要一开始做大而全平台。正确路线：

```text
先做 GA 外部 CEO
→ 打通 Multica 调度闭环
→ 跑通一个最小 AI 财富办公室项目
→ 逐步沉淀角色、数据、回测、质检、报告
→ 产品化成可持续运转的一人公司系统
```

核心闭环：

```text
用户目标
→ CEO 拆解
→ Multica 分派
→ worker 执行
→ CEO 拉结果
→ CEO 判断质量
→ CEO 返工或汇总
→ 用户决策
```

完整阶段：

```text
0. 现状探测与基线确认
1. Multica CLI Adapter
2. CEO 任务模型与 Issue 协议
3. 角色 Prompt 与 Worker 协作协议
4. 最小量化任务闭环
5. 质检与返工系统
6. 报告与决策包系统
7. 沉淀资产与工作流产品化
8. 完整 AI 财富办公室
9. 数据资产与策略资产库
10. 多 Agent 运营治理
11. 安全、合规与风控边界
12. 商业化 / 产品形态演进
13. 自我改进与反思系统
14. 从量化扩展到通用 AI 办公室
```

执行分批：

```text
第一批：0→1→2→3→4，让系统活起来
第二批：5→6→11，让系统可信
第三批：7→9→10→13，让系统可复用、会进化
第四批：8→12→14，让系统规模化、产品化
```

---

# 第 1 卷：阶段 0-4，让系统活起来

## 阶段 0：现状探测与基线确认

### 目标

搞清楚当前环境已经有什么、缺什么，避免凭空造系统。

### 探测对象

#### 0.1 Multica CLI

需要确认：

```bash
multica --version
multica issue create ...
multica issue list --output json
multica issue get <id> --output json
multica issue assign <id> --to <agent>
multica issue comment add/list/delete
multica issue runs <issue-id> --output json
multica issue run-messages <task-id> --output json
multica workspace ...
multica agents ...
multica projects ...
```

### 0.2 Worker 能力

确认当前可用 worker：

```text
Claude Code
Codex
OpenClaw
Hermes
其他 Multica agents
```

每个 worker 记录：

```json
{
  "name": "claude-code",
  "can_code": true,
  "can_read_write_files": true,
  "can_network": false,
  "can_be_assigned": true,
  "can_be_mentioned": true,
  "known_risks": ["long task may timeout"]
}
```

### 0.3 GenericAgent 当前接入点

确认：

```text
GA 如何调用 shell
GA 如何保存任务状态
GA 是否能轮询
GA 是否能解析 JSON
GA 是否有计划模式/反思模式
GA 是否能调用 Multica CLI
```

### 0.4 量化基础设施

确认：

```text
是否已有 A股数据目录
是否已有 backtrader 环境
是否已有聚宽策略样本
是否已有报告模板
是否已有 akshare/tushare/baostock/csv 数据源
```

### 阶段 0 产出

```text
environment_report.md
multica_capability_matrix.json
worker_registry.json
current_gap_list.md
```

### 验收标准

CEO 能回答：

```text
Multica CLI 是否可用？
有哪些 worker？
哪个 worker 适合做什么？
当前能否 create→assign→fetch？
量化 demo 缺哪些基础设施？
```

---

## 阶段 1：Multica CLI Adapter

### 目标

给 GA 做一个稳定的 Multica 外部控制器，避免业务逻辑里到处拼 CLI 命令。

结构：

```text
GenericAgent
  → MulticaClient
    → multica CLI
```

### 建议模块

```text
ga_multica/
  __init__.py
  client.py
  models.py
  errors.py
  parser.py
  polling.py
```

### client.py

封装：

```python
create_issue(title, body, project=None, labels=None) -> Issue
assign_issue(issue_id, agent) -> Issue
list_issues(status=None) -> list[Issue]
get_issue(issue_id) -> Issue
add_comment(issue_id, content, parent=None) -> Comment
list_comments(issue_id) -> list[Comment]
list_runs(issue_id) -> list[Run]
list_run_messages(task_id, after=None) -> list[Message]
```

### models.py

定义：

```python
Issue
Comment
Run
Message
Worker
TaskResult
```

每个对象保留：

```text
id
title/content
status
created_at
updated_at
raw_json
```

### errors.py

定义：

```python
MulticaCommandError
MulticaJSONParseError
MulticaTimeoutError
MulticaWorkerStuckError
```

### polling.py

实现：

```python
wait_issue_done(issue_id, timeout, interval)
wait_run_messages(task_id, after=None)
watch_issue(issue_id)
```

### 关键原则

```text
能用 --output json 必须用 JSON
不能用 JSON 的输出必须独立 parser
所有 raw stdout/stderr 都保存
所有命令必须有 timeout
失败要保存 command/stdout/stderr/exit_code
```

### 阶段 1 验收

跑通 Hello Worker：

```text
GA 创建 issue：请 worker 返回 hello + 当前时间 + JSON
GA 分派给 worker
GA 轮询 runs/messages
GA 解析输出
GA 判断是否符合 schema
```

成功标准：

```text
无需人工介入，完成 create → assign → wait → fetch → summarize
```

---

## 阶段 2：CEO 任务模型与 Issue 协议

### 目标

让 GA CEO 用标准协议发任务，而不是随口发一句话给 worker。

### 核心模型

#### CEOProject

```json
{
  "project_id": "wealth_office_2026_001",
  "goal": "回测100条A股ETF策略",
  "constraints": {},
  "deliverables": [],
  "stages": [],
  "status": "planning|running|qc|done|failed"
}
```

#### CEOTask

```json
{
  "task_id": "S3_DATA_001",
  "stage": "S3",
  "role": "Coder",
  "assignee": "claude-code",
  "input": {},
  "expected_output": {},
  "acceptance_criteria": [],
  "dependencies": [],
  "status": "todo|running|blocked|done|qc_failed"
}
```

#### Artifact

```json
{
  "artifact_id": "backtest_result_001",
  "type": "code|data|result|report|log|decision",
  "path": "...",
  "source_task_id": "S4_BACKTEST_001",
  "checksum": "...",
  "schema": "...",
  "created_by": "Coder"
}
```

### Issue 标准模板

```markdown
# Role
你是：Coder / 投研 / 投顾 / 质检 / 秘书

# Context
项目目标：
当前阶段：
上游产物：
已知约束：

# Task
你要完成什么：

# Input
输入文件 / 数据 / 策略编号：

# Output Contract
必须输出：
1. 结构化 JSON
2. 人类可读摘要
3. 产物路径
4. 风险/不确定点

# Acceptance Criteria
验收标准：

# Forbidden
禁止事项：
- 不得修改已通过质检的数字
- 不得编造数据
- 不得跳过无法完成的原因说明
```

### 阶段 2 产出

```text
ceo_project.schema.json
ceo_task.schema.json
artifact.schema.json
issue_templates/
  base.md
  coder.md
  researcher.md
  advisor.md
  qc.md
  secretary.md
  pm.md
```

### 验收标准

同类任务输出结构稳定；worker 不合规时，CEO 能要求按 schema 重交。

---

## 阶段 3：角色 Prompt 与 Worker 协作协议

### 目标

让 AI 员工职责清楚，不要全员变 CEO。

### CEO

职责：

```text
目标澄清
任务拆解
依赖管理
验收标准
异常判断
返工路径选择
最终汇总
```

禁止：

```text
自己假装完成 worker 工作
盲信 worker 输出
跳过质检
```

### Coder / 数据工程

职责：

```text
读策略代码
迁移聚宽 API
写 backtrader 策略
跑批量回测
输出日志和结果
```

输出必须包含：

```text
代码路径
运行命令
数据范围
参数配置
结果文件
失败策略及原因
```

### 投研

职责：

```text
策略逻辑
收益来源
失效条件
因子解释
优化方向
```

禁止：凭空编造回测数据。

### 投顾

职责：

```text
收益风险分析
最大回撤
夏普
交易次数
配置价值
真实投资风险
```

必须强调：不构成投资建议，历史回测不代表未来。

### 质检

职责：

```text
编号一致性
数据源一致性
时间段一致性
图表数字一致性
指标复算
证据链检查
返工路径判断
```

输出：

```json
{
  "verdict": "PASS|FAIL",
  "failed_stage": "S3|S4|S6|S7_INTERNAL",
  "issues": [],
  "required_rework": []
}
```

### 秘书

职责：

```text
HTML/PPT/Word/Markdown
图表
摘要
排版
```

禁止：修改数字、编造结论、隐藏风险。

### 阶段 3 产出

```text
roles/
  ceo.md
  coder.md
  researcher.md
  advisor.md
  qc.md
  secretary.md
  pm.md
```

### 验收标准

同一份回测结果交给投研/投顾/质检/秘书，输出职责必须明显不同。

---

## 阶段 4：最小量化任务闭环

### 目标

先跑 3 条策略，不要一开始跑 100 条。

### MVP 定义

```text
3 条策略
1 个数据源
1 个回测框架
1 份 HTML 报告
1 次质检
```

任务示例：

```text
选 3 条简单 ETF 轮动/均线/动量策略，
用本地免费数据跑 backtrader 回测，
输出排名、收益曲线、最大回撤、夏普、交易次数，
由投研/投顾评审，
质检通过后生成 HTML 报告。
```

### 项目目录

```text
wealth_office/projects/demo_001/
  project.json
  tasks/
  issues/
  artifacts/
  data/
  strategies/
  backtests/
  reviews/
  qc/
  reports/
```

### 最小数据

```text
交易日历
ETF 日线行情
指数日线行情
复权价格
```

### 最小指标

```text
总收益
年化收益
最大回撤
夏普
波动率
交易次数
收益曲线
回撤曲线
```

### S1-S8 流程

```text
S1 坤哥给目标
S2 CEO 拆成 5-8 个 issue
S3 Coder 准备数据
S4 Coder 写/迁移 3 个策略并回测
S5 投研/投顾分别评审
S6 可选做 1 轮简单优化
S7 质检复算 + 秘书出 HTML
S8 CEO 汇总决策包
```

### 阶段 4 产出

```text
projects/demo_001/final_decision_pack.md
projects/demo_001/reports/index.html
projects/demo_001/qc/qc_report.json
projects/demo_001/backtests/results.csv
```

### 验收标准

CEO 能回答：

```text
哪个策略最好？
为什么？
风险是什么？
结果可信吗？
下一步该做什么？
```

---

