# AI 智能问答系统 - 前端界面

这是一个基于RAG（检索增强生成）的AI智能问答系统的前端界面，专门用于中药学知识问答。

## 功能特性

- 🤖 **智能问答**: 基于RAG技术，提供准确的中药学知识问答
- 💬 **多轮对话**: 支持上下文相关的连续对话
- 📁 **文件上传**: 支持上传PDF、TXT、MD等格式的文档
- 📚 **历史记录**: 自动保存和管理对话历史
- 🎨 **现代化UI**: 美观的聊天界面设计
- 📱 **响应式设计**: 支持桌面和移动设备

## 安装和运行

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python app.py
```

### 3. 访问系统

打开浏览器访问: http://localhost:5000

## 使用说明

### 基本操作

1. **开始新会话**: 点击侧边栏的"新会话"按钮
2. **发送消息**: 在输入框中输入问题，按Enter或点击发送按钮
3. **查看历史**: 点击侧边栏的历史会话记录
4. **上传文件**: 点击"上传文件"按钮选择要上传的文档

### 支持的文件格式

- `.txt` - 文本文件
- `.pdf` - PDF文档
- `.md` - Markdown文件
- `.doc` - Word文档
- `.docx` - Word文档

### 快捷键

- `Enter` - 发送消息
- `Shift + Enter` - 换行

## 技术架构

### 前端技术栈

- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **JavaScript (ES6+)** - 交互逻辑
- **Font Awesome** - 图标库

### 后端技术栈

- **Flask** - Web框架
- **Flask-CORS** - 跨域支持
- **RAG系统** - 检索增强生成

### 核心功能模块

1. **聊天界面** (`script.js`)
   - 消息发送和接收
   - 实时对话显示
   - 自动滚动

2. **文件管理** (`script.js`)
   - 文件上传处理
   - 文件类型验证
   - 文件删除功能

3. **会话管理** (`script.js`)
   - 历史记录保存
   - 会话切换
   - 本地存储

4. **后端API** (`app.py`)
   - 聊天接口
   - 文件处理
   - RAG系统集成

## 文件结构

```
frontend/
├── index.html          # 主页面
├── styles.css          # 样式文件
├── script.js           # 前端逻辑
├── app.py              # 后端服务
├── requirements.txt    # 依赖管理
└── README.md          # 说明文档
```

## API接口

### POST /api/chat
发送聊天消息

**请求参数:**
- `message` (string): 用户消息
- `files` (file[]): 上传的文件（可选）

**响应:**
```json
{
  "answer": "AI回复内容",
  "context": "检索到的上下文",
  "timestamp": "2024-01-01T12:00:00"
}
```

### GET /api/sessions
获取所有会话

### GET /api/sessions/<session_id>
获取特定会话

### DELETE /api/sessions/<session_id>
删除会话

### POST /api/clear-history
清空聊天历史

### GET /api/health
健康检查

## 自定义配置

### 修改端口
在 `app.py` 中修改端口号：
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

### 修改文件大小限制
在 `script.js` 中修改文件大小限制：
```javascript
if (file.size > 10 * 1024 * 1024) {  // 10MB
    alert(`文件 ${file.name} 太大，请选择小于10MB的文件。`);
    return;
}
```

## 故障排除

### 常见问题

1. **端口被占用**
   - 修改 `app.py` 中的端口号
   - 或者关闭占用端口的程序

2. **文件上传失败**
   - 检查文件大小是否超过限制
   - 确认文件格式是否支持

3. **RAG系统连接失败**
   - 确认RAG系统已正确初始化
   - 检查环境变量配置

### 日志查看

启动时会在控制台显示详细的日志信息，包括：
- 系统启动状态
- 文件处理过程
- 错误信息

## 开发说明

### 添加新功能

1. 在前端 `script.js` 中添加交互逻辑
2. 在 `styles.css` 中添加样式
3. 在后端 `app.py` 中添加API接口

### 样式定制

主要样式变量在 `styles.css` 中定义：
- 主色调: `#667eea` 和 `#764ba2`
- 字体: `'Segoe UI', Tahoma, Geneva, Verdana, sans-serif`
- 圆角: `8px` 和 `25px`

## 许可证

本项目仅供学习和研究使用。