# 快速启动指南

## 1. 配置环境变量

在项目根目录（RAG文件夹）创建 `.env` 文件：

```env
DASHSCOPE_API_KEY=你的阿里云百炼API密钥
DASHSCOPE_API_BASE=https://dashscope.aliyuncs.com/api/v1
DASHSCOPE_MODEL=qwen-turbo
DASHSCOPE_EMBEDDING_MODEL=text-embedding-v1
DASHSCOPE_RERANK_MODEL=bge-reranker-v2-m3
```

## 2. 获取API密钥

1. 访问 [阿里云百炼控制台](https://dashscope.console.aliyun.com/)
2. 注册/登录账号
3. 创建API密钥
4. 将密钥填入 `.env` 文件

## 3. 启动系统

### Windows用户：
双击运行 `start.bat`

### Linux/Mac用户：
```bash
chmod +x start.sh
./start.sh
```

### 手动启动：
```bash
cd frontend
pip install -r requirements.txt
python test_config.py  # 检查配置
python app.py          # 启动服务
```

## 4. 访问系统

打开浏览器访问：http://localhost:5001

## 常见问题

### Q: 提示"配置检查失败"
A: 请检查 `.env` 文件是否正确创建，API密钥是否正确配置

### Q: 提示"模块导入失败"
A: 请确保在frontend目录下运行，并且已安装所有依赖

### Q: 前端无法对话
A: 请检查控制台是否有错误信息，确保RAG系统正常初始化

### Q: 端口被占用
A: 如果5001端口被占用，可以修改app.py中的端口号 