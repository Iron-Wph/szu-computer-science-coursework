from flask import Blueprint, jsonify, request
from flask import Flask
from flask_cors import CORS
import json
import os

# 获取题库文件的绝对路径
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), 'questions', 'questions.json')

app = Flask(__name__)
CORS(app)



def load_questions():
    try:
        with open(QUESTIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"当前工作目录: {os.getcwd()}")
        raise Exception(f"读取题库文件失败: {str(e)}")

@app.route('/api/questions')
def get_questions():
    """获取题目接口"""
    # 获取题目类型参数
    question_type = request.args.get('type')
    # 验证题目类型是否合法
    valid_types = {'single', 'multiple', 'judge', 'fill', 'essay'}
    
    try:
        # 如果未提供题型或题型不合法
        if not question_type or question_type not in valid_types:
            return jsonify({
                "code": 400,
                "data": None,
                "message": "无效的题目类型，可选类型：single/multiple/judge/fill/essay"
            })
        
        # 读取题库
        questions = load_questions()
        
        # 获取指定类型的题目
        if question_type in questions:
            return jsonify({
                "code": 200,
                "data": questions[question_type],
                "message": "success"
            })
        else:
            return jsonify({
                "code": 404,
                "data": None,
                "message": f"未找到{question_type}类型的题目"
            })
            
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": None,
            "message": f"服务器错误: {str(e)}"
        }) 
    

if __name__ == '__main__':
    app.run(debug=True, port=5002)