# 基于 LangChain 的智能问答系统

这是一个基于 LangChain 框架开发的智能问答系统，支持知识库检索、网页爬取、多轮对话等功能。系统使用向量数据库存储文档，支持实时网页爬取并基于内容进行问答。

## 项目结构

```
RAG/
├── main.py                 # 主程序入口
├── test_rag.py            # RAG 系统测试文件
├── requirements.txt        # 项目依赖
├── documents/             # 知识库文档目录
├── data_base/            # 向量数据库存储目录
├── files/                # 中药学文档目录
├── frontend/             # 前端Web应用
│   ├── app.py            # Flask后端服务
│   ├── index.html        # 主页面
│   ├── knowledge.html    # 知识库管理页面
│   ├── script.js         # 前端JavaScript
│   ├── styles.css        # 样式文件
│   ├── requirements.txt  # 前端依赖
│   └── start.bat         # Windows启动脚本
└── utils/                # 工具类目录
    ├── retrieval_qa.py       # 检索问答核心实现
    ├── knowledgebase.py      # 知识库管理
    ├── web_crawler.py        # 网页爬虫
    ├── document_processor.py # 文档处理
    ├── qw_embedding.py       # 通义千问 Embedding
    ├── prompts.py           # 提示词模板
    ├── tool.py              # 通用工具函数
    └── chat_history_manager.py # 对话历史管理
```

## 主要功能

1. **知识库问答**：基于向量数据库的文档检索和问答
2. **网页爬取问答**：支持实时爬取网页内容并基于内容进行问答
3. **多轮对话**：支持上下文理解的多轮对话
4. **文档处理**：支持多种格式文档的处理和入库
5. **Web界面**：提供友好的Web界面进行交互
6. **文件上传**：支持通过Web界面上传文档到知识库

## 环境配置

1. 安装依赖：
```bash
# 安装主项目依赖
pip install -r requirements.txt

# 安装前端依赖
cd frontend
pip install -r requirements.txt
```

2. 配置环境变量：
创建 `.env` 文件，添加以下配置：
```
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_API_BASE=your_api_base
DASHSCOPE_MODEL=your_model_name
DASHSCOPE_EMBEDDING_MODEL=your_embedding_model
DASHSCOPE_RERANK_MODEL=your_rerank_model
```

## 使用方法

### 1. 启动Web应用

```bash
cd frontend
python app.py
```

然后在浏览器中访问 `http://localhost:5000`

### 2. 使用Python API

```python
from utils.retrieval_qa import RetrievalQA
qa = RetrievalQA()

# 简单问答
response = qa.invoke("你的问题")

# 带历史记录的对话
chat_history = [("human", "上一个问题"), ("ai", "上一个回答")]
response = qa.invoke("新的问题", chat_history=chat_history)
```

### 3. 网页爬取问答

系统会通过正则表达式自动检测问题中的 URL，进行爬取和问答：
```python
response = qa.invoke("这个网页说了什么 https://example.com")
```

## Web界面功能

1. **聊天界面**：支持与AI进行实时对话
2. **文件上传**：支持上传PDF、TXT、MD等格式的文档
3. **知识库管理**：查看和管理已上传的文档
4. **历史记录**：保存和查看对话历史

## 注意事项

1. 确保已正确配置 API 密钥和模型参数
2. 文档入库前会自动进行分块处理
3. 网页爬取功能需要目标网站允许爬取
4. 向量数据库文件会保存在 data_base 目录下
5. 首次运行时会自动创建必要的目录结构

## 基础测试

运行测试脚本：
```bash
python test_rag.py
```

## 开发说明

- `utils/retrieval_qa.py`: 实现了检索增强生成（RAG）的核心逻辑
- `utils/knowledgebase.py`: 管理向量数据库，实现文档的增删改查
- `utils/web_crawler.py`: 实现网页爬取和内容提取
- `utils/document_processor.py`: 处理文档分块、清洗等预处理操作
- `utils/qw_embedding.py`: 实现通义千问的 Embedding 接口
- `utils/prompts.py`: 管理系统使用的提示词模板
- `utils/tool.py`: 提供通用工具函数
- `utils/chat_history_manager.py`: 管理多轮对话的历史记录
- `frontend/app.py`: Flask后端服务，提供Web API
- `frontend/index.html`: 主聊天界面
- `frontend/knowledge.html`: 知识库管理界面

## 技术栈

- **后端**: Python, Flask, LangChain
- **前端**: HTML, CSS, JavaScript
- **数据库**: ChromaDB (向量数据库)
- **AI模型**: 通义千问 (DashScope)
- **文档处理**: PyMuPDF, Unstructured
