# 架构设计说明

## 整体架构

本系统采用"零代码平台 + AI引擎 + 轻量脚本"的架构模式。

## 组件说明

### NocoBase（数据后端）
- 创业项目表：存储创业者录入的项目信息
- 评估报告表：存储AI生成的评估报告
- 行业数据表：存储对标企业和行业数据
- 提供可视化表单和REST API

### Dify（AI引擎）
- Workflow模式，3个LLM节点串联
- 节点1：基本面分析
- 节点2：政策与风险评估
- 节点3：综合报告生成
- 通过API对外提供服务

### Python桥接脚本
- 轮询NocoBase获取待评估项目
- 调用Dify API进行AI评估
- 将结果回写NocoBase
- 使用流式模式（streaming）避免超时

## 数据表设计

### startup_projects（创业项目表）
| 字段 | 类型 | 说明 |
|------|------|------|
| project_name | 单行文本 | 项目名称 |
| project_stage | 单选 | 项目阶段 |
| industry | 单选 | 行业领域 |
| target_users | 单行文本 | 目标用户 |
| application_scenario | 多行文本 | 应用场景 |
| core_technology | 多行文本 | 核心技术 |
| main_products | 单行文本 | 主营产品 |
| founder_name | 单行文本 | 联系人 |
| status | 单选 | 评估状态 |

### evaluation_reports（评估报告表）
| 字段 | 类型 | 说明 |
|------|------|------|
| ai_report | 多行文本 | AI完整报告 |
| policy_match | 多行文本 | 政策匹配 |
| risk_level | 单选 | 风险等级 |
| unicorn_score | 数字 | 独角兽潜力分 |
| benchmark_companies | 多行文本 | 对标企业 |
| generated_at | 日期 | 生成时间 |

### industry_data（行业数据表）
