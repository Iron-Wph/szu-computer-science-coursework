from flask import Flask, request, jsonify, send_from_directory
import os
import random
import string
from flask_cors import CORS
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 配置上传文件夹
VIDEO_UPLOAD_FOLDER = 'uploads/videos'
IMAGE_UPLOAD_FOLDER = 'uploads/images'
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv'}  # 允许的视频格式
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # 允许的图片格式
app.config['VIDEO_UPLOAD_FOLDER'] = VIDEO_UPLOAD_FOLDER
app.config['IMAGE_UPLOAD_FOLDER'] = IMAGE_UPLOAD_FOLDER

# 确保上传文件夹存在
os.makedirs(VIDEO_UPLOAD_FOLDER, exist_ok=True)
os.makedirs(IMAGE_UPLOAD_FOLDER, exist_ok=True)

# 判断文件扩展名是否合法
def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# 生成随机文件名
def generate_random_filename(filename):
    extension = filename.rsplit('.', 1)[1].lower()
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"{random_str}.{extension}"

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=os.getenv("MOONSHOT_API_KEY"),  # 替换为有效的 API Key
    base_url="https://api.moonshot.cn/v1"
)

@app.route('/get_ai_suggestion', methods=['POST'])
def get_ai_suggestion():
    try:
        # 获取前端发送的课程描述数据
        data = request.json
        course_name = data.get('courseName', '')
        course_description = data.get('description', '')
        course_content = data.get('content', '')
        # 调用 Moonshot API 获取 AI 建议
        completion = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=[ {
                    "role": "system",
                    "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
                },
                {
                    "role": "user",
                    "content": f"你好，AI，请根据以下课程描述给出一些改进建议，检查错字情况：\n课程名称：{course_name}\n课程描述：{course_description}\n课程内容：{course_content} 请不要使用markdown语法文本回答我"
                }],
            temperature=0.3 )
        # 获取 AI 的响应
        ai_response = completion.choices[0].message.content
        return jsonify({"suggestion": ai_response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 上传视频接口
@app.route('/upload_video', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify(errno=1, message='No video file part')

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify(errno=1, message='No selected video file')

    if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
        video_filename = generate_random_filename(video_file.filename)
        video_filepath = os.path.join(app.config['VIDEO_UPLOAD_FOLDER'], video_filename)
        try:
            video_file.save(video_filepath)
            video_url = f"http://127.0.0.1:5008/uploads/videos/{video_filename}"

            return jsonify(errno=0, data={"url": video_url})
        except Exception as e:
            return jsonify(errno=1, message=f"视频文件保存失败: {str(e)}")

    return jsonify(errno=1, message='Invalid video file format')

# 上传图像接口
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify(errno=1, message='No image file part')

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify(errno=1, message='No selected image file')

    if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        image_filename = generate_random_filename(image_file.filename)
        image_filepath = os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], image_filename)
        try:
            image_file.save(image_filepath)
            image_url = f"http://127.0.0.1:5008/uploads/images/{image_filename}"

            return jsonify(errno=0, data={"url": image_url})
        except Exception as e:
            return jsonify(errno=1, message=f"图像文件保存失败: {str(e)}")

    return jsonify(errno=1, message='Invalid image file format')

# 提供静态文件访问
@app.route('/uploads/videos/<filename>')
def uploaded_video_file(filename):
    return send_from_directory(app.config['VIDEO_UPLOAD_FOLDER'], filename)

@app.route('/uploads/images/<filename>')
def uploaded_image_file(filename):
    return send_from_directory(app.config['IMAGE_UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5008)