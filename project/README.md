<p align="center">
  <img alt="Agentic RAG for Dummies Logo" src="../assets/logo.png" width="320px">
</p>

<h1 align="center">Agentic RAG for Dummies</h1>

<p align="center">
  基于 <strong>LangGraph + Qdrant + Gradio</strong> 的模块化 Agentic RAG 应用，
  支持文档管理、父子分块混合检索、多轮对话记忆、查询澄清与流式回答。
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white">
  <img alt="LangGraph" src="https://img.shields.io/badge/LangGraph-1.2%2B-orange?logo=langchain&logoColor=white">
  <img alt="Qdrant" src="https://img.shields.io/badge/Vector%20DB-Qdrant-DC244C">
  <img alt="Ollama" src="https://img.shields.io/badge/LLM-Ollama-black">
</p>

<p align="center">
  <img alt="Agentic RAG Demo" src="../assets/demo.gif" width="720px">
</p>

## 项目简介

这个项目实现了一个可以实际使用的 Agentic RAG 助手。你可以在 Gradio 界面中上传 PDF 或 Markdown 文档，系统会自动完成转换、分块、向量化与索引；随后通过 LangGraph 编排的 Agent 工作流回答问题。

它不是简单的 “文档切片 + 单轮问答”，而是包含以下能力：

- **父子分块检索**：用较小的 child chunk 提高检索精度，再返回较大的 parent chunk 提供完整上下文。
- **混合检索**：结合稠密向量与 BM25 稀疏向量，提升召回质量。
- **多轮对话记忆**：总结历史上下文，改写当前问题，支持连续追问。
- **查询澄清**：遇到模糊问题时，Agent 会先向用户确认或要求补充信息。
- **子问题拆解**：复杂问题会被拆成多个子查询，分别检索和回答后聚合。
- **自我修正与回退**：检索结果不足时自动补充查询；仍然失败时生成兜底回答。
- **上下文压缩**：长检索循环中控制上下文长度，避免 token 过快膨胀。
- **本地化运行**：默认使用本地 Ollama 模型和本地 Qdrant 数据目录。

## 工作流程

```text
上传文档
    │
    ▼
PDF / Markdown 转换
    │
    ▼
按 Markdown 标题生成 Parent Chunk
    │
    ▼
生成 Child Chunk 并写入 Qdrant
    │
    ▼
用户提问
    │
    ▼
历史总结 → 问题改写 → 查询澄清
    │
    ▼
Agent 检索 / 迭代推理 / 上下文压缩
    │
    ▼
聚合答案 → 流式输出到 Gradio
```

## 核心特性

| 特性 | 说明 |
|---|---|
| 文档管理 | 上传 PDF / Markdown，自动转换、分块、索引，并可清空和刷新知识库 |
| 层级索引 | Parent chunk 保存完整语义上下文，child chunk 用于高精度检索 |
| 混合搜索 | 使用 FastEmbed 稠密向量和 Qdrant BM25 稀疏向量 |
| Agent 编排 | LangGraph 管理检索、工具调用、压缩、聚合与兜底流程 |
| 对话记忆 | 保留并压缩近期上下文，支持跨轮次追问 |
| 可观测性 | 可选接入 Langfuse，跟踪 LLM 调用、工具使用和图执行过程 |
| Gradio UI | 提供文档管理和对话两个标签页，回答支持流式展示 |

## 项目结构

```text
project/
├── app.py                         # Gradio 应用入口
├── config.py                      # 模型、检索、分块和日志配置
├── document_chunker.py            # 父子分块逻辑
├── core/
│   ├── rag_system.py              # 初始化数据库、模型、工具和 Agent 图
│   ├── document_manager.py        # 文档上传、转换、索引和清理
│   ├── chat_interface.py          # 聊天流程与流式输出
│   └── observability.py           # Langfuse 可观测性
├── db/
│   ├── vector_db_manager.py       # 本地 Qdrant 管理器
│   └── parent_store_manager.py    # 父块持久化存储
├── rag_agent/
│   ├── graph.py                   # LangGraph 图构建
│   ├── nodes.py                   # 节点实现
│   ├── edges.py                   # 条件路由
│   ├── tools.py                   # 检索工具
│   ├── prompts.py                 # Agent Prompt
│   └── schemas.py                 # 结构化输出模型
├── ui/
│   └── gradio_app.py              # Gradio 界面
├── .env.example                   # 环境变量示例
└── Dockerfile                     # 本地容器部署
```

## 快速开始

### 1. 准备环境

请确认已安装：

