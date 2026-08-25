from flask import Flask, request, jsonify
import json
import os
import hashlib
from datetime import datetime, timedelta, timezone
import jwt
import random


SECRET_KEY = '0ddsadjasiljoasjiodas12221e12e1e121212sada4524ds2fsdfssadaasdas1'

# 创建 Flask 应用
app = Flask(__name__)

# 数据文件路径
db_path = 'db.json'

# 加载数据库
def load_db():
    if os.path.exists(db_path):
        with open(db_path, 'r') as file:
            return json.load(file)
    else:
        return {"users": {}, "courses": {},
                "students": {}, "teachers": {},
                "administrators": {}, "assignments": {},
                "enrollments": {}, "homeworks": {},
                "questions": {
                    "szu":[
                            {
                                "question": "JavaScript是一种什么样的语言？",
                                "options": [
                                    "A. 编译型语言",
                                    "B. 标记语言",
                                    "C. 解释型语言",
                                    "D. 以上都不是"
                                ],
                                "answer": "C",
                                "reason": "JavaScript是一种解释型语言，因为它的代码在运行时逐行解释执行，而不是在执行前编译成机器码。"
                            },
                            {
                                "question": "JavaScript主要用于什么？",
                                "options": [
                                    "A. 服务器端开发",
                                    "B. 数据库管理",
                                    "C. 客户端脚本",
                                    "D. 操作系统开发"
                                ],
                                "answer": "C",
                                "reason": "JavaScript最初是为浏览器设计的，用于增强网页的交互性，因此主要用于客户端脚本。"
                            },
                            {
                                "question": "以下哪个是JavaScript的全局对象？",
                                "options": [
                                    "A. window",
                                    "B. document",
                                    "C. navigator",
                                    "D. 以上都是"
                                ],
                                "answer": "D",
                                "reason": "window、document和navigator都是浏览器环境中的全局对象，它们在JavaScript中具有全局作用域。"
                            },
                            {
                                "question": "JavaScript中的`var`和`let`关键字有什么区别？",
                                "options": [
                                    "A. `var`有块级作用域，`let`没有",
                                    "B. `var`没有块级作用域，`let`有",
                                    "C. 两者都有块级作用域",
                                    "D. 两者都没有块级作用域"
                                ],
                                "answer": "B",
                                "reason": "`var`声明的变量具有函数作用域或全局作用域，而`let`声明的变量具有块级作用域。"
                            },
                            {
                                "question": "JavaScript中的`==`和`===`有什么区别？",
                                "options": [
                                    "A. `==`是严格等于，`===`是非严格等于",
                                    "B. `==`是非严格等于，`===`是严格等于",
                                    "C. 两者都是严格等于",
                                    "D. 两者都是非严格等于"
                                ],
                                "answer": "B",
                                "reason": "`==`是非严格等于，会在比较前进行类型转换；`===`是严格等于，不会进行类型转换，如果类型不同直接返回false。"
                            },
                            {
                                "question": "JavaScript中如何创建一个数组？",
                                "options": [
                                    "A. var array = {}",
                                    "B. var array = (1, 2, 3)",
                                    "C. var array = new Array(1, 2, 3)",
                                    "D. 以上都可以"
                                ],
                                "answer": "D",
                                "reason": "在JavaScript中，可以使用字面量语法（如B和C选项所示），或者使用`new Array`构造函数来创建数组。"
                            },
                            {
                                "question": "JavaScript中，`null`和`undefined`有什么区别？",
                                "options": [
                                    "A. `null`是一个表示没有值的特殊值，`undefined`表示变量未定义",
                                    "B. `null`表示变量未定义，`undefined`是一个表示没有值的特殊值",
                                    "C. 两者都表示没有值",
                                    "D. 两者都表示变量未定义"
                                ],
                                "answer": "A",
                                "reason": "`null`是一个表示没有值的特殊值，用于表示空引用；`undefined`表示变量已声明但未定义，或者函数没有返回值。"
                            },
                            {
                                "question": "JavaScript中，`function`关键字声明的函数和函数表达式有什么区别？",
                                "options": [
                                    "A. 函数声明会提升，函数表达式不会",
                                    "B. 函数表达式会提升，函数声明不会",
                                    "C. 两者都会被提升",
                                    "D. 两者都不会被提升"
                                ],
                                "answer": "A",
                                "reason": "函数声明会被提升到它们所在的作用域的顶部，而函数表达式则不会。"
                            },
                            {
                                "question": "JavaScript中，`console.log`用于做什么？",
                                "options": [
                                    "A. 计算数学表达式",
                                    "B. 输出错误信息到控制台",
                                    "C. 输出信息到控制台",
                                    "D. 格式化字符串"
                                ],
                                "answer": "C",
                                "reason": "`console.log`用于将信息输出到浏览器的控制台，是调试JavaScript代码的常用方法。"
                            },
                            {
                                "question": "JavaScript中，`typeof`运算符返回什么？",
                                "options": [
                                    "A. 一个数字",
                                    "B. 一个字符串",
                                    "C. 一个对象",
                                    "D. 一个布尔值"
                                ],
                                "answer": "B",
                                "reason": "`typeof`运算符返回一个字符串，表示未经计算的操作数的类型。"
                            },
                            {
                                "question": "JavaScript中，`Array.prototype.map`方法的作用是什么？",
                                "options": [
                                    "A. 过滤数组中的元素",
                                    "B. 对数组中的每个元素执行一个函数",
                                    "C. 将数组连接成字符串",
                                    "D. 反转数组"
                                ],
                                "answer": "B",
                                "reason": "`map`方法创建一个新数组，其结果是该数组中的每个元素是调用一次提供的函数后的返回值。"
                            },
                            {
                                "question": "JavaScript中，`==`和`===`运算符的主要区别是什么？",
                                "options": [
                                    "A. `==`会进行类型转换，`===`不会",
                                    "B. `==`不会进行类型转换，`===`会",
                                    "C. 两者都会进行类型转换",
                                    "D. 两者都不会进行类型转换"
                                ],
                                "answer": "A",
                                "reason": "`==`运算符在比较时会进行类型转换，而`===`运算符则不会，如果类型不同直接返回false。"
                            },
                            {
                                "question": "JavaScript中，`try...catch`语句的作用是什么？",
                                "options": [
                                    "A. 循环执行代码直到成功",
                                    "B. 捕获代码执行中的错误",
                                    "C. 条件执行代码",
                                    "D. 定义代码块"
                                ],
                                "answer": "B",
                                "reason": "`try...catch`语句用于捕获代码执行中的错误，以便程序可以处理异常而不是崩溃。"
                            },
                            {
                                "question": "JavaScript中，`const`声明的变量是否可以重新赋值？",
                                "options": [
                                    "A. 是的，可以重新赋值",
                                    "B. 不可以，`const`声明的变量是只读的",
                                    "C. 只能重新赋值一次",
                                    "D. 只能在声明时赋值"
                                ],
                                "answer": "B",
                                "reason": "`const`声明的变量是只读的，一旦赋值后不能被重新赋值，但可以修改其属性（如果是对象的话）。"
                            },
                            {
                                "question": "JavaScript中，`Promise`对象主要用于什么？",
                                "options": [
                                    "A. 处理服务器请求",
                                    "B. 处理异步操作",
                                    "C. 处理DOM事件",
                                    "D. 处理样式变化"
                                ],
                                "answer": "B",
                                "reason": "`Promise`对象用于异步计算，它代表了一个可能还不可用的值，或者一个在未来某个时间点才可用的最终值。"
                            },
                            {
                                "question": "JavaScript中，`arguments`对象是什么？",
                                "options": [
                                    "A. 一个包含所有命令行参数的对象",
                                    "B. 一个包含函数调用时传递的所有参数的对象",
                                    "C. 一个包含函数定义时所有参数的对象",
                                    "D. 一个包含函数调用栈的对象"
                                ],
                                "answer": "B",
                                "reason": "`arguments`对象是一个类数组对象，它包含了函数调用时传递的所有参数。"
                            },
                            {
                                "question": "JavaScript中，`this`关键字指向什么？",
                                "options": [
                                    "A. 全局对象",
                                    "B. 当前对象",
                                    "C. 函数的调用者",
                                    "D. 函数本身"
                                ],
                                "answer": "B",
                                "reason": "`this`关键字在函数中指向函数的调用者，但这个调用者取决于函数是如何被调用的。"
                            },
                            {
                                "question": "JavaScript中，`setTimeout`函数的作用是什么？",
                                "options": [
                                    "A. 立即执行代码",
                                    "B. 在指定的毫秒数后执行代码",
                                    "C. 无限循环执行代码",
                                    "D. 每间隔指定的毫秒数执行代码"
                                ],
                                "answer": "B",
                                "reason": "`setTimeout`函数用于在指定的毫秒数后执行代码，它接受一个函数和一个时间作为参数。"
                            },
                            {
                                "question": "JavaScript中，`JSON.parse()`和`JSON.stringify()`方法的作用是什么？",
                                "options": [
                                    "A. 解析JSON字符串和序列化JavaScript对象",
                                    "B. 解析XML字符串和序列化JavaScript对象",
                                    "C. 解析HTML字符串和序列化JavaScript对象",
                                    "D. 解析JavaScript对象和序列化JSON字符串"
                                ],
                                "answer": "A",
                                "reason": "`JSON.parse()`用于将JSON字符串解析成JavaScript对象，`JSON.stringify()`用于将JavaScript对象序列化成JSON字符串。"
                            },
                            {
                                "question": "JavaScript中，`document.getElementById()`方法的作用是什么？",
                                "options": [
                                    "A. 获取指定ID的第一个元素",
                                    "B. 获取指定ID的所有元素",
                                    "C. 创建一个新的元素",
                                    "D. 删除指定ID的元素"
                                ],
                                "answer": "A",
                                "reason": "`document.getElementById()`方法用于获取文档中指定ID的第一个元素。"
                            },
                            {
                                "question": "JavaScript中，`Array.prototype.forEach`方法的作用是什么？",
                                "options": [
                                    "A. 创建一个新数组",
                                    "B. 对数组中的每个元素执行一个函数",
                                    "C. 过滤数组中的元素",
                                    "D. 将数组连接成字符串"
                                ],
                                "answer": "B",
                                "reason": "`forEach`方法对数组中的每个元素执行一次提供的函数，这个方法没有返回值。"
                            },
                            {
                                "question": "JavaScript中，`async`和`await`关键字用于什么？",
                                "options": [
                                    "A. 处理DOM事件",
                                    "B. 处理异步操作",
                                    "C. 处理样式变化",
                                    "D. 处理服务器请求"
                                ],
                                "answer": "B",
                                "reason": "`async`和`await`关键字用于异步函数，它们使得异步代码的编写和阅读更接近同步代码的风格。"
                            },
                            {
                                "question": "JavaScript中，`document.querySelector()`和`document.querySelectorAll()`方法的区别是什么？",
                                "options": [
                                    "A. `querySelector`返回第一个匹配的元素，`querySelectorAll`返回所有匹配的元素",
                                    "B. `querySelector`返回所有匹配的元素，`querySelectorAll`返回第一个匹配的元素",
                                    "C. 两者都返回所有匹配的元素",
                                ],
                                "answer": "A",
                                "reason": "`querySelector`返回文档中匹配指定CSS选择器的第一个元素，而`querySelectorAll`返回所有匹配指定CSS选择器的元素的一个NodeList集合。"
                            },
                            {
                                "question": "JavaScript中，`Function.prototype.bind`方法的作用是什么？",
                                "options": [
                                    "A. 创建一个新函数，当被调用时，将其`this`关键字设置为提供的值",
                                    "B. 创建一个新函数，当被调用时，忽略其`this`关键字",
                                    "C. 创建一个新函数，当被调用时，将其`this`关键字设置为全局对象",
                                    "D. 创建一个新函数，当被调用时，将其`this`关键字设置为`undefined`"
                                ],
                                "answer": "A",
                                "reason": "`bind`方法创建一个新函数，在调用时将`this`关键字设置为提供的值，这允许你预设函数的`this`值。"
                            },
                            {
                                "question": "JavaScript中，`Array.prototype.filter`方法的作用是什么？",
                                "options": [
                                    "A. 创建一个新数组，包含通过测试的所有元素",
                                    "B. 创建一个新数组，不包含通过测试的所有元素",
                                    "C. 修改原数组，包含通过测试的所有元素",
                                    "D. 修改原数组，不包含通过测试的所有元素"
                                ],
                                "answer": "A",
                                "reason": "`filter`方法创建一个新数组，其包含通过所提供函数实现的测试的所有元素。"
                            },
                            {
                                "question": "JavaScript中，`Object.keys()`方法的作用是什么？",
                                "options": [
                                    "A. 返回一个包含对象所有值的数组",
                                    "B. 返回一个包含对象所有键的数组",
                                    "C. 返回一个包含对象所有属性的数组",
                                    "D. 返回一个包含对象所有方法的数组"
                                ],
                                "answer": "B",
                                "reason": "`Object.keys()`方法返回一个由给定对象的自身可枚举属性组成的数组，数组中属性的顺序与使用for...in循环遍历时返回的顺序相同。"
                            },
                            {
                                "question": "JavaScript中，`==`和`===`运算符的主要区别是什么？",
                                "options": [
                                    "A. `==`会进行类型转换，`===`不会",
                                    "B. `==`不会进行类型转换，`===`会",
                                    "C. 两者都会进行类型转换",
                                    "D. 两者都不会进行类型转换"
                                ],
                                "answer": "A",
                                "reason": "`==`运算符是非严格相等运算符，如果两个值的类型不同，JavaScript会尝试将它们转换为相同的类型再进行比较。而`===`运算符是严格相等运算符，不会进行类型转换，如果两个值的类型不同，直接返回false。"
                            }
                        ]}
                }

