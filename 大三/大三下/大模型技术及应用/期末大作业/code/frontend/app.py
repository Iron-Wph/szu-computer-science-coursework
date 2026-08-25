from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys
import json
from datetime import datetime
import tempfile
import shutil
from dotenv import load_dotenv
import time
import urllib.parse

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

# 添加父目录到路径，以便导入RAG模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.retrieval_qa import RetrievalQA
from utils.document_processor import DocumentProcessor

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化RAG系统
qa_system = RetrievalQA()

# 存储会话数据
chat_sessions = {}

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
        # 获取消息内容和会话ID
        message = request.form.get('message', '').strip()
        session_id = request.form.get('session_id')
        
        if not message:
            return jsonify({'error': '消息不能为空'}), 400
        
        # 检查是否请求流式输出
        stream = request.form.get('stream', 'false').lower() == 'true'
        
        if stream:
            # 流式输出
            def generate():
                # 首先返回思考开始标记
                yield f"data: {json.dumps({'type': 'thinking_start', 'content': 'AI正在思考中...'})}\n\n"
                
                # 调用RAG系统获取结果，传递会话ID
                result = qa_system.invoke(message, session_id=session_id)
                print(f"debug: result: {result}")
                if isinstance(result, dict):
                    answer = result.get('answer', '抱歉，我无法回答这个问题。')
                    context = result.get('context', '')
                    sources = result.get('sources', [])
                else:
                    answer = str(result)
                    context = ''
                    sources = []
                
                # 模拟流式输出答案
                words = answer.split()
                for i, word in enumerate(words):
                    # 每3个词发送一次
                    if i % 3 == 0:
                        partial_answer = ' '.join(words[:i+1])
                        yield f"data: {json.dumps({'type': 'thinking', 'content': partial_answer})}\n\n"
                        time.sleep(0.1)  # 模拟思考时间
                
                # 发送完整答案
                yield f"data: {json.dumps({'type': 'answer', 'content': answer, 'context': context, 'sources': sources})}\n\n"
                
                # 发送结束标记
                yield f"data: {json.dumps({'type': 'thinking_end'})}\n\n"
            
            return app.response_class(
                generate(),
                mimetype='text/plain',
                headers={'Cache-Control': 'no-cache', 'Connection': 'keep-alive'}
            )
        else:
            # 非流式输出（保持原有逻辑）
            result = qa_system.invoke(message, session_id=session_id)
            print(f"debug: result: {result}")
            # 返回结果
            if isinstance(result, dict):
                response = {
                    'answer': result.get('answer', '抱歉，我无法回答这个问题。'),
                    'context': result.get('context', ''),
                    'sources': result.get('sources', []),
                    'timestamp': datetime.now().isoformat()
                }
            else:
                response = {
                    'answer': str(result),
                    'context': '',
                    'sources': [],
                    'timestamp': datetime.now().isoformat()
                }
            
            return jsonify(response)
        
    except Exception as e:
        print(f"聊天处理错误: {str(e)}")
        return jsonify({
            'error': '处理请求时发生错误',
            'details': str(e)
        }), 500

def generate_thinking_steps(question, answer):
    """生成AI思考过程步骤"""
    steps = []
    
    # 步骤1：理解问题
    steps.append({
        'step': 1,
        'action': '理解问题',
        'content': f'我正在分析您的问题："{question[:50]}{"..." if len(question) > 50 else ""}"',
        'delay': 800
    })
    
    # 步骤2：检索相关知识
    steps.append({
        'step': 2,
        'action': '检索知识库',
        'content': '正在从知识库中检索相关信息...',
        'delay': 1200
    })
    
    # 步骤3：分析信息
    steps.append({
        'step': 3,
        'action': '分析信息',
        'content': '正在分析和整理检索到的信息...',
        'delay': 1000
    })
    
    # 步骤4：生成答案
    steps.append({
        'step': 4,
        'action': '生成答案',
        'content': '正在生成答案...',
        'delay': 600
    })
    
    # 步骤5：最终答案
    steps.append({
        'step': 5,
        'action': '完成',
        'content': answer,
        'delay': 0
    })
    
    return steps

@app.route('/api/sessions', methods=['GET'])
def get_sessions():
    """获取所有会话"""
    return jsonify(chat_sessions)

@app.route('/api/sessions/<session_id>', methods=['GET'])
def get_session(session_id):
    """获取特定会话"""
    if session_id in chat_sessions:
        return jsonify(chat_sessions[session_id])
    return jsonify({'error': '会话不存在'}), 404