- Python **3.11+**
- [Ollama](https://ollama.com/)
- Git

克隆仓库：

```bash
git clone https://github.com/GiovanniPasq/agentic-rag-for-dummies.git
cd agentic-rag-for-dummies
```

### 2. 准备 Ollama 模型

默认聊天模型是 `llama3.1:8b`。如果本机还没有任何 Ollama 模型，Windows 启动脚本会尝试自动下载该模型：

```bash
ollama pull llama3.1:8b
```

启动 Ollama 服务：

```bash
ollama serve
```

macOS 和 Windows 桌面版 Ollama 通常会自动运行服务。Linux 用户可能需要手动执行 `ollama serve`。

### 3. 安装依赖并启动

#### Windows

双击运行：

```powershell
.\start.bat
```

脚本会创建 `.venv`、安装依赖，并执行 `project/app.py`。如果启动失败，窗口会保留错误信息并等待按键，便于查看具体原因。

#### Linux / macOS

```bash
chmod +x start.sh
./start.sh
```

如果系统安装了 `uv`，脚本会优先使用 `uv run project/app.py`；否则会回退到标准 Python 虚拟环境。

### 4. 访问界面

启动后打开：

```text
http://127.0.0.1:7860
```

1. 在 **文档管理** 标签页上传 PDF 或 Markdown 文件。
2. 点击 **添加文档**，等待转换和索引完成。
3. 切换到 **对话** 标签页提问。

## Docker 部署

在仓库根目录执行：

```bash
docker build -f project/Dockerfile -t agentic-rag-for-dummies .
docker run --rm -p 7860:7860 agentic-rag-for-dummies
```

容器内部会启动 Ollama，并尝试拉取 `llama3.1:8b` 模型。如果模型下载较慢，可以提前在宿主机完成下载，或按需修改 `project/config.py` 与容器启动脚本。

## 配置说明

主要配置集中在 `project/config.py`。

### 模型

```python
DENSE_MODEL = "Qwen/Qwen3-Embedding-0.6B"
SPARSE_MODEL = "Qdrant/bm25"
LLM_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")
JUDGE_MODEL = "ministral-3:3b-instruct-2512-q8_0"
LLM_TEMPERATURE = 0
LLM_SEED = 42
```

可以通过 `project/.env` 或系统环境变量覆盖聊天模型：

```env
OLLAMA_MODEL=llama3.1:8b
```

如果请求的模型未安装，应用会自动选择本机已安装的候选模型或第一个可用模型。

### 检索

```python
RETRIEVAL_SCORE_THRESHOLD = 0.4
DEFAULT_RETRIEVAL_K = 7
```

- `RETRIEVAL_SCORE_THRESHOLD` 越低，召回越多但噪声也可能增加。
- `DEFAULT_RETRIEVAL_K` 控制每轮检索返回的 child chunk 数量。

### 分块

```python
CHILD_CHUNK_SIZE = 500
CHILD_CHUNK_OVERLAP = 100
MIN_PARENT_SIZE = 2000
MAX_PARENT_SIZE = 4000
```

系统按 Markdown 标题组织 parent chunk，然后在 parent chunk 内生成较小的 child chunk。

### 数据目录

```python
MARKDOWN_DIR = "markdown_docs"
PARENT_STORE_PATH = "parent_store"
QDRANT_DB_PATH = "qdrant_db"
```

这些目录会保存在仓库根目录下。清空文档时会同时清理转换后的 Markdown、parent store 和 Qdrant collection。

## Langfuse 可观测性

如需启用 Langfuse，先复制环境变量示例：

```bash
cp project/.env.example project/.env
```

然后修改：

```env
LANGFUSE_ENABLED=true
LANGFUSE_PUBLIC_KEY=pk-lf-...
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_BASE_URL=http://localhost:3000
```

重启应用后，LLM 调用、工具调用和图执行链路即可写入 Langfuse。

## 常见问题

### Ollama 连接失败

确认服务正在运行：

```bash
curl http://localhost:11434
```

如果无法访问，启动或重启 Ollama。

### 模型不存在

运行：

```bash
ollama list
```

确认默认模型或 `OLLAMA_MODEL` 中配置的模型已存在。如未安装：

```bash
ollama pull llama3.1:8b
```

### 第一次提问很慢

首次运行时可能需要下载 embedding 模型，并初始化本地向量库。文档较多时，建议等待索引完成后再开始提问。

### 文档重复上传没有生效

系统按文件名去重。如果同名 Markdown 已经存在于 `markdown_docs/`，会被跳过。如需重建索引，请点击 **清空全部** 后重新上传。

## 路线图

- [ ] 支持更多文档格式
- [ ] 提供多用户会话隔离
- [ ] 增加持久化对话历史
- [ ] 提供检索质量评估脚本
- [ ] 支持更多 LLM 提供商配置

## 贡献

欢迎提交 Issue 和 Pull Request。修改代码前请先讨论设计；提交 PR 时请说明：

1. 解决的问题
2. 主要改动点
3. 测试方式

## 许可证

本项目基于 [MIT License](../LICENSE) 发布。
