import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

USERS_FILE = 'users.json'
HOMEPAGE_COURSES_FILE = 'homepage_courses.json'


# 读取用户数据
def read_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# 保存用户数据
def save_users(users):
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)


# 读取首页课程配置
def read_homepage_courses():
    if not os.path.exists(HOMEPAGE_COURSES_FILE):
        return {'slider': [], 'latest': [], 'recommendation': []}
    with open(HOMEPAGE_COURSES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


# 保存首页课程配置
def save_homepage_courses(data):
    with open(HOMEPAGE_COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 获取所有学生账号
@app.route('/api/admin/users', methods=['GET'])
def get_users():
    users = read_users()
    students = [user for user in users if user['role'] == 'student']
    return jsonify(students), 200


# 管理课程：删除课程
@app.route('/api/admin/courses/<course_id>', methods=['DELETE'])
def delete_course(course_id):
    users = read_users()
    for user in users:
        if 'courses' in user:
            user['courses'] = [course for course in user['courses'] if course['courseId'] != course_id]
    save_users(users)
    return jsonify({"message": f"课程 {course_id} 已删除"}), 200


# 管理课程：取消学生的选课机会
@app.route('/api/admin/students/<username>/courses/<course_id>', methods=['DELETE'])
def remove_course_from_student(username, course_id):
    users = read_users()
    user = next((u for u in users if u['username'] == username and u['role'] == 'student'), None)
    if not user:
        return jsonify({"message": "学生未找到"}), 404
    user['courses'] = [course for course in user['courses'] if course['courseId'] != course_id]
    save_users(users)
    return jsonify({"message": f"课程 {course_id} 已从学生 {username} 的选课中移除"}), 200


# 管理首页轮播图：获取首页课程
@app.route('/api/admin/homepage/courses', methods=['GET'])
def get_homepage_courses():
    homepage_courses = read_homepage_courses()
    return jsonify(homepage_courses), 200


# 管理首页轮播图：更新首页课程
@app.route('/api/admin/homepage/courses', methods=['PUT'])
def update_homepage_courses():
    data = request.json
    save_homepage_courses(data)
    return jsonify({"message": "首页课程配置已更新"}), 200


# 开关自助注册按钮
@app.route('/api/admin/self-registration', methods=['PUT'])
def toggle_self_registration():
    config = request.json
    self_registration_enabled = config.get('enabled', False)
    # 假设我们有一个文件记录此配置
    with open('self_registration_config.json', 'w', encoding='utf-8') as f:
        json.dump({"enabled": self_registration_enabled}, f, ensure_ascii=False, indent=4)
    return jsonify({"message": f"自助注册功能已{'启用' if self_registration_enabled else '禁用'}"}), 200


if __name__ == '__main__':
    app.run(debug=True,port=5004)