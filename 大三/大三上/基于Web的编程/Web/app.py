from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# 读取题库文件
def load_questions():
    with open('questions.json', 'r', encoding='utf-8') as f:
        return json.load(f)

@app.route('/api/questions')
def get_questions():
    # 获取请求参数中的 type
    question_type = request.args.get('type')
    
    try:
        questions = load_questions()
        
        # 如果指定了题目类型且该类型存在
        if question_type and question_type in questions:
            return jsonify({
                "code": 200,
                "data": questions[question_type],
                "message": "success"
            })
        # 如果未指定类型或类型不存在
        else:
            return jsonify({
                "code": 400,
                "data": None,
                "message": "Invalid question type"
            })
            
    except Exception as e:
        return jsonify({
            "code": 500,
            "data": None,
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True) 