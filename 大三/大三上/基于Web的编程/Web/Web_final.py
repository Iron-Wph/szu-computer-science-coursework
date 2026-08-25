from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import hashlib
import os

app = Flask(__name__)
CORS(app)

def generate_token():
    return hashlib.sha256(os.urandom(24)).hexdigest()

@app.route('/api/register', methods=['POST'])
def add_student():
    student_data = request.get_json()
    if 'studentId' not in student_data or 'password' not in student_data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        with open('students.json', 'r', encoding='utf-8') as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        students = []

    students.append({
        "studentId": student_data["studentId"],
        "name": student_data.get("name", "Unknown"),
        "password": student_data["password"]
    })

    with open('students.json', 'w', encoding='utf-8') as file:
        json.dump(students, file, ensure_ascii=False, indent=4)

    return jsonify({"message": "Student added successfully!"}), 200

@app.route('/api/login', methods=['POST'])
def login_student():
    login_data = request.get_json()
    student_id = login_data.get("studentId")
    password = login_data.get("password")

    if not student_id or not password:
        return jsonify({"message": "用户名和密码不能为空"}), 400

    try:
        with open('students.json', 'r', encoding='utf-8') as file:
            students = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"message": "没有注册的用户"}), 400
    user = next((s for s in students if s['studentId'] == student_id), None)
    if not user or user['password'] != password:
        return jsonify({"message": "用户名或密码错误"}), 401
    token = generate_token()
    return jsonify({
        "token": token,
        "username": user["studentId"],
        "nickname": user["name"]
    }), 200

if __name__ == '__main__':
    app.run(debug=True)
