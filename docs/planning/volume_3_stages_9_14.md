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
投研/投顾可以并行
报告必须等质检后生成
优化实验可以按候选策略并行
```

### 冲突裁决原则

```text
质检 > 数据证据 > Coder可实现性 > 投顾风险 > 投研想法
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
