# 基于 LangChain 的智能问答系统

这是一个基于 LangChain 框架开发的智能问答系统，支持知识库检索、网页爬取、多轮对话等功能。系统使用向量数据库存储文档，支持实时网页爬取并基于内容进行问答。

## 目录结构

```
demo/
├── main.py                 # 主程序入口
├── test_rag.py            # RAG 系统测试文件
├── requirements.txt        # 项目依赖
├── documents/             # 知识库文档目录
├── data_base/            # 向量数据库存储目录
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

## 环境配置

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 配置环境变量：
创建 `.env` 文件，添加以下配置：
```
DASHSCOPE_API_KEY=your_api_key
DASHSCOPE_API_BASE=your_api_base
DASHSCOPE_MODEL=your_model_name
DASHSCOPE_EMBEDDING_MODEL=your_embedding_model
# 参考模型调用方式
# https://help.aliyun.com/zh/model-studio/third-party-tools/?spm=a2c4g.11186623.help-menu-2400256.d_0_7.42ca1458if27FI&scm=20140722.H_2880895._.OR_help-T_cn~zh-V_1
# https://bailian.console.aliyun.com/?spm=5176.29597918.J_SEsSjsNv72yRuRFS2VknO.2.16a87b08Jtw4Sa&tab=api&accounttraceid=2ba25faf33524245a9663f4e9ad6bb40mgqh#/api/?type=model&url=https%3A%2F%2Fhelp.aliyun.com%2Fdocument_detail%2F2712515.html&renderType=iframe
```

## 使用方法

1. **启动问答系统**：
```python
from utils.retrieval_qa import RetrievalQA
qa = RetrievalQA()

# 简单问答
response = qa.invoke("你的问题")

# 带历史记录的对话
chat_history = [("human", "上一个问题"), ("ai", "上一个回答")]
response = qa.invoke("新的问题", chat_history=chat_history)
```

2. **网页爬取问答**：
系统会通过正则表达式自动检测问题中的 URL，进行爬取和问答：
```python
response = qa.invoke("这个网页说了什么 https://example.com")
```

## 注意事项

1. 确保已正确配置 API 密钥和模型参数
2. 文档入库前会自动进行分块处理
3. 网页爬取功能需要目标网站允许爬取
4. 向量数据库文件会保存在 data_base 目录下

## 基础测试
最最最基本的RAG系统实现（弃用）
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