@app.route('/api/sessions/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """删除会话"""
    if session_id in chat_sessions:
        del chat_sessions[session_id]
        return jsonify({'message': '会话已删除'})
    return jsonify({'error': '会话不存在'}), 404

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """清空聊天历史"""
    session_id = request.form.get('session_id')
    qa_system.clear_chat_history(session_id=session_id)
    return jsonify({'message': '聊天历史已清空'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'rag_system': 'initialized'
    })

@app.route('/api/documents', methods=['GET'])
def list_documents():
    """列出知识库文件"""
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documents'))
    files = []
    for fname in os.listdir(docs_dir):
        fpath = os.path.join(docs_dir, fname)
        if os.path.isfile(fpath):
            files.append(fname)
    return jsonify({'files': files})

@app.route('/api/documents/upload', methods=['POST'])
def upload_document():
    """上传文件到知识库"""
    # docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documents'))
    if 'file' not in request.files:
        return jsonify({'error': '未检测到文件'}), 400
    file = request.files['file']
    if not file.filename or str(file.filename).strip() == '':
        return jsonify({'error': '文件名不能为空'}), 400
    safe_name = os.path.basename(str(file.filename))
    save_path = os.path.join("../documents", safe_name)
    file.save(save_path)
    # 保存到知识库
    docs = qa_system.kb_manager.doc_processor.load_document(save_path)
    qa_system.kb_manager.add_documents(docs)
    # qa_system.kb_manager.check_collection()

    return jsonify({'message': '文件上传成功'})

@app.route('/api/documents/<path:filename>/download', methods=['GET'])
def download_document(filename):
    """下载文件"""
    print(f"下载文件请求: {filename}")
    docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documents'))
    safe_name = os.path.basename(str(urllib.parse.unquote(filename)))
    fpath = os.path.join(docs_dir, safe_name)
    print(f"文件路径: {fpath}")
    print(f"文件是否存在: {os.path.exists(fpath)}")
    
    if not os.path.exists(fpath) or not os.path.isfile(fpath):
        print(f"文件不存在: {fpath}")
        return jsonify({'error': '文件不存在'}), 404
    
    try:
        return send_from_directory(docs_dir, safe_name, as_attachment=True)
    except Exception as e:
        print(f"下载文件失败: {str(e)}")
        return jsonify({'error': f'下载文件失败: {str(e)}'}), 500

@app.route('/api/documents/<path:filename>', methods=['DELETE'])
def delete_document(filename):
    """删除知识库文件"""
    print(f"删除文件请求: {filename}")
    # docs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documents'))
    safe_name = os.path.basename(str(urllib.parse.unquote(filename)))
    fpath = os.path.join("../documents", safe_name)
    # print(f"文档目录: {docs_dir}")
    print(f"安全文件名: {safe_name}")
    print(f"完整文件路径: {fpath}")
    print(f"文件是否存在: {os.path.exists(fpath)}")
    print(f"是否为文件: {os.path.isfile(fpath) if os.path.exists(fpath) else 'N/A'}")
    
    if not os.path.exists(fpath):
        print(f"文件不存在: {fpath}")
        return jsonify({'error': '文件不存在'}), 404
    
    if not os.path.isfile(fpath):
        print(f"路径不是文件: {fpath}")
        return jsonify({'error': '路径不是文件'}), 400
    
    try:
        qa_system.kb_manager.delete_documents(where={"source": fpath})
        os.remove(fpath)
        # qa_system.kb_manager.check_collection()
        print(f"文件删除成功: {fpath}")
        return jsonify({'message': '文件已删除'})
    except PermissionError as e:
        print(f"权限错误: {str(e)}")
        return jsonify({'error': '没有权限删除文件'}), 403
    except Exception as e:
        print(f"删除文件失败: {str(e)}")
        return jsonify({'error': f'删除文件失败: {str(e)}'}), 500

@app.route('/api/switch-session', methods=['POST'])
def switch_session():
    """切换当前会话，不清空历史记录"""
    try:
        session_id = request.form.get('session_id')
        if not session_id:
            return jsonify({'error': '会话ID不能为空'}), 400
            
        # 这里不需要做特殊处理，因为每次请求都会传递session_id
        # 只需返回成功消息即可
        return jsonify({'message': '会话切换成功', 'session_id': session_id})
    except Exception as e:
        print(f"切换会话错误: {str(e)}")
        return jsonify({
            'error': '处理请求时发生错误',
            'details': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '接口不存在'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500

if __name__ == '__main__':
    print("启动AI聊天系统...")
    print("访问地址: http://localhost:5000")
    
    # 打印所有注册的路由
    print("\n注册的路由:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.endpoint}")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except OSError as e:
        print(f"启动失败: {e}")
    except Exception as e:
        print(f"启动失败: {e}")