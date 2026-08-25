import json
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

USERS_FILE = 'users.json'


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


# 用户类
class User:
    def __init__(self, username, password, name, courses, info, imageUrl):
        self.username = username
        self.password = password
        self.name = name
        self.courses = courses
        self.info = info
        self.imageUrl = imageUrl

    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "name": self.name,
            "courses": self.courses,
            "info": self.info,
            "imageUrl": self.imageUrl
        }


# 获取所有用户
@app.route('/api/users', methods=['GET'])
def get_users():
    users = read_users()
    return jsonify(users), 200


# 获取指定用户 profile
@app.route('/api/users/<username>/profile', methods=['GET'])
def get_profile(username):
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)
    if user:
        profile = {
            "name": user['name'],
            "courses": user['courses'],
            "info": user['info'],
            "imageUrl": user['imageUrl']
        }
        return jsonify(profile), 200
    else:
        return jsonify({"message": "User not found"}), 404


# 用户登录校验
@app.route('/api/login', methods=['POST'])
def login():
    login_data = request.json
    username = login_data.get('username')
    password = login_data.get('password')
    print(login_data)
    users = read_users()
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)
    if user:
        profile = {
            "name": user['name'],
            "courses": user['courses'],
            "info": user['info'],
            "imageUrl": user['imageUrl'],
            "role": user['role']
        }
        return jsonify(profile), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# 用户注册
@app.route('/api/register', methods=['POST'])
def register():
    register_data = request.json
    username = register_data.get('username')
    password = register_data.get('password')
    name = register_data.get('name')
    courses = register_data.get('courses', [])
    info = register_data.get('info', '')
    imageUrl = register_data.get('imageUrl', '')

    users = read_users()
    # 检查用户名是否已存在
    if any(u['username'] == username for u in users):
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username, password, name, courses, info, imageUrl)
    users.append(new_user.to_dict())
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201


# 使用 POST 方法更新用户 profile（头像URL，name和info）
@app.route('/api/users/<username>/profile', methods=['POST'])
def update_profile(username):
    update_data = request.json
    name = update_data.get('name')
    info = update_data.get('info')
    imageUrl = update_data.get('imageUrl')

    users = read_users()
    user = next((u for u in users if u['username'] == username), None)

    if user:
        # 更新用户的资料
        if name:
            user['name'] = name
        if info:
            user['info'] = info
        if imageUrl:
            user['imageUrl'] = imageUrl

        save_users(users)
        return jsonify({"message": "Profile updated successfully"}), 200
    else:
        return jsonify({"message": "User not found"}), 404


@app.route('/api/users/<username>/select_course', methods=['POST'])
def select_course(username):
    # 获取课程ID
    course_id = request.json.get('courseId')

    if not course_id:
        return jsonify({"message": "Course ID is required"}), 400

    # 读取用户列表
    users = read_users()
    user = next((u for u in users if u['username'] == username), None)

    if not user:
        return jsonify({"message": "User not found"}), 404

    # 如果该用户已经选择了这个课程，则返回错误
    if course_id in user['courses']:
        return jsonify({"message": "你已经选了这门课了！"}), 400

    # 将课程ID添加到用户课程列表中
    user['courses'].append(course_id)

    # 保存更新后的用户数据
    save_users(users)

    return jsonify({"message": "Course selected successfully"}), 200
if __name__ == '__main__':
    app.run(debug=True, port=5001)