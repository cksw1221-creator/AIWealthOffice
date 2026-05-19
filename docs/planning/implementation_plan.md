# Multica + GenericAgent AI 财富办公室：详细实现路径

> 目标：实现一个有组织结构、有责任链、有质检、有复盘、有资产沉淀的 AI 财富办公室。
> GenericAgent=AI CEO；Multica=协作/执行层；AI workers=PM/Coder/投资分析师/秘书等员工。

---

## 0. 总体路线

不要一开始做大而全平台。正确路线：

```text
先跑通 Multica 最小闭环
→ 创建几个 Coder worker
→ 让代码相关工作优先通过 Multica 分派给 Coder
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
你是：Coder / 投资分析师 / 秘书 / PM

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
  investment_analyst.md
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

### Coder / 代码工程师

职责：

```text
负责所有代码相关工作
通过 Multica 接收和执行代码任务
读策略代码
迁移聚宽 API
编写与维护 backtrader 策略/回测脚本
编写数据接入与清洗脚本
编写自动化脚本、批处理与工具链
跑批量回测
实现优化实验
调试修复与重构
输出日志、产物与结果
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

### 投资分析师

职责：

```text
合并投研与投顾职责
分析策略逻辑
解释收益来源
判断失效条件与过拟合风险
评估收益、回撤、夏普、交易次数与配置价值
提出优化方向与继续研究建议
```

禁止：凭空编造回测数据；必须强调不构成投资建议，历史回测不代表未来。

### 秘书

职责：

```text
合并质检与秘书职责
检查编号一致性
检查数据源、时间段、复权口径
复算关键指标与核查证据链
生成 HTML/PPT/Word/Markdown
图表、摘要、排版
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

禁止：修改数字、编造结论、隐藏风险。

### 阶段 3 产出

```text
roles/
  ceo.md
  coder.md
  investment_analyst.md
  secretary.md
  pm.md
```

### 验收标准

同一份回测结果交给投资分析师与秘书，输出职责必须明显不同：投资分析师负责逻辑、收益风险和优化建议；秘书负责核查、返工路由和报告表达。

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
由投资分析师评审，
必要的代码实现、脚手架补齐、自动化和调试工作通过 Multica 分派给 Coder，
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
S5 投资分析师评审
S6 可选做 1 轮简单优化
S7 秘书复算/核查 + 出 HTML
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

# 第 2 卷：阶段 5-8，让系统可信、可复用、可运转

## 阶段 5：质检与返工系统

### 目标

把“AI 会错”当成系统设计前提。不是出错后人工骂它，而是流程自动识别、自动回流。

### 模块结构

```text
qc/
  checks/
    strategy_id_consistency.py
    data_range_check.py
    metric_recompute.py
    report_number_trace.py
    artifact_existence.py
    overfit_warning.py
  qc_runner.py
  qc_schema.json
```

### 检查项

#### 策略编号一致性

检查：

```text
strategy_id
strategy_name
source_file
backtest_result
report_table
chart_data
```

#### 数据范围一致性

检查：

```text
start_date
end_date
symbol universe
adjustment
frequency
```

#### 指标复算

至少复算：

```text
total_return
max_drawdown
sharpe
trade_count
```

#### 报告数字溯源

检查：

```text
report.html
→ chart_data.json
→ results.csv
→ backtest_log
→ strategy_code + data
```

### 返工路由器

```python
if data_error:
    return "S3"
elif migration_or_backtest_error:
    return "S4"
elif optimization_result_error:
    return "S6"
elif report_only_error:
    return "S7_INTERNAL"
else:
    return "PASS"
```

### 质检报告格式

```json
{
  "verdict": "FAIL",
  "failed_stage": "S4",
  "issues": [
    {
      "type": "strategy_id_mismatch",
      "detail": "策略 #26 的报告结果对应 #29",
      "evidence": []
    }
  ],
  "required_rework": [
    {
      "target_stage": "S4",
      "task": "重新绑定 strategy_id 与 backtest_result"
    }
  ]
}
```

### 验收标准

故意制造错误：

```text
策略编号错
报告数字错
数据时间段错
```

系统能判断回到：

```text
S3 / S4 / S6 / S7_INTERNAL
```

---

## 阶段 6：报告与决策包系统

### 目标

不是生成漂亮报告，而是生成可决策报告。

### 报告结构

```text
1. CEO 摘要
2. 本轮任务目标
3. 数据和方法
4. 策略池说明
5. 排名总表
6. Top 策略卡片
7. 收益曲线
8. 回撤分析
9. 投研观点
10. 投顾观点
11. 质检结论
12. 风险和不确定点
13. 下一步建议
14. 附录：代码/数据/日志/参数
```

### 决策包结构

```markdown
# CEO决策包

## 1. 结论先行
本轮最值得继续研究的是：

## 2. 证据
- 回测指标
- 投研解释
- 投顾评估
- 质检结果

## 3. 风险
- 数据风险
- 过拟合风险
- 市场环境风险
- 实盘摩擦风险

## 4. 建议动作
A. 继续优化
B. 推回聚宽验证
C. 扩展数据Skill
D. 放弃某些策略

## 5. 需要CEO拍板的问题
```

### 产出

```text
report_generator.py
templates/
  html_report.html.j2
  decision_pack.md.j2
  ppt_outline.md.j2
```

### 验收标准

CEO无需看日志即可知道：

```text
结论是什么
证据是什么
风险是什么
不确定点是什么
下一步该拍板什么
```

---

## 阶段 7：沉淀资产与工作流产品化

### 目标

每次项目结束都沉淀可复用资产，而不是留下零散文件。

### 沉淀资产

```text
1. 角色 Prompt
2. Issue 模板
3. 数据 Skill
4. 回测 Schema
5. 策略迁移规则
6. 质检规则
7. 报告模板
8. 返工路由规则
9. Worker 能力矩阵
10. 常见失败案例库
```

### 复盘文件

每次项目结束生成：

```text
retrospective.md
```

内容：

```text
哪些 worker 表现好
哪些任务容易失败
哪些 Prompt 需要改
哪些数据缺口影响最大
哪些检查救了命
哪些流程可以自动化
下一轮应该改什么
```

### 产出

```text
workflow_registry.json
role_prompt_versions.json
worker_scorecard.json
failure_casebook.md
```

### 验收标准

下一次项目能直接复用上一次的模板、Prompt、QC 规则和数据 Skill。

---

## 阶段 8：完整 AI 财富办公室

### 目标

从“能跑一次”升级为“可持续运转”。

### 能力方向

#### 策略工厂

```text
自动收集策略
自动分类策略
自动迁移策略
自动回测策略
自动排名
自动淘汰
自动推荐下一轮
```

#### 数据工厂

```text
行情数据
ETF 数据
指数数据
财务数据
估值数据
因子数据
新闻情绪
资金流
宏观数据
```

#### 聚宽双向验证

```text
本地免费数据初筛
→ 推回聚宽自动回测
→ 对比差异
→ 判断本地回测可信度
```

#### 组合层

```text
单策略评估
→ 策略组合
→ 低相关组合
→ 风险预算
→ 再平衡
```

#### 持续监控

```text
每日更新数据
每周跑回测
每月出报告
策略失效预警
市场环境切换预警
```

### 验收标准

用户输入：

```text
帮我筛 100 条 A股量化策略，找出低回撤、高夏普、适合继续研究的前 10 条。
```

系统能自动：

```text
澄清目标→创建项目→拆任务→分派worker→准备数据→迁移策略→批量回测→多角色评审→优化实验→质检→生成报告→汇总决策包→沉淀模板
```

---

# 第 3 卷：阶段 9-14，让系统资产化、治理化、产品化

## 阶段 9：数据资产与策略资产库

### 目标

从一次性项目升级为长期投资研究资产。

### 数据资产库

沉淀：

```text
行情数据
ETF 数据
指数数据
行业数据
估值数据
财务数据
因子数据
交易日历
复权数据
宏观数据
新闻/情绪数据
资金流数据
```

数据 metadata：

```json
{
  "dataset_id": "cn_etf_daily_akshare",
  "provider": "akshare",
  "symbols": ["510300", "159915"],
  "start_date": "2019-01-01",
  "end_date": "2026-05-18",
  "frequency": "1d",
  "adjustment": "qfq",
  "last_updated": "...",
  "missing_rate": 0.002,
  "known_issues": ["部分ETF上市前为空"],
  "validated_by": "qc"
}
```

### 策略资产库

每条策略登记：

```json
{
  "strategy_id": "JQ_026",
  "name": "波动率过滤",
  "source": "joinquant",
  "type": "ETF rotation",
  "status": "migrated|failed|pending|deprecated",
  "data_dependencies": ["etf_daily", "index_daily"],
  "jq_api_dependencies": ["get_price", "attribute_history"],
  "local_impl_path": "...",
  "backtest_result_ids": [],
  "known_risks": [],
  "last_review": "..."
}
```

状态：

```text
待分析
可迁移
部分可迁移
不可迁移
已回测
已优化
已放弃
待聚宽验证
```

### 研究结论库

保存：

```text
策略为什么有效
在哪些市场环境有效
为什么可能失效
适合什么组合位置
下次该怎么优化
```

---

## 阶段 10：多 Agent 运营治理

### 目标

防止多 Agent 变成多个人一起胡说、重复劳动、互相甩锅。

### Worker 能力矩阵

```json
{
  "worker": "claude-code",
  "best_for": ["code_migration", "debugging"],
  "weak_for": ["long_running_browser_task"],
  "success_rate": 0.82,
  "format_compliance_rate": 0.76,
  "avg_completion_time": 1800,
  "stuck_count": 3,
  "last_failure_reason": "ignored output schema"
}
```

### 绩效指标

```text
是否按时完成
是否按格式输出
是否编造数据
是否需要返工
是否造成严重错误
```

### 调度策略

```text
数据准备必须先于回测
投资分析师分析可以并行
报告必须等秘书核查后生成
优化实验可以按候选策略并行
```

### 冲突裁决原则

```text
秘书核查 > 数据证据 > Coder可实现性 > 投资分析师建议
```

质检 FAIL 时，任何漂亮结论都不能进入决策包。

---

## 阶段 11：安全、合规与风控边界

### 目标

财富办公室必须从一开始设边界。

### 投资建议边界

所有报告标注：

```text
本文仅用于研究，不构成投资建议。
历史回测不代表未来收益。
策略实盘表现可能受交易成本、滑点、流动性、市场环境影响。
```

### 自动实盘边界

早期禁止：

```text
自动下单
自动调仓
自动连接券商实盘账户
自动使用真实资金
```

未来若要做，另开阶段：

```text
纸面交易
模拟盘
小资金灰度
人工确认下单
实盘风控
```

### 数据合规

确认：

```text
数据来源是否合法
是否允许缓存
是否允许商业使用
是否允许二次分发
是否含账号密钥
```

### 密钥边界

```text
密钥文件只引用，不读取/移动
不写入报告
不进入 worker prompt
不进入日志
```

### 风控规则

```text
最大回撤阈值
单一资产集中度
交易频率
换手率
流动性
异常收益
未来函数
过拟合
样本外表现
```

---

## 阶段 12：商业化 / 产品形态演进

### 阶段形态

#### 内部工具

```text
命令行 + 文件夹 + 报告
```

#### 工作台

```text
Web Dashboard
项目列表
任务状态
worker 状态
策略库
报告库
质检结果
返工记录
```

#### AI 投研 Copilot

```text
上传策略
自动回测
自动评审
自动生成报告
```

#### AI 财富办公室 SaaS

```text
多用户
多项目
策略市场
数据插件
Agent 插件
报告模板
权限管理
计费
```

#### 私有化部署

```text
本地部署
私有数据
自有模型
自有策略库
自有合规模板
```

---

## 阶段 13：自我改进与反思系统

### 目标

让 AI 财富办公室每做完一次项目都变聪明。

### 每轮结束生成 postmortem

```text
本轮哪里慢
哪里错
哪个 worker 不靠谱
哪个 Prompt 不清楚
哪个数据缺口最大
哪个质检规则救了命
哪些流程应该自动化
```

### 自动更新

```text
Prompt 版本
Issue 模板
QC 规则
Worker 评分
失败案例库
```

### 验收标准

下一轮项目相比上一轮：

```text
少犯同类错误
少人工干预
更快出报告
质检命中率更高
```

---

## 阶段 14：从量化扩展到通用 AI 办公室

### 目标

A股量化是第一业务场景，但组织能力可以迁移。

### 可扩展业务

```text
行业研究办公室
公司财报分析办公室
竞品情报办公室
政策跟踪办公室
内容生产办公室
自动化软件开发办公室
知识库运营办公室
```

### 不变结构

```text
CEO
→ CEO
→ Multica
→ AI 员工
→ 质检
→ 报告
→ 决策
```

### 变化部分

```text
数据源
角色 Prompt
业务流程
报告模板
质检规则
```

---

# 落地优先级

## P0：马上做

```text
阶段 0：现状探测
阶段 1：MulticaClient
阶段 2：任务模型/Issue协议
阶段 3：角色Prompt
阶段 4：Demo 001
```

## P1：紧接着做

```text
阶段 5：质检返工
阶段 6：报告决策包
阶段 11：风控边界
```

## P2：形成资产

```text
阶段 7：工作流产品化
阶段 9：数据/策略资产库
阶段 10：Agent治理
阶段 13：反思系统
```

## P3：规模化

```text
阶段 8：完整办公室
阶段 12：商业化
阶段 14：通用办公室
```

---

# 立即下一步

建议马上执行：

```text
Step 1：探测当前 Multica / GA 环境
Step 2：实现 MulticaClient
Step 3：跑 Hello Worker 闭环
```

只要这三步完成，AI 财富办公室就从概念进入工程实体。
