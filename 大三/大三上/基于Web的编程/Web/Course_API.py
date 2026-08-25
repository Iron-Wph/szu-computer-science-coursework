import uuid
import os
import json
from datetime import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

COURSES_FILE = 'courses.json'


# 课程相关服务类
class CourseService:
    @staticmethod
    def read_courses():
        if not os.path.exists(COURSES_FILE):
            return []
        with open(COURSES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_courses(courses):
        with open(COURSES_FILE, 'w', encoding='utf-8') as f:
            json.dump(courses, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_course_by_id(course_id):
        courses = CourseService.read_courses()
        return next((c for c in courses if c['courseId'] == course_id), None)


# 公告相关服务类
class AnnouncementService:
    @staticmethod
    def get_announcements(course_id):
        announcements_file = f'courses/{course_id}/announcements.json'
        if not os.path.exists(announcements_file):
            return []
        with open(announcements_file, 'r', encoding='utf-8') as f:
            return json.load(f)


# 资源相关服务类
class ResourceService:
    @staticmethod
    def get_resources_file(course_id):
        resources_file = f'courses/{course_id}/resources.json'
        if not os.path.exists(resources_file):
            return []
        try:
            with open(resources_file, 'r', encoding='utf-8') as f:
                if os.stat(resources_file).st_size == 0:
                    return []  # 文件为空，返回空列表
                return json.load(f)
        except json.JSONDecodeError:
            return []  # 如果文件格式不正确或者为空，返回空列表

    @staticmethod
    def save_resources(course_id, resources):
        resources_file = f'courses/{course_id}/resources.json'
        os.makedirs(os.path.dirname(resources_file), exist_ok=True)  # 确保目录存在

        with open(resources_file, 'w', encoding='utf-8') as f:
            json.dump(resources, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_resources_by_course(course_id):
        return ResourceService.get_resources_file(course_id)


# 待完成事项相关服务类
class TodoItemService:
    @staticmethod
    def get_todo_file(course_id):
        todo_file = f'courses/{course_id}/todo-items.json'
        if not os.path.exists(todo_file):
            # 如果文件不存在，创建文件夹和空的待完成事项列表
            os.makedirs(os.path.dirname(todo_file), exist_ok=True)
            with open(todo_file, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        return todo_file

    @staticmethod
    def read_todo_items(course_id):
        todo_file = TodoItemService.get_todo_file(course_id)
        with open(todo_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_todo_items(course_id, todo_items):
        todo_file = TodoItemService.get_todo_file(course_id)
        with open(todo_file, 'w', encoding='utf-8') as f:
            json.dump(todo_items, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_all_todo_items(course_id):
        return TodoItemService.read_todo_items(course_id)

    @staticmethod
    def add_todo_item(course_id, item_data):
        todo_items = TodoItemService.read_todo_items(course_id)
        item_id = str(uuid.uuid4())
        new_item = {
            "id": item_id,
            "title": item_data.get("title"),
            "description": item_data.get("description"),
            "type": item_data.get("type"),
            "dueDate": item_data.get("dueDate"),
            "status": "Pending"  # 默认状态为 Pending
        }
        todo_items.append(new_item)
        TodoItemService.save_todo_items(course_id, todo_items)
        return new_item

    @staticmethod
    def get_todo_item(course_id, item_id):
        todo_items = TodoItemService.read_todo_items(course_id)
        return next((item for item in todo_items if item['id'] == item_id), None)

    @staticmethod
    def update_todo_item(course_id, item_id, updated_data):
        todo_items = TodoItemService.read_todo_items(course_id)
        for item in todo_items:
            if item['id'] == item_id:
                item.update(updated_data)
                TodoItemService.save_todo_items(course_id, todo_items)
                return item
        return None

    @staticmethod
    def delete_todo_item(course_id, item_id):
        todo_items = TodoItemService.read_todo_items(course_id)
        filtered_items = [item for item in todo_items if item['id'] != item_id]
        if len(filtered_items) == len(todo_items):
            return False  # 未找到要删除的项
        TodoItemService.save_todo_items(course_id, filtered_items)
        return True


# 评论相关服务类
class CommentService:
    @staticmethod
    def get_comments(course_id):
        comments_file = f'courses/{course_id}/comments.json'
        if not os.path.exists(comments_file):
            return []
        with open(comments_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_comments(course_id, comments):
        comments_file = f'courses/{course_id}/comments.json'
        os.makedirs(os.path.dirname(comments_file), exist_ok=True)  # 确保目录存在
        with open(comments_file, 'w', encoding='utf-8') as f:
            json.dump(comments, f, ensure_ascii=False, indent=4)

    @staticmethod
    def add_comment(course_id, comment_data):
        comment_id = str(uuid.uuid4())
        comment_data['id'] = comment_id
        comment_data['likes'] = 0
        comment_data['timestamp'] = datetime.utcnow().isoformat()  # 生成标准的 ISO 8601 格式时间戳
        comment_data['replies'] = []  # Initialize replies as an empty list
        comments = CommentService.get_comments(course_id)
        comments.append(comment_data)
        CommentService.save_comments(course_id, comments)
        return comment_data

    @staticmethod
    def add_reply(course_id, comment_id, reply_data):
        comments = CommentService.get_comments(course_id)
        for comment in comments:
            if comment['id'] == comment_id:
                reply_id = str(uuid.uuid4())
                reply_data['id'] = reply_id
                reply_data['timestamp'] = datetime.utcnow().isoformat()  # 使用 ISO 8601 格式时间戳
                comment['replies'].append(reply_data)
                CommentService.save_comments(course_id, comments)
                return reply_data
        return None

    @staticmethod
    def like_comment(course_id, comment_id):
        comments = CommentService.get_comments(course_id)
        for comment in comments:
            if comment['id'] == comment_id:
                comment['likes'] += 1
                CommentService.save_comments(course_id, comments)
                return comment
        return None


# 题库相关服务类
class QuestionService:
    QUESTIONS_FILE = 'quizzes/questions.json'

    @staticmethod
    def get_questions_file():
        if not os.path.exists(QuestionService.QUESTIONS_FILE):
            # 如果文件不存在，创建空的题库
            os.makedirs(os.path.dirname(QuestionService.QUESTIONS_FILE), exist_ok=True)
            with open(QuestionService.QUESTIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        return QuestionService.QUESTIONS_FILE

    @staticmethod
    def read_questions():
        questions_file = QuestionService.get_questions_file()
        with open(questions_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_questions(questions):
        questions_file = QuestionService.get_questions_file()
        with open(questions_file, 'w', encoding='utf-8') as f:
            json.dump(questions, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_question_by_id(question_id):
        questions = QuestionService.read_questions()
        return next((q for q in questions if q['id'] == question_id), None)

    @staticmethod
    def add_question(question_data):
        questions = QuestionService.read_questions()
        question_id = str(uuid.uuid4())
        new_question = {
            "id": question_id,
            "type": question_data.get("type"),
            "title": question_data.get("title"),
            "options": question_data.get("options", []),
            "answer": question_data.get("answer")
        }
        questions.append(new_question)
        QuestionService.save_questions(questions)
        return new_question


# 测验相关服务类
class QuizService:
    QUIZZES_FILE = 'quizzes/quizzes.json'

    @staticmethod
    def get_quizzes_file():
        if not os.path.exists(QuizService.QUIZZES_FILE):
            # 如果文件不存在，创建空的测验列表
            os.makedirs(os.path.dirname(QuizService.QUIZZES_FILE), exist_ok=True)
            with open(QuizService.QUIZZES_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=4)
        return QuizService.QUIZZES_FILE

    @staticmethod
    def read_quizzes():
        quizzes_file = QuizService.get_quizzes_file()
        with open(quizzes_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def save_quizzes(quizzes):
        quizzes_file = QuizService.get_quizzes_file()
        with open(quizzes_file, 'w', encoding='utf-8') as f:
            json.dump(quizzes, f, ensure_ascii=False, indent=4)

    @staticmethod
    def get_quiz_by_id(quiz_id):
        quizzes = QuizService.read_quizzes()
        return next((quiz for quiz in quizzes if quiz['id'] == quiz_id), None)

    @staticmethod
    def add_quiz(quiz_data):
        quizzes = QuizService.read_quizzes()
        quiz_id = str(uuid.uuid4())
        new_quiz = {
            "id": quiz_id,
            "title": quiz_data.get("title"),
            "description": quiz_data.get("description"),
            "questions": quiz_data.get("questions", [])  # List of question IDs
        }
        quizzes.append(new_quiz)
        QuizService.save_quizzes(quizzes)
        return new_quiz


# 待完成事项相关路由
@app.route('/api/courses/<course_id>/todo-items', methods=['GET'])
def get_todo_items(course_id):
    todo_items = TodoItemService.get_all_todo_items(course_id)
    if todo_items:
        return jsonify(todo_items), 200
    else:
        return jsonify({"message": "没有找到待完成事项"}), 404


# 添加新的待完成事项
@app.route('/api/courses/<course_id>/todo-items', methods=['POST'])
def add_todo_item(course_id):
    item_data = request.json
    required_fields = ['title', 'description', 'type', 'dueDate']
    if not all(field in item_data for field in required_fields):
        return jsonify({"message": f"缺少必要的字段: {', '.join(required_fields)}"}), 400
    if item_data['type'] not in ['quiz', 'assignment']:
        return jsonify({"message": "类型必须是 'quiz' 或 'assignment'"}), 400
    new_item = TodoItemService.add_todo_item(course_id, item_data)
    return jsonify(new_item), 201


# 获取单个待完成事项
@app.route('/api/courses/<course_id>/todo-items/<item_id>', methods=['GET'])
def get_todo_item(course_id, item_id):
    item = TodoItemService.get_todo_item(course_id, item_id)
    if item:
        return jsonify(item), 200
    else:
        return jsonify({"message": "待完成事项未找到"}), 404


# 更新待完成事项
@app.route('/api/courses/<course_id>/todo-items/<item_id>', methods=['PUT'])
def update_todo_item(course_id, item_id):
    updated_data = request.json
    valid_fields = ['title', 'description', 'type', 'dueDate', 'status']
    if not any(field in updated_data for field in valid_fields):
        return jsonify({"message": f"至少需要提供以下字段之一进行更新: {', '.join(valid_fields)}"}), 400
    if 'type' in updated_data and updated_data['type'] not in ['quiz', 'assignment']:
        return jsonify({"message": "类型必须是 'quiz' 或 'assignment'"}), 400
    updated_item = TodoItemService.update_todo_item(course_id, item_id, updated_data)
    if updated_item:
        return jsonify(updated_item), 200
    else:
        return jsonify({"message": "待完成事项未找到"}), 404


# 删除待完成事项
@app.route('/api/courses/<course_id>/todo-items/<item_id>', methods=['DELETE'])
def delete_todo_item(course_id, item_id):
    success = TodoItemService.delete_todo_item(course_id, item_id)
    if success:
        return jsonify({"message": "待完成事项已删除"}), 200
    else:
        return jsonify({"message": "待完成事项未找到"}), 404


# 回复课程评论
@app.route('/api/courses/<course_id>/comments/<comment_id>/replies', methods=['POST'])
def add_reply(course_id, comment_id):
    reply_data = request.json
    if 'username' not in reply_data or 'content' not in reply_data:
        return jsonify({"message": "缺少必要的字段: username 或 content"}), 400

    reply = CommentService.add_reply(course_id, comment_id, reply_data)
    if reply:
        return jsonify(reply), 201
    else:
        return jsonify({"message": "评论未找到，无法回复"}), 404


# 获取课程评论
@app.route('/api/courses/<course_id>/comments', methods=['GET'])
def get_comments(course_id):
    comments = CommentService.get_comments(course_id)
    if comments:
        return jsonify(comments), 200
    else:
        return jsonify({"message": "没有找到评论"}), 404


# 添加课程评论
@app.route('/api/courses/<course_id>/comments', methods=['POST'])
def add_comment(course_id):
    comment_data = request.json
    if 'username' not in comment_data or 'content' not in comment_data:
        return jsonify({"message": "缺少必要的字段: username 或 content"}), 400

    comment = CommentService.add_comment(course_id, comment_data)
    return jsonify(comment), 201


# 点赞课程评论
@app.route('/api/comments/<comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    course_id = request.args.get('course_id')
    if not course_id:
        return jsonify({"message": "缺少课程ID"}), 400

    comment = CommentService.like_comment(course_id, comment_id)
    if comment:
        return jsonify(comment), 200
    else:
        return jsonify({"message": "评论未找到"}), 404


# 获取课程资源详情
@app.route('/api/courses/<course_id>/<resource_id>', methods=['GET'])
def get_resource_by_id(course_id, resource_id):
    resources = ResourceService.get_resources_file(course_id)
    for resource in resources:
        if resource['id'] == resource_id:
            return jsonify(resource), 200
    return jsonify({"message": "资源未找到"}), 404


# 获取课程资源
@app.route('/api/courses/<course_id>/resources', methods=['GET'])
def get_resources(course_id):
    resources = ResourceService.get_resources_by_course(course_id)
    if resources:
        return jsonify(resources), 200
    else:
        return jsonify({"message": "没有找到该课程的资源"}), 404


# 为课程添加资源
@app.route('/api/courses/<course_id>/resources', methods=['POST'])
def add_resource(course_id):
    resource_data = request.json
    resource_id = str(uuid.uuid4())
    resource_data['id'] = resource_id
    resource_data.pop('courseId', None)
    resources = ResourceService.get_resources_by_course(course_id)
    resources.append(resource_data)
    ResourceService.save_resources(course_id, resources)

    return jsonify({"message": "资源已成功添加！", "id": resource_id}), 201


# 添加课程
@app.route('/api/courses', methods=['POST'])
def add_course():
    course_data = request.json
    courses = CourseService.read_courses()
    courses.append(course_data)
    CourseService.save_courses(courses)
    return jsonify({"message": "课程已成功提交！"}), 201


# 获取全部课程
@app.route('/api/courses', methods=['GET'])
def get_courses():
    courses = CourseService.read_courses()
    return jsonify(courses), 200


# 获取指定课程信息
@app.route('/api/courses/<course_id>', methods=['GET'])
def get_course_by_id(course_id):
    course = CourseService.get_course_by_id(course_id)
    if course:
        return jsonify(course), 200
    else:
        return jsonify({"message": "课程未找到"}), 404


# 获取指定公告
@app.route('/api/courses/<course_id>/announcements', methods=['GET'])
def get_announcements_for_course(course_id):
    announcements = AnnouncementService.get_announcements(course_id)
    if announcements:
        return jsonify(announcements), 200
    else:
        return jsonify({"message": "没有找到该课程的公告"}), 404


# 获取测验详情
@app.route('/api/quizzes/<quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = QuizService.get_quiz_by_id(quiz_id)
    if not quiz:
        return jsonify({"message": "测验未找到"}), 404

    # 获取测验关联的题目
    questions = []
    for q_id in quiz.get('questions', []):
        question = QuestionService.get_question_by_id(q_id)
        if question:
            questions.append(question)

    if not questions:
        return jsonify({"message": "测验没有关联的题目"}), 404

    # 返回测验详情和题目
    quiz_details = {
        "id": quiz['id'],
        "title": quiz['title'],
        "description": quiz['description'],
        "questions": questions
    }
    return jsonify(quiz_details), 200


# 提交测验答案
@app.route('/api/quizzes/<quiz_id>/submit', methods=['POST'])
def submit_quiz(quiz_id):
    quiz = QuizService.get_quiz_by_id(quiz_id)
    if not quiz:
        return jsonify({"message": "测验未找到"}), 404

    submitted_answers = request.json.get('answers', {})
    if not isinstance(submitted_answers, dict):
        return jsonify({"message": "提交的答案格式不正确"}), 400

    questions = []
    for q_id in quiz.get('questions', []):
        question = QuestionService.get_question_by_id(q_id)
        if question:
            questions.append(question)

    if not questions:
        return jsonify({"message": "测验没有关联的题目"}), 404

    # 评分逻辑
    total = len(questions)
    correct = 0
    feedback = []

    for question in questions:
        q_id = question['id']
        correct_answer = question['answer']
        user_answer = submitted_answers.get(q_id)

        if question['type'] in ['single', 'truefalse']:
            is_correct = user_answer == correct_answer
        elif question['type'] == 'multiple':
            if isinstance(user_answer, list):
                is_correct = set(user_answer) == set(correct_answer)
            else:
                is_correct = False
        elif question['type'] == 'short':
            if isinstance(user_answer, str):
                is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            else:
                is_correct = False
        else:
            is_correct = False

        if is_correct:
            correct += 1
            feedback.append({
                "question_id": q_id,
                "correct": True,
                "message": "正确"
            })
        else:
            feedback.append({
                "question_id": q_id,
                "correct": False,
                "message": f"错误。正确答案是: {correct_answer}"
            })

    score = {
        "total": total,
        "correct": correct,
        "percentage": (correct / total) * 100 if total > 0 else 0,
        "feedback": feedback
    }

    return jsonify({
        "message": "测验提交成功",
        "score": score
    }), 200


# 添加新的题目
@app.route('/api/questions', methods=['POST'])
def add_question():
    question_data = request.json
    required_fields = ['type', 'title', 'answer']
    if not all(field in question_data for field in required_fields):
        return jsonify({"message": f"缺少必要的字段: {', '.join(required_fields)}"}), 400
    if question_data['type'] not in ['single', 'multiple', 'short', 'truefalse']:
        return jsonify({"message": "题目类型必须是 'single', 'multiple', 'short' 或 'truefalse'"}), 400
    new_question = QuestionService.add_question(question_data)
    return jsonify(new_question), 201


# 添加新的测验
@app.route('/api/quizzes', methods=['POST'])
def add_quiz():
    quiz_data = request.json
    required_fields = ['title', 'description', 'questions']
    if not all(field in quiz_data for field in required_fields):
        return jsonify({"message": f"缺少必要的字段: {', '.join(required_fields)}"}), 400
    if not isinstance(quiz_data['questions'], list):
        return jsonify({"message": "questions 字段必须是一个列表"}), 400
    # 验证题目 ID 是否存在
    for q_id in quiz_data['questions']:
        question = QuestionService.get_question_by_id(q_id)
        if not question:
            return jsonify({"message": f"题目 ID {q_id} 未找到"}), 404
    new_quiz = QuizService.add_quiz(quiz_data)
    return jsonify(new_quiz), 201

@app.route('/api/homepage/courses', methods=['GET'])
def get_homepage_courses():
    if not os.path.exists("homepage_courses.json"):
        return jsonify({"message": "主页课程配置文件未找到"}), 404

    with open("homepage_courses.json", 'r', encoding='utf-8') as f:
        homepage_courses = json.load(f)

    # 获取各类别的课程ID
    slider_ids = homepage_courses.get('slider', [])
    latest_ids = homepage_courses.get('latest', [])
    recommendation_ids = homepage_courses.get('recommendation', [])

    # 根据课程ID获取课程详情
    courses = CourseService.read_courses()

    # 分别获取不同类别的课程详情
    slider_courses = [course for course in courses if course['courseId'] in slider_ids]
    latest_courses = [course for course in courses if course['courseId'] in latest_ids]
    recommendation_courses = [course for course in courses if course['courseId'] in recommendation_ids]

    # 返回响应时按照类别分类
    response = {
        "slider": slider_courses,
        "latest": latest_courses,
        "recommendation": recommendation_courses
    }

    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)