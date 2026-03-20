# 🚀 创业加速器 AI 评估系统

基于 **NocoBase + Dify + Python** 构建的创业项目智能评估系统，实现从数据录入到 AI 评估报告生成的全自动化流程。

---

## 📖 项目简介

本项目是"创业加速器"平台的核心评估模块，面向创业者，通过大数据和人工智能技术：

- **降低创业风险和难度**
- **提高创业成功率**
- **帮助创业者避坑、少走弯路**

**核心功能**：创业者录入项目信息 → AI 自动分析 → 生成专业评估报告（政策匹配、风险评估、独角兽潜力分析、对标企业推荐）

---
## 📸 效果展示

NocoBase 项目录入表单
![nocobase-project](https://github.com/user-attachments/assets/c9e7d14c-3064-4dd9-bc23-b0eaa3991a6a)


Dify Workflow 工作流
![dify-workflow](https://github.com/user-attachments/assets/321cff39-d27e-4376-b2ee-8b5561726023)


脚本运行效果
![script-running](https://github.com/user-attachments/assets/81dbbbe3-3991-43d7-8d75-42d0098c3794)


AI 评估报告
![nocobase-report-list](https://github.com/user-attachments/assets/1abc08ac-176b-4be6-b72d-faaeaa8921aa)


---

## 🏗️ 技术架构

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ NocoBase │────▶│ Python 脚本 │────▶│ Dify AI │
│ 零代码数据后端 │ │ 集成桥接层 │ │ 智能评估引擎 │
│ │ │ │ │ │
│ • 可视化表单录入 │ │ • 自动检测新项目 │ │ • Workflow 工作流 │
│ • 数据表管理 │ │ • 调用 Dify API │ │ • 3个LLM节点串联 │
│ • REST API 服务 │ │ • 报告回写NocoBase │ │ • 流式响应 │
└──────────────────┘ └──────────────────┘ └──────────────────┘
▲ │
│ │
└────────────────────────────────────────────────┘
评估报告自动回写

---

## 🔧 技术栈

| 组件 | 版本 | 用途 |
|------|------|------|
| [NocoBase](https://www.nocobase.com/) | Latest | 零代码数据后端，数据表管理、可视化表单搭建、REST API |
| [Dify](https://dify.ai/) | Cloud | AI 工作流引擎，LLM 编排、Workflow 设计、API 服务 |
| Python | 3.8+ | 集成桥接脚本，打通 NocoBase 与 Dify 数据流 |
| Docker | Latest | NocoBase 容器化部署 |
| 智谱 AI (GLM-4) | - | 大语言模型，提供 AI 分析能力 |

---

## 📊 数据流说明
步骤1：创业者在 NocoBase 可视化表单中录入项目信息
│
▼
步骤2：Python 脚本轮询检测到新的「待评估」项目
│
▼
步骤3：脚本提取项目信息，更新状态为「评估中」
│
▼
步骤4：脚本调用 Dify Workflow API（流式模式）
│
├── LLM 节点1：项目基本面分析
│ （市场规模、增长趋势、竞争格局、技术壁垒）
│
├── LLM 节点2：政策匹配 + 风险评估
│ （国家政策匹配、独角兽潜力评分、五维风险评估）
│
└── LLM 节点3：生成综合评估报告
（结构化报告、对标企业、改进建议）
│
▼
步骤5：脚本将 AI 生成的报告写回 NocoBase 评估报告表
│
▼
步骤6：更新项目状态为「已完成」，用户可在 NocoBase 中查看报告


---

## 📦 项目结构

startup-accelerator/
├── README.md # 项目说明文档
├── LICENSE # 开源协议
├── .gitignore # Git 忽略文件
├── scripts/
│ ├── nocobase_dify_bridge.py # 核心集成脚本（NocoBase ↔ Dify）
│ ├── get_token.py # NocoBase Token 获取工具
│ └── requirements.txt # Python 依赖
├── docs/
│ ├── architecture.md # 架构设计说明
│ └── setup-guide.md # 详细部署指南
└── screenshots/ # 效果截图
├── nocobase-project-form.png # NocoBase 项目录入表单
├── nocobase-report-list.png # NocoBase 评估报告列表
├── dify-workflow.png # Dify Workflow 工作流全貌
└── script-running.png # 脚本运行效果

---

## 🔑 核心特性

-零代码数据管理：基于 NocoBase 搭建，无需编写前后端代码
-AI 智能评估：基于 Dify Workflow 编排多个 LLM 节点，多维度深度分析
-自动化流程：Python 脚本自动检测新项目、调用 AI、回写报告，全程无需人工干预
-数据流贯通：NocoBase ↔ Python ↔ Dify 三者数据联通，不断裂、不孤立
-流式响应：采用 streaming 模式调用 Dify API，避免大模型长时间处理导致超时


## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。


## 📞 支持与反馈

如有问题或建议，可在GitHub Discussions中讨论

---