# 保存数据库
def save_db(db):
    with open(db_path, 'w') as file:
        json.dump(db, file, indent=4)

# 加载用户和课程数据
db = load_db()
users = db['users']
courses = db['courses']
students = db['students']
teachers = db['teachers']
administrators = db['administrators']
assignments = db['assignments']
enrollments = db['enrollments']         # 学生选课记录
homeworks = db['homeworks']             # 学生作业记录
questions = db['questions']             # 题库

# 获取jwt的token
def generate_jwt(user_id):
    payload = {
        'exp': datetime.now(timezone.utc) + timedelta(days=0, hours=12),  # 设置过期时间为12小时后
        'iat': datetime.now(timezone.utc),  # 发布时间为当前时间
        'sub': user_id  # 用户ID作为JWT的主题
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

# 获取哈希值
def generate_hash(str):
    return hashlib.sha256(str.encode()).hexdigest()[:10]

# 获取固定格式的时间
def getDate():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 1.1 登录接口
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password_hash = data.get('passwordHash')
    # 根据userID查找用户
    user = users.get(generate_hash(username))

    if user and user['status'] == '禁用':
        return jsonify({"success": False, "message": "账户已被冻结，请联系管理员"})

    if user and user['passwordHash'] == password_hash:
        user['failedAttempts'] = 0  # 登录成功后重置失败次数
        save_db(db)
        return jsonify({
            "success": True,
            "message": "登录成功",
            "userDetails": {
                "userId": user['userID'],
                "userType": user['userType'],
                "avatar": "",
                "registrationDate": user['registrationDate'],
                "status": "正常"
            },
            "token": generate_jwt(user['userID'])
        })
    else:
        # 登录失败时，增加失败次数
        user['failedAttempts'] += 1
        if user['failedAttempts'] >= 5:
            # 登录失败次数超过5次，冻结账户
            user['status'] = '禁用'
            user['freezeReason'] = "密码错误次数超过5次"
            save_db(db)
        return jsonify({"success": False, "message": "用户名或密码错误，最多可以尝试5次"})


# 1.2 注册接口
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password_hash = data.get('passwordHash')
    user_type = data.get('userType')

    # 使用SHA-256算法生成哈希值，并取前10位作为userID
    userID = generate_hash(username)
    if username not in users:
        # 注册时设置为非冻结状态，密码错误次数为0
        users[userID] = {"userID":userID, "passwordHash": password_hash, "userType": user_type,
                           "registrationDate": getDate(), "status": '正常', "failedAttempts": 0,
                           "freezeReason": None}
        # 根据用户类型，添加到对应的用户列表
        if user_type == 'student':
            students[userID] = {
                "userId": userID,
                "studentId": userID,
                "studentName": username
            }
        elif user_type == 'teacher':
            teachers[userID] = {
                "userId": userID,
                "teacherId": userID,
                "teacherName": username
            }
        elif user_type == 'administrator':
            administrators[userID] = {
                "userId": userID,
                "administratorId": userID,
                "administratorName": username
            }

        save_db(db)  # 保存更新到文件
        return jsonify({"success": True, "message": "注册成功", "userId": userID})
    else:
        return jsonify({"success": False, "message": "用户名已存在"})


# 2.1 获取最新的课程列表
@app.route('/api/course/latest', methods=['POST'])
def get_latest_courses():
    data = request.get_json()

    # 获取所有课程ID列表
    course_ids = list(courses.keys())
    # 获取所有课程详细信息，并按照发布时间排序
    sorted_courses = sorted(courses.values(), key=lambda x: x['publishedDate'],reverse=True)
    # 根据分页参数获取分页后的课程详细信息
    sliced_courses = sorted_courses[0: 4]

    # 构造返回的分页课程信息
    paginated_courses = []
    for course in sliced_courses:
        paginated_course = {
            'courseId': course['courseId'],
            'courseName': course['courseName'],
            'teacherName': course['teacherName'],
            'teacherId': course['teacherId'],
            'summary': course['summary'],
            'publishedDate': course['publishedDate'],
            'isRecommended': course['isRecommended'],
            'numberOfStudents': course['numberOfStudents'],
            'imageUrl': course['imageUrl'],
            'credit': course['credit'],
            'hours': course['hours'],
            'detailedDescription': course['detailedDescription'],
            'university': course['university'],
            'startDate': course['startDate']
        }
        paginated_courses.append(paginated_course)

    return {
        "success": True,
        'courses': paginated_courses,
        "pagination": {
            "currentPage": 1,
            "totalPages": 1,
            "totalItems": len(sliced_courses)
        }
    }

# 2.1 获取推荐的课程列表
@app.route('/api/course/recommondation', methods=['POST'])
def get_recommonded_courses():
    data = request.get_json()

    # 获取所有课程ID列表
    course_ids = list(courses.keys())
    # 获取所有课程详细信息，并按照是否推荐排序
    sorted_courses = sorted(courses.values(), key=lambda x: (x['isRecommended'], -x['numberOfStudents']), reverse=True)
    # 根据分页参数获取分页后的课程详细信息
    sliced_courses = sorted_courses[0: 4]

    # 构造返回的分页课程信息
    paginated_courses = []
    for course in sliced_courses:
        paginated_course = {
            'courseId': course['courseId'],
            'courseName': course['courseName'],
            'teacherName': course['teacherName'],
            'teacherId': course['teacherId'],
            'summary': course['summary'],
            'publishedDate': course['publishedDate'],
            'isRecommended': course['isRecommended'],
            'numberOfStudents': course['numberOfStudents'],
            'imageUrl': course['imageUrl'],
            'credit': course['credit'],
            'hours': course['hours'],
            'detailedDescription': course['detailedDescription'],
            'university': course['university'],
            'startDate': course['startDate']
        }
        paginated_courses.append(paginated_course)

    return {
        "success": True,
        'courses': paginated_courses,
        "pagination": {
            "currentPage": 1,
            "totalPages": 1,
            "totalItems": len(sliced_courses)
        }
    }

# 2.3 获取首页的课程列表
@app.route('/api/course/home', methods=['POST'])
def get_home_courses():
    data = request.get_json()

    # 获取所有课程ID列表
    course_ids = list(courses.keys())
    # 确保列表不会超出范围
    course_ids = course_ids[0:4]

    # 根据课程ID获取课程详细信息
    sliced_courses = []
    for course_id in course_ids:
        course = courses.get(course_id)
        if course:
            sliced_course = {
                'courseId': course.get('courseId'),
                'courseName': course.get('courseName'),
                'teacherName': course.get('teacherName'),
                'teacherId': course.get('teacherId'),
                'summary': course.get('summary', ''),
                'publishedDate': course.get('publishedDate'),
                'isRecommended': course.get('isRecommended'),
                'numberOfStudents': course.get('numberOfStudents'),
                'imageUrl': course.get('imageUrl', ''),
                'credit': course.get('credit', 0),
                'hours': course.get('hours', 0),
                'detailedDescription': course.get('detailedDescription', ''),
                'university': course.get('university', ''),
                'startDate': course.get('startDate')
            }
            sliced_courses.append(sliced_course)

    return {
        "success": True,
        'courses': sliced_courses,
        "pagination": {
            "currentPage": 1,
            "totalPages": 1,
            "totalItems": len(sliced_courses)
        }
    }

# 2.2 学生选课接口
@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    student_id = data.get('studentId')
    course_id = data.get('courseId')

    if not users.get(student_id):
        return jsonify({"success": False, "message": "学生不存在"})

    if not courses.get(course_id):
        return jsonify({"success": False, "message": "课程不存在"})

    if enrollments.get(student_id) and course_id in enrollments.get(student_id):
        return jsonify({"success": False, "message": "已选过该课程"})

    # 添加选课记录
    if not enrollments.get(student_id):
        enrollments[student_id] = []
    enrollments[student_id].append(course_id)
    courses[course_id]['numberOfStudents'] += 1

    # 如果课程有作业，自动补充作业
    for assignment_id, assignment in assignments.items():
        if assignment['courseId'] == course_id:
            if not homeworks.get(assignment_id):
                homeworks[assignment_id] = []
            hw = {
                "studentId": student_id,
                "teacherId": assignment['teacherId'],
                "courseId": course_id,
                "submitted": False,
                "grade": None,
                "fileUrl": None,
                "additionalNotes": None,
                "submissionDate": None,
                "feedback": None,
                "gradeDate": None,
                "graded": False
            }
            homeworks[assignment_id].append(hw)

    save_db(db)
    return jsonify({"success": True, "message": "选课成功"})

# 2.3 教师发布课程接口
@app.route('/publish-course', methods=['POST'])
def publish_course():
    data = request.get_json()
    teacher_id = data.get('teacherId')
    course = data.get('course')
    # 生成10位课程ID
    courseId = generate_hash(course.get('courseName'))

    courses[courseId] = {
        "courseId": courseId,
        "courseName": course.get('courseName'),
        "teacherName": teachers.get(teacher_id).get('teacherName'),
        "teacherId": teacher_id,
        "summary": course.get('summary'),
        "publishedDate": getDate(),
        "imageUrl": None,
        # 课程对应的路径
        "coursePath": course.get('courseMaterialPath'),
        # 默认未推荐
        "isRecommended": course.get('isRecommended'),
        # 选课人数为0，点赞人数为0
        "numberOfStudents": 0,
        "likes": 0,
        "credit": 0,
        "hours": 0,
        "detailedDescription":  None,
        "university": None,
        "startDate": getDate()
    }

    save_db(db)  # 保存更新到文件
    return jsonify({"success": True, "message": "课程发布成功", "courseId": courseId})

# 2.4 学生查看课程详情
@app.route('/api/course/<id>', methods=['POST'])
def get_course_detail():
    data = request.get_json()
    student_id = data.get('userId')
    course_id = data.get('courseId')

    if not users[student_id]:
        return jsonify({"success": False, "message": "用户不存在"})

    if users[student_id]['userType'] != 'student':
        return jsonify({"success": False, "message": "不是学生，无权查看课程详情"})

    course = courses.get(course_id)
    return jsonify({
        "success": True,
        "message": "查询成功",
        "course": {
            "courseId": course['courseId'],
            "courseName": course['courseName'],
            "teacherName": course['teacherName'],
            "teacherId": course['teacherId'],
            "summary": course['summary'],
            "publishedDate": course['publishedDate'],
            "isRecommended": course['isRecommended'],
            "numberOfStudents": course['numberOfStudents'],
            "imageUrl": course['imageUrl'],
            "credit": course['credit'],
            "hours": course['hours'],
            "detailedDescription": course['detailedDescription'],
            "university": course['university'],
            "startDate": course['startDate']
            }
        })

# 3.1教师发布作业
@app.route('/publish-assignment', methods=['POST'])
def publish_assignment():
    data = request.get_json()
    teacher_id = data.get('teacherId')
    course_id = data.get('courseId')
    assignment = data.get('assignment')

    assignment_id = generate_hash(assignment.get('name'))

    # 作业发布成功，初始化作业信息
    assignments[assignment_id] = {
        "assignmentId": assignment_id,
        "name": assignment.get('name'),
        "teacherId": teacher_id,
        "courseId": course_id,
        "description": assignment.get('description'),
        "deadline": assignment.get('deadline'),
        # 作业总人数为0
        "totalSubmissions": courses[course_id]['numberOfStudents'],
        # 已提交人数为0
        "submitted": 0,
    }

    if not homeworks.get(assignment_id):
        homeworks[assignment_id] = []

    # 选课学生的作业更新
    for studentid, course in enrollments.items():
        if course_id in course:
            if not homeworks.get(assignment_id):
                homeworks[assignment_id] = []
            hw = {
                "studentId": studentid,
                "teacherId": teacher_id,
                "courseId": course_id,
                "submitted": False,
                "grade": None,
                "fileUrl": None,
                "additionalNotes": None,
                "submissionDate": None,
                "feedback": None,
                "gradeDate": None,
                "graded": False
            }
            homeworks[assignment_id].append(hw)

    save_db(db)
    return jsonify({
        "success": True,
        "message": "作业发布成功",
        "assignmentId": assignment_id
    })

# 3.2学生提交作业
@app.route('/submit-assignment', methods=['POST'])
def submit_assignment():
    data = request.get_json()
    student_id = data.get('studentId')
    assignment_id = data.get('assignmentId')
    submission_data = data.get('submission')

    # 实现作业的提交
    for hw in homeworks.get(assignment_id, []):
        if hw["studentId"] == student_id:
            hw["fileUrl"] = submission_data['fileUrl']
            hw["additionalNotes"] = submission_data['additionalNotes']
            hw["submitted"] = True  # 假设上传文件后，将作业标记为已提交
            hw["submissionDate"] = getDate()

    save_db(db)
    return jsonify({
        "success": True,
        "message": "作业提交成功"
    })

# 3.3老师批改作业
@app.route('/grade-assignment', methods=['POST'])
def grade_assignment():
    data = request.get_json()
    teacher_id = data.get('teacherId')
    assignment_id = data.get('assignmentId')
    grades_data = data.get('grades')

    if not assignments.get(assignment_id):
        return jsonify({
            "success": False,
            "message": "作业未找到"
        })

    if assignments[assignment_id]['teacherId'] != teacher_id:
        return jsonify({
            "success": False,
            "message": "您未开设此课程，无权批改该作业"
        })

    # 批改作业
    for hw in homeworks.get(assignment_id, []):
        if hw["teacherId"] == teacher_id:
            for grade in grades_data:
                if hw["studentId"] == grade['studentId']:
                    hw["grade"] = grade['score']
                    hw["feedback"] = grade['feedback']
                    hw["gradeDate"] = getDate()
                    hw["graded"] = True

    save_db(db)
    return jsonify({
        "success": True,
        "message": "作业批改完成"
    })

# 3.4查看作业
@app.route('/get-assignments', methods=['POST'])
def get_assignments():
    data = request.get_json()
    user_id = data.get('userId')

    if not users.get(user_id):
        return jsonify({
            "success": False,
            "message": "用户不存在"
        })

    # 返回学生所有的作业
    if users[user_id]['userType'] == 'student':
        all_hws = []
        for assignmentid, hws in homeworks.items():
            for hw in hws:
                if hw['studentId'] == user_id:
                    all_hws.append(hw)
        return jsonify({
            "success": True,
            "message": "查询成功",
            "homeworks": all_hws
        })

    # 返回教师发布的所有作业
    if users[user_id]['userType'] == 'teacher':
        all_hws = []
        for assignmentid, hw in assignments.items():
            if hw['teacherId'] == user_id:
                all_hws.append(hw)
        return jsonify({
            "success": True,
            "message": "查询成功",
            "assignments": all_hws
        })


# 4.1 推荐课程
@app.route('/recommend-course', methods=['POST'])
def recommend_course():
    data = request.get_json()
    admin_id = data.get('adminId')
    course_id = data.get('courseId')
    is_recommended = data.get('isRecommended')

    if not administrators.get(admin_id):
        return jsonify({
            "success": False,
            "message": "不是管理员，没有管理员权限"
        })

    if not courses.get(course_id):
        return jsonify({
            "success": False,
            "message": "课程未找到"
        })

    # 设置为推荐课程
    course = courses[course_id]
    course['isRecommended'] = is_recommended

    save_db(db)
    return jsonify({
        "success": True,
        "message": "课程已推荐"
    })


# 4.2 冻结用户
@app.route('/freeze-user', methods=['POST'])
def freeze_user():
    data = request.get_json()
    admin_id = data.get('adminId')
    user_id = data.get('userId')
    reason = data.get('reason')

    if not administrators.get(admin_id):
        return jsonify({
            "success": False,
            "message": "不是管理员，没有管理员权限"
        })

    if user_id not in users:
        return jsonify({
            "success": False,
            "message": "用户未找到"
        })


    user = users.get(user_id)
    user['status'] = '禁用'
    user['freezeReason'] = reason

    save_db(db)
    return jsonify({
        "success": True,
        "message": "用户已冻结"
    })

# 5.1 获取题库
@app.route('/api/questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    user_id = data.get('userId')
    course_id = data.get('courseId')

    if not users.get(user_id):
        return jsonify({
            "success": False,
            "message": "用户不存在"
        })

    if not courses.get(course_id):
        return jsonify({
            "success": False,
            "message": "课程不存在"
        })


    ret_ques = []
    for ques, q in questions.items():
        if course_id == ques:
            # 每次返回10道题目
            random_ints = random.sample(range(0, len(q)), 10)
            for i in range(10):
                ret_ques.append(q[random_ints[i]])

    return jsonify({
        "success": True,
        "message": "查询成功",
        "courseId": course_id,
        "questions": ret_ques,
        "questionsCount": len(ret_ques)
    })

if __name__ == '__main__':
    app.run(port=5000)
