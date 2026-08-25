# 配置说明

## 环境变量配置

在项目根目录创建 `.env` 文件，包含以下配置：

```env
# 阿里云百炼API配置
DASHSCOPE_API_KEY=your_api_key_here
DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen-turbo
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v1
DASHSCOPE_RERANK_MODEL=bge-reranker-v2-m3
```

## 获取API密钥

1. 访问 [阿里云百炼控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建API密钥
4. 将密钥填入 `.env` 文件中的 `DASHSCOPE_API_KEY`

## 依赖安装

确保安装了所有必要的依赖：

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
cd frontend
python app.py
```

然后访问 http://localhost:5000 