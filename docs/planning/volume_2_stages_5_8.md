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

