#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# 添加父目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)
CORS(app)

# 简单的问答系统
class SimpleQA:
    def __init__(self):
        self.name = "AI助手"
        self.description = "我是一个简单的AI助手，可以回答基本问题。"
    
    def answer(self, question):
        """简单的问答逻辑"""
        if "你好" in question or "hello" in question.lower():
            return "你好！我是AI助手，有什么可以帮助你的吗？"
        elif "介绍" in question or "你是谁" in question:
            return self.description
        elif "谢谢" in question or "感谢" in question:
            return "不客气！很高兴能帮助你。"
        else:
            return f"我收到了你的问题：'{question}'。这是一个很好的问题，但我目前只能提供基本的回答。如果你有具体的文档相关问题，可以上传文档后再次询问。"

# 初始化简单的问答系统
qa_system = SimpleQA()

@app.route('/')
def index():
    """提供前端页面"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    """提供静态文件"""
    return send_from_directory('.', filename)

@app.route('/api/chat', methods=['POST'])
def chat():
    """处理聊天请求"""
    try:
        # 获取消息内容
        message = request.form.get('message', '').strip()
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 使用简单的问答系统
        answer = qa_system.answer(message)
        
        # 返回结果
        response = {
            'answer': answer,
            'context': '',
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"聊天处理错误: {str(e)}")
        return jsonify({
            'error': '处理请求时发生错误',
            'details': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'system': 'simple_qa'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("启动简单AI聊天系统...")
    print("访问地址: http://localhost:5000")
    print("这是一个简化版本，用于测试基本功能")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except OSError as e:
        if "Address already in use" in str(e):
            print("端口5000被占用，尝试使用端口5001...")
            app.run(debug=True, host='0.0.0.0', port=5001, use_reloader=False)
        else:
            print(f"启动失败: {e}")
    except Exception as e:
        print(f"启动失败: {e}") 