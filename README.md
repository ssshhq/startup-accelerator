# 🚀 创业加速器 AI 评估系统

> 基于 **NocoBase + Dify** 构建的创业项目智能评估系统，实现从数据录入到 AI 评估报告生成的全自动化流程。

---

## 📖 项目简介

创业者录入项目信息 → AI 自动分析 → 生成专业评估报告（政策匹配、风险评估、独角兽潜力分析、对标企业推荐）

---

## 📸 效果展示

### NocoBase 项目录入表单

![nocobase-project](https://github.com/user-attachments/assets/c9e7d14c-3064-4dd9-bc23-b0eaa3991a6a)

### Dify Workflow 工作流

![dify-workflow](https://github.com/user-attachments/assets/321cff39-d27e-4376-b2ee-8b5561726023)

### 脚本运行效果

![script-running](https://github.com/user-attachments/assets/81dbbbe3-3991-43d7-8d75-42d0098c3794)

### AI 评估报告

![nocobase-report-list](https://github.com/user-attachments/assets/1abc08ac-176b-4be6-b72d-faaeaa8921aa)

---

## 🏗️ 技术架构

```text
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│     NocoBase     │─────▶│   Python 脚本     │─────▶│     Dify AI      │
│   零代码数据后端  │      │    集成桥接层      │      │   智能评估引擎    │
│                  │      │                  │      │                  │
│ • 可视化表单录入  │      │ • 自动检测新项目   │      │ • Workflow 工作流 │
│ • 数据表管理     │      │ • 调用 Dify API   │      │ • 3个LLM节点串联  │
│ • REST API 服务  │      │ • 报告回写NocoBase │      │ • 流式响应        │
└──────────────────┘      └──────────────────┘      └──────────────────┘
         ▲                                                   │
         │                                                   │
         └───────────────────────────────────────────────────┘
                          评估报告自动回写
```

---

## 🔧 技术栈

| 组件 | 版本 | 用途 |
|:-----|:-----|:-----|
| [NocoBase](https://www.nocobase.com/) | Latest | 零代码数据后端，数据表管理、可视化表单搭建、REST API |
| [Dify](https://dify.ai/) | Cloud | AI 工作流引擎，LLM 编排、Workflow 设计、API 服务 |
| Python | 3.11+ | 集成桥接脚本，打通 NocoBase 与 Dify 数据流 |
| Docker | Latest | NocoBase 容器化部署 |
| 智谱 AI (GLM-4) | - | 大语言模型，提供 AI 分析能力 |

---

## 📊 数据流说明

```text
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
         │     （市场规模、增长趋势、竞争格局、技术壁垒）
         │
         ├── LLM 节点2：政策匹配 + 风险评估
         │     （国家政策匹配、独角兽潜力评分、五维风险评估）
         │
         └── LLM 节点3：生成综合评估报告
               （结构化报告、对标企业、改进建议）
         │
         ▼
步骤5：脚本将 AI 生成的报告写回 NocoBase 评估报告表
         │
         ▼
步骤6：更新项目状态为「已完成」，用户可在 NocoBase 中查看报告
```

---

## 📦 项目结构

```text
startup-accelerator/
│
├── README.md                           # 项目说明文档
├── LICENSE                             # 开源协议
├── .gitignore                          # Git 忽略文件
│
├── scripts/                            # 脚本目录
│   ├── nocobase_dify_bridge.py         # 核心集成脚本（NocoBase ↔ Dify）
│   ├── get_token.py                    # NocoBase Token 获取工具
│   └── requirements.txt               # Python 依赖
│
├── docs/                               # 文档目录
│   ├── architecture.md                 # 架构设计说明
│   └── setup-guide.md                  # 详细部署指南
│
└── screenshots/                        # 效果截图
    ├── nocobase-project-form.png       # NocoBase 项目录入表单
    ├── nocobase-report-list.png        # NocoBase 评估报告列表
    ├── dify-workflow.png               # Dify Workflow 工作流全貌
    └── script-running.png              # 脚本运行效果
```

---

## 🔑 核心特性

| 特性 | 说明 |
|:-----|:-----|
| 🧩 **零代码数据管理** | 基于 NocoBase 搭建，无需编写前后端代码，可视化配置数据表和表单 |
| 🤖 **AI 智能评估** | 基于 Dify Workflow 编排多个 LLM 节点，从政策、风险、市场等多维度深度分析 |
| ⚡ **自动化流程** | Python 脚本自动检测新项目、调用 AI、回写报告，全程无需人工干预 |
| 🔗 **数据流贯通** | NocoBase ↔ Python ↔ Dify 三者数据联通，不断裂、不孤立 |
| 🌊 **流式响应** | 采用 streaming 模式调用 Dify API，避免大模型长时间处理导致超时 |

---

## 📋 AI 评估报告内容

每份自动生成的评估报告包含以下模块：

| 评估模块 | 内容详情 |
|:---------|:---------|
| 📊 **行业分析** | 市场规模、增长趋势、竞争格局 |
| 📜 **政策匹配** | 支持类 ✅/❌ · 鼓励类 ✅/❌ · 限制类 ✅/❌ · 禁止类 ✅/❌ |
| 🦄 **独角兽潜力** | 千亿规模潜力 · 五年百亿营收 · 五年内上市 · 革命性创新 · 唯一第一（每项1-10分） |
| ⚠️ **风险评估** | 资金风险 · 团队风险 · 市场风险 · 技术风险 · 政策风险（高/中/低） |
| 🏢 **对标企业** | 同行业已上市 / 已融资 / 申报中企业 TOP5 |
| 💡 **综合建议** | 项目优势、不足分析、改进建议、下一步行动方案 |

---

## 🚀 快速部署

### 1️⃣ 部署 NocoBase

```bash
docker run -d \
  --name nocobase \
  -p 13000:80 \
  -e DB_DIALECT=sqlite \
  nocobase/nocobase:latest
```

访问 `http://localhost:13000`

### 2️⃣ 配置 Dify Workflow

1. 登录 [Dify Cloud](https://cloud.dify.ai)
2. 配置模型供应商（推荐 [智谱 AI](https://open.bigmodel.cn) glm-4-flash，注册即送免费额度）
3. 创建 **Workflow** 类型应用，配置 3 个 LLM 节点
4. 发布应用，获取 API Key

### 3️⃣ 运行集成脚本

```bash
cd scripts
pip install -r requirements.txt

# 配置环境变量
export NOCOBASE_TOKEN="your-nocobase-token"
export DIFY_API_KEY="your-dify-api-key"

# 运行
python nocobase_dify_bridge.py
```

Windows PowerShell：

```powershell
$env:NOCOBASE_TOKEN="your-nocobase-token"
$env:DIFY_API_KEY="your-dify-api-key"
python scripts\nocobase_dify_bridge.py
```

---

## 🔮 扩展计划

- [ ] 接入 **Spider-Flow** 爬虫，自动采集行业公开数据
- [ ] 接入 **Superset** 数据可视化报表大屏
- [ ] 接入 **MyBricks** 搭建微信小程序前端
- [ ] 构建 **RAG 知识库**，导入产业政策文件提升评估准确性
- [ ] 完整数据流闭环：小程序录入 → NocoBase → 爬虫 → Dify → Superset → 小程序展示

---

## ⚠️ 注意事项

**报告声明**：AI 生成的评估报告仅供参考，不作任何法律或投资依据

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

## 📞 支持与反馈

如有问题或建议，欢迎在 [GitHub Discussions]中交流讨论。
