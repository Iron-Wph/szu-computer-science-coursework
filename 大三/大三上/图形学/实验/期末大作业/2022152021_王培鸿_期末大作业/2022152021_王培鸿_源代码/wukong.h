#pragma once
#include "TriMesh.h"

#include "stb_image.h"
#include "Camera.h"
#include "MatrixStack.h"
#include "openGLObject.h"

enum WuKong_Movement {
	FOR, BACK, LEFT, RIGHT, UP, DOWN
};

const float wk_YAW = -90.0f;
const float wk_PITCH = 0.0f;
const float wk_SPEED = 50.0f;
const float wk_SENSITIVITY = 0.1f;
const float wk_ZOOM = 2.0f;

// 是否为运动
bool isMove = false;

struct Robot
{
	// 关节角和菜单选项值
	enum {
		Gun,			// 金箍棒
		Body,			// 身体
		Head,			// 头部
		LeftArm,		// 左臂
		LeftHand,		// 左手
		RightArm,		// 右臂
		RightHand,		// 右手
		LeftThigh,		// 左大腿
		LeftShin,		// 左小腿
		RightThigh,		// 右大腿
		RightShin,		// 右小腿
		LeftFoot,		// 左脚
		RightFoot,		// 右脚
		Cloud			// yun
	};

	// 关节角大小
	GLfloat theta[14] = {
		110.0,    // gun
		-90.0,    // body
		0.0,    // head
		0.0,    // leftArm
		0.0,    // leftHand
		0.0,    // rightArm
		0.0,    // rightHand
		0.0,    // leftThigh
		0.0,    // leftShin
		0.0,    // rightThigh
		0.0,	// rightShin
		0.0,	// leftFoot
		0.0,	// rightFoot
		90.0     // yun
	};
};
Robot robot;
// 被选中的物体
int Selected_mesh = robot.Body;

struct wukong{
	// 相机的位置
	glm::vec3 Position;
	// 相机的方向
	glm::vec3 Front;
	// 相机的上轴
	glm::vec3 Up;
	// 相机的右轴
	glm::vec3 Right;
	glm::vec3 WorldUp;
	// euler Angles
	float Yaw;
	float Pitch;
	// camera options
	float MovementSpeed;
	float MouseSensitivity;
	// 金箍棒的缩放参数
	glm::vec3 kpscale = glm::vec3(1.0, 2.0, 1.0);
	glm::vec3 kptraslate = glm::vec3(0.08, -0.25, -0.04);
	// 是否召唤筋斗云
	bool yun = false;

	// 投影参数
	float zNear = 0.1;
	float zFar = 100.0;
	// 透视投影参数
	float Zoom;         // 等价于视野域
	float aspect = 1.0;
	// 正交投影参数
	float scale = 1.5;

	// 模视矩阵
	glm::mat4 viewMatrix;
	glm::mat4 projMatrix;


	// 模型
	TriMesh* gun;
	TriMesh* head;
	TriMesh* body;
	TriMesh* leftArm;
	TriMesh* leftHand;
	TriMesh* rightArm;
	TriMesh* rightHand;
	TriMesh* leftThigh;
	TriMesh* leftShin;
	TriMesh* rightThigh;
	TriMesh* rightShin;
	TriMesh* leftFoot;
	TriMesh* rightFoot;
	TriMesh* cloud;

	// 
	openGLObject *gunObject;
	openGLObject *headObject;
	openGLObject *bodyObject;
	openGLObject *leftArmObject;
	openGLObject *leftHandObject;
	openGLObject *rightArmObject;
	openGLObject *rightHandObject;
	openGLObject *leftThighObject;
	openGLObject *leftShinObject;
	openGLObject *rightThighObject;
	openGLObject *rightShinObject;
	openGLObject *leftFootObject;
	openGLObject *rightFootObject;
	openGLObject *cloudObject;

	void load_texture_STBImage(const std::string& file_name, GLuint& texture) {
		// 读取纹理图片，并将其传递给着色器
		int width, height, channels = 0;
		unsigned char* pixels = NULL;
		// 读取图片的时候先翻转一下图片，如果不设置的话显示出来是反过来的图片
		stbi_set_flip_vertically_on_load(true);
		// 读取图片数据
		pixels = stbi_load(file_name.c_str(), &width, &height, &channels, 0);

		// 调整行对齐格式
		if (width * channels % 4 != 0)
			glPixelStorei(GL_UNPACK_ALIGNMENT, 1);
		GLenum format = GL_RGB;
		// 设置通道格式
		switch (channels)
		{
		case 1:
			format = GL_RED;
			break;
		case 3:
			format = GL_RGB;
			break;
		case 4:
			format = GL_RGBA;
			break;
		default:
			format = GL_RGB;
			break;
		}

		// 绑定纹理对象
		glBindTexture(GL_TEXTURE_2D, texture);

		// 指定纹理的放大，缩小滤波，使用线性方式，即当图片放大的时候插值方式
		// 将图片的rgb数据上传给opengl
		glTexImage2D(
			GL_TEXTURE_2D,    // 指定目标纹理，这个值必须是GL_TEXTURE_2D
			0,                // 执行细节级别，0是最基本的图像级别，n表示第N级贴图细化级别
			format,           // 纹理数据的颜色格式(GPU显存)
			width,            // 宽度。早期的显卡不支持不规则的纹理，则宽度和高度必须是2^n
			height,           // 高度。早期的显卡不支持不规则的纹理，则宽度和高度必须是2^n
			0,                // 指定边框的宽度。必须为0
			format,           // 像素数据的颜色格式(CPU内存)
			GL_UNSIGNED_BYTE, // 指定像素数据的数据类型
			pixels            // 指定内存中指向图像数据的指针
		);

		// 生成多级渐远纹理，多消耗1/3的显存，较小分辨率时获得更好的效果
		// glGenerateMipmap(GL_TEXTURE_2D);

		// 指定插值方法
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);

		// 恢复初始对齐格式
		glPixelStorei(GL_UNPACK_ALIGNMENT, 4);
		// 释放图形内存
		stbi_image_free(pixels);
	};

	void bindObjectAndData(TriMesh* mesh, openGLObject& object, const std::string& texture_image, const std::string& vshader, const std::string& fshader) {
		// 初始化各种对象
		std::vector<glm::vec3> points = mesh->getPoints();
		std::vector<glm::vec3> normals = mesh->getNormals();
		std::vector<glm::vec3> colors = mesh->getColors();
		std::vector<glm::vec2> textures = mesh->getTextures();

		// 创建顶点数组对象
		#ifdef __APPLE__	// for MacOS
			glGenVertexArraysAPPLE(1, &object.vao);		// 分配1个顶点数组对象
			glBindVertexArrayAPPLE(object.vao);		// 绑定顶点数组对象
		#else				// for Windows
			glGenVertexArrays(1, &object.vao);  	// 分配1个顶点数组对象
			glBindVertexArray(object.vao);  	// 绑定顶点数组对象
		#endif

		// 创建并初始化顶点缓存对象
		glGenBuffers(1, &object.vbo);
		glBindBuffer(GL_ARRAY_BUFFER, object.vbo);
		glBufferData(GL_ARRAY_BUFFER,
			points.size() * sizeof(glm::vec3) +
			normals.size() * sizeof(glm::vec3) +
			colors.size() * sizeof(glm::vec3) +
			textures.size() * sizeof(glm::vec2),
			NULL, GL_STATIC_DRAW);

		// 绑定顶点数据
		glBufferSubData(GL_ARRAY_BUFFER, 0, points.size() * sizeof(glm::vec3), points.data());
		// 绑定颜色数据
		glBufferSubData(GL_ARRAY_BUFFER, points.size() * sizeof(glm::vec3), colors.size() * sizeof(glm::vec3), colors.data());
		// 绑定法向量数据
		glBufferSubData(GL_ARRAY_BUFFER, (points.size() + colors.size()) * sizeof(glm::vec3), normals.size() * sizeof(glm::vec3), normals.data());
		// 绑定纹理数据
		glBufferSubData(GL_ARRAY_BUFFER, (points.size() + normals.size() + colors.size()) * sizeof(glm::vec3), textures.size() * sizeof(glm::vec2), textures.data());

		object.vshader = vshader;
		object.fshader = fshader;
		object.program = InitShader(object.vshader.c_str(), object.fshader.c_str());

		// 将顶点传入着色器
		object.pLocation = glGetAttribLocation(object.program, "vPosition");
		glEnableVertexAttribArray(object.pLocation);
		glVertexAttribPointer(object.pLocation, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(0));

		// 将颜色传入着色器
		object.cLocation = glGetAttribLocation(object.program, "vColor");
		glEnableVertexAttribArray(object.cLocation);
		glVertexAttribPointer(object.cLocation, 3, GL_FLOAT, GL_FALSE, 0, BUFFER_OFFSET(points.size() * sizeof(glm::vec3)));

		// 将法向量传入着色器
		object.nLocation = glGetAttribLocation(object.program, "vNormal");
		glEnableVertexAttribArray(object.nLocation);
		glVertexAttribPointer(object.nLocation, 3,
			GL_FLOAT, GL_FALSE, 0,
			BUFFER_OFFSET((points.size() + colors.size()) * sizeof(glm::vec3)));

		object.tLocation = glGetAttribLocation(object.program, "vTexture");
		glEnableVertexAttribArray(object.tLocation);
		glVertexAttribPointer(object.tLocation, 2,
			GL_FLOAT, GL_FALSE, 0,
			BUFFER_OFFSET((points.size() + colors.size() + normals.size()) * sizeof(glm::vec3)));


		// 获得矩阵位置
		object.modelLocation = glGetUniformLocation(object.program, "model");
		object.viewLocation = glGetUniformLocation(object.program, "view");
		object.projectionLocation = glGetUniformLocation(object.program, "projection");

		object.shadowLocation = glGetUniformLocation(object.program, "isShadow");

		// 读取纹理图片数
		object.texture_image = texture_image;
		// 创建纹理的缓存对象
		glGenTextures(1, &object.texture);
		// 调用stb_image生成纹理
		load_texture_STBImage(object.texture_image, object.texture);

		// Clean up
		glUseProgram(0);
		#ifdef __APPLE__
			glBindVertexArrayAPPLE(0);
		#else
			glBindVertexArray(0);
		#endif

	};

	void bindLightAndMaterial(TriMesh* mesh, openGLObject& object, Light* light, Camera* camera) {
		// 传递材质、光源等数据给着色器

		glUniform3fv(glGetUniformLocation(object.program, "eye_position"), 1, &camera->Position[0]);

		// 传递物体的材质
		glm::vec4 meshAmbient = mesh->getAmbient();
		glm::vec4 meshDiffuse = mesh->getDiffuse();
		glm::vec4 meshSpecular = mesh->getSpecular();
		float meshShininess = mesh->getShininess();

		glUniform4fv(glGetUniformLocation(object.program, "material.ambient"), 1, &meshAmbient[0]);
		glUniform4fv(glGetUniformLocation(object.program, "material.diffuse"), 1, &meshDiffuse[0]);
		glUniform4fv(glGetUniformLocation(object.program, "material.specular"), 1, &meshSpecular[0]);
		glUniform1f(glGetUniformLocation(object.program, "material.shininess"), meshShininess);


		// 传递光源信息
		glm::vec4 lightAmbient = light->getAmbient();
		glm::vec4 lightDiffuse = light->getDiffuse();
		glm::vec4 lightSpecular = light->getSpecular();
		glm::vec3 lightPosition = light->getTranslation();
		glUniform4fv(glGetUniformLocation(object.program, "light.ambient"), 1, &lightAmbient[0]);
		glUniform4fv(glGetUniformLocation(object.program, "light.diffuse"), 1, &lightDiffuse[0]);
		glUniform4fv(glGetUniformLocation(object.program, "light.specular"), 1, &lightSpecular[0]);
		glUniform3fv(glGetUniformLocation(object.program, "light.position"), 1, &lightPosition[0]);

		glUniform1f(glGetUniformLocation(object.program, "light.constant"), light->getConstant());
		glUniform1f(glGetUniformLocation(object.program, "light.linear"), light->getLinear());
		glUniform1f(glGetUniformLocation(object.program, "light.quadratic"), light->getQuadratic());

	}

	// 加载模型文件
	void init() {
		std::string vshader, fshader;
		// 读取着色器并使用
		#ifdef __APPLE__	// for MacOS
			vshader = "shaders/vshader_mac.glsl";
			fshader = "shaders/fshader_mac.glsl";
		#else				// for Windows
			vshader = "shaders/vshader_win.glsl";
			fshader = "shaders/fshader_win.glsl";
		#endif

		this->gunObject = new openGLObject();
		this->headObject = new openGLObject();
		this->bodyObject = new openGLObject();
		this->leftArmObject = new openGLObject();
		this->leftHandObject = new openGLObject();
		this->rightArmObject = new openGLObject();
		this->rightHandObject = new openGLObject();
		this->leftThighObject = new openGLObject();
		this->leftShinObject = new openGLObject();
		this->rightThighObject = new openGLObject();
		this->rightShinObject = new openGLObject();
		this->leftFootObject = new openGLObject();
		this->rightFootObject = new openGLObject();
		this->cloudObject = new openGLObject();

		// 筋斗云
		this->cloud = new TriMesh();
		this->cloud->setNormalize(true);
		this->cloud->readObj("./assets/cloud/cloud.obj");
		//
		this->cloud->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->cloud->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->cloud->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->cloud->setShininess(10.0f);
		bindObjectAndData(this->cloud, *this->cloudObject, "./assets/cloud/cloud.png", vshader, fshader);

		// 金箍棒
		std::string str = "kingp";
		this->gun = new TriMesh();
		this->gun->setNormalize(true);
		this->gun->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->gun->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->gun->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->gun->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->gun->setShininess(10.0f);
		bindObjectAndData(this->gun, *this->gunObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 头部
		str = "head";
		this->head = new TriMesh();
		this->head->setNormalize(true);
		this->head->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->head->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->head->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->head->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->head->setShininess(10.0f);
		bindObjectAndData(this->head, *this->headObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 躯干
		str = "body";
		this->body = new TriMesh();
		this->body->setNormalize(true);
		this->body->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->body->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->body->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->body->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->body->setShininess(10.0f);
		// 设置物体的旋转位移
		this->body->setTranslation(glm::vec3(0.0, 0.7, 0.0));
		bindObjectAndData(this->body, *this->bodyObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 左臂
		str = "leftArm";
		this->leftArm = new TriMesh();
		this->leftArm->setNormalize(true);
		this->leftArm->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->leftArm->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->leftArm->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->leftArm->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->leftArm->setShininess(10.0f);
		bindObjectAndData(this->leftArm, *this->leftArmObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 左手
		str = "lefthand";
		this->leftHand = new TriMesh();
		this->leftHand->setNormalize(true);
		this->leftHand->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->leftHand->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->leftHand->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->leftHand->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->leftHand->setShininess(10.0f);
		bindObjectAndData(this->leftHand, *this->leftHandObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 右臂
		str = "rightArm";
		this->rightArm = new TriMesh();
		this->rightArm->setNormalize(true);
		this->rightArm->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->rightArm->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->rightArm->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->rightArm->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->rightArm->setShininess(10.0f);
		bindObjectAndData(this->rightArm, *this->rightArmObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 右手
		str = "righthand";
		this->rightHand = new TriMesh();
		this->rightHand->setNormalize(true);
		this->rightHand->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->rightHand->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->rightHand->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->rightHand->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->rightHand->setShininess(10.0f);
		bindObjectAndData(this->rightHand, *this->rightHandObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 左大腿
		str = "thigh";
		this->leftThigh = new TriMesh();
		this->leftThigh->setNormalize(true);
		this->leftThigh->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->leftThigh->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->leftThigh->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->leftThigh->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->leftThigh->setShininess(10.0f);
		bindObjectAndData(this->leftThigh, *this->leftThighObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 左小腿
		str = "shin";
		this->leftShin = new TriMesh();
		this->leftShin->setNormalize(true);
		this->leftShin->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->leftShin->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->leftShin->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->leftShin->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->leftShin->setShininess(10.0f);
		bindObjectAndData(this->leftShin, *this->leftShinObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 右大腿
		str = "thigh";
		this->rightThigh = new TriMesh();
		this->rightThigh->setNormalize(true);
		this->rightThigh->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->rightThigh->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->rightThigh->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->rightThigh->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->rightThigh->setShininess(10.0f);
		bindObjectAndData(this->rightThigh, *this->rightThighObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 右小腿
		str = "shin";
		this->rightShin = new TriMesh();
		this->rightShin->setNormalize(true);
		this->rightShin->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->rightShin->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->rightShin->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->rightShin->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->rightShin->setShininess(10.0f);
		bindObjectAndData(this->rightShin, *this->rightShinObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 左脚
		str = "foot";
		this->leftFoot = new TriMesh();
		this->leftFoot->setNormalize(true);
		this->leftFoot->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->leftFoot->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->leftFoot->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->leftFoot->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->leftFoot->setShininess(10.0f);
		bindObjectAndData(this->leftFoot, *this->leftFootObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);

		// 右脚
		str = "foot";
		this->rightFoot = new TriMesh();
		this->rightFoot->setNormalize(true);
		this->rightFoot->readObj("./assets/wukong/" + str + "/" + str + ".obj");
		//
		this->rightFoot->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
		this->rightFoot->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
		this->rightFoot->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
		this->rightFoot->setShininess(10.0f);
		bindObjectAndData(this->rightFoot, *this->rightFootObject, "./assets/wukong/" + str + "/" + str + ".png", vshader, fshader);
	}

	// 显示
	void drawMesh(glm::mat4 modelMatrix, TriMesh* mesh, openGLObject& object, Light* light, Camera* camera, bool projMode) {
		camera->updateCameraVectors();
		camera->viewMatrix = camera->getViewMatrix();
		camera->projMatrix = camera->getProjectionMatrix(projMode);

		#ifdef __APPLE__	// for MacOS
			glBindVertexArrayAPPLE(object.vao);
		#else	
			glBindVertexArray(object.vao);
		#endif
			glUseProgram(object.program);

		// 传递矩阵
		glUniformMatrix4fv(object.modelLocation, 1, GL_FALSE, &modelMatrix[0][0]);
		glUniformMatrix4fv(object.viewLocation, 1, GL_FALSE, &camera->viewMatrix[0][0]);
		glUniformMatrix4fv(object.projectionLocation, 1, GL_FALSE, &camera->projMatrix[0][0]);
		// 将着色器 isShadow 设置为0，表示正常绘制的颜色，如果是1着表示阴影
		glUniform1i(object.shadowLocation, 0);

		glActiveTexture(GL_TEXTURE0);
		glBindTexture(GL_TEXTURE_2D, object.texture);// 该语句必须，否则将只使用同一个纹理进行绘制
		// 传递纹理数据 将生成的纹理传给shader
		glUniform1i(glGetUniformLocation(object.program, "texture"), 0);

		// 将材质和光源数据传递给着色器
		bindLightAndMaterial(mesh, object, light, camera);
		// 绘制
		glDrawArrays(GL_TRIANGLES, 0, mesh->getPoints().size());

		// 绘制阴影
		modelMatrix = light->getShadowProjectionMatrix() * modelMatrix;

		// 传递 isShadow 变量。
		glUniform1i(object.shadowLocation, 1);
		// 传递 unifrom 关键字的矩阵数据。
		glUniformMatrix4fv(object.modelLocation, 1, GL_FALSE, &modelMatrix[0][0]);
		glUniformMatrix4fv(object.viewLocation, 1, GL_FALSE, &camera->viewMatrix[0][0]);
		glUniformMatrix4fv(object.projectionLocation, 1, GL_FALSE, &camera->projMatrix[0][0]);
		// 绘制
		glDrawArrays(GL_TRIANGLES, 0, mesh->getPoints().size());

		#ifdef __APPLE__	// for MacOS
			glBindVertexArrayAPPLE(0);
		#else
			glBindVertexArray(0);
		#endif
			glUseProgram(0);
	};

	// 每个部件的显示
	// 筋斗云
	void Cloud(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, 0.0, 0.0));
		instance = glm::scale(instance, glm::vec3(2.5, 2.5, 2.5));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->cloud, *this->cloudObject, light, camera, projMode);
	}

	// 躯干
	void Body(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, 0.0, 0.0));
		instance = glm::scale(instance, glm::vec3(1.0, 1.0, 1.0));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->body, *this->bodyObject, light, camera, projMode);
	}

	// 头部
	void Head(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode)
	{
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(-0.25, 0.53, 0.015));
		instance = glm::scale(instance, glm::vec3(1.0, 1.0, 1.0));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->head, *this->headObject, light, camera, projMode);
	}

	// 左臂
	void LeftArm(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.08, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->leftArm, *this->leftArmObject, light, camera, projMode);
	}

	// 左手
	void LeftHand(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.12, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->leftHand , *this->leftHandObject, light, camera, projMode);
	}

	// 右臂
	void RightArm(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.10, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->rightArm, *this->rightArmObject, light, camera, projMode);
	}

	// 右手
	void RightHand(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.12, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->rightHand, *this->rightHandObject, light, camera, projMode);
	}

	// 左大腿
	void LeftThigh(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.10, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->leftThigh, *this->leftThighObject, light, camera, projMode);
	}

	// 左小腿
	void LeftShin(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.08, 0.0));
		instance = glm::scale(instance, glm::vec3(0.2, 0.3, 0.2));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->leftShin, *this->leftShinObject, light, camera, projMode);
	}

	// 左脚
	void LeftFoot(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(-0.04, -0.05, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->leftFoot, *this->leftFootObject, light, camera, projMode);
	}

	// 右大腿
	void RightThigh(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.10, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->rightThigh, *this->rightThighObject, light, camera, projMode);
	}

	// 右小腿
	void RightShin(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, -0.08, 0.0));
		instance = glm::scale(instance, glm::vec3(0.2, 0.3, 0.2));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->rightShin, *this->rightShinObject, light, camera, projMode);
	}

	// 右脚
	void RightFoot(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(-0.04, -0.05, 0.0));
		instance = glm::scale(instance, glm::vec3(0.3, 0.4, 0.3));
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->rightFoot, *this->rightFootObject, light, camera, projMode);
	}

	// 金箍棒
	void KingP(glm::mat4 modelMatrix, Light* light, Camera* camera, bool projMode) {
		// 本节点局部变换矩阵
		glm::mat4 instance = glm::mat4(1.0);
		instance = glm::translate(instance, glm::vec3(0.0, 0.0, 0.0));
		instance = glm::scale(instance, kpscale);
		// 乘以来自父物体的模型变换矩阵，绘制当前物体
		drawMesh(modelMatrix * instance, this->gun, *this->gunObject, light, camera, projMode);
	}

	void show(Light* light, Camera* camera, bool projMode) {
		// 物体的变换矩阵
		glm::mat4 modelMatrix = glm::mat4(1.0);

		// 保持变换矩阵的栈
		MatrixStack mstack;
		float delta = cos(glfwGetTime() * 40.0 / 7.5) * 40;

		// 躯干
		modelMatrix = glm::translate(modelMatrix, this->body->getTranslation());
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.Body]), glm::vec3(0.0, 1.0, 0.0));
		Body(modelMatrix, light, camera, projMode);

		mstack.push(modelMatrix); // 保存躯干变换矩阵
		// 头部
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, 0.0, 0.0));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.Head]), glm::vec3(0.0, 1.0, 0.0));
		Head(modelMatrix, light, camera, projMode);
		modelMatrix = mstack.pop(); // 恢复躯干变换矩阵

		// 左臂
		mstack.push(modelMatrix);   // 保存躯干变换矩阵
		// 这里我们希望机器人的左臂只绕Z轴旋转，所以只计算了RotateZ
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, 0.20, -0.19));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.LeftArm]), glm::vec3(0.0, 0.0, 1.0));
		LeftArm(modelMatrix, light, camera, projMode);

		// 左手
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.20, -0.04));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.LeftHand]), glm::vec3(1.0, 0.0, 0.0));
		LeftHand(modelMatrix, light, camera, projMode);

		// 金箍棒
		modelMatrix = glm::translate(modelMatrix, kptraslate);
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.Gun]), glm::vec3(0.0, 0.0, 1.0));
		KingP(modelMatrix, light, camera, projMode);

		modelMatrix = mstack.pop(); // 恢复躯干变换矩阵V

		// 筋斗云
		if (yun) {
			mstack.push(modelMatrix);   // 保存躯干变换矩阵
			modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.7, 0.0));
			modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.Cloud]), glm::vec3(0.0, 1.0, 0.0));
			Cloud(modelMatrix, light, camera, projMode);
			modelMatrix = mstack.pop();
		}

		// 右臂
		mstack.push(modelMatrix);   // 保存躯干变换矩阵
		// 这里我们希望机器人的右臂只绕Z轴旋转，所以只计算了RotateZ
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, 0.22, 0.19));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(isMove ? robot.theta[robot.RightArm] - delta: robot.theta[robot.RightArm]), glm::vec3(0.0, 0.0, 1.0));
		RightArm(modelMatrix, light, camera, projMode);

		// 右手
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.23, 0.04));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.RightHand]), glm::vec3(1.0, 0.0, 0.0));
		RightHand(modelMatrix, light, camera, projMode);

		modelMatrix = mstack.pop(); // 恢复躯干变换矩阵V

		mstack.push(modelMatrix);   // 保存躯干变换矩阵
		// 左大腿
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.05, -0.15, -0.09));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(isMove ? robot.theta[robot.LeftThigh] - delta - 10 : robot.theta[robot.LeftThigh]), glm::vec3(0.0, 0.0, 1.0));
		LeftThigh(modelMatrix, light, camera, projMode);

		// 左小腿
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.25, 0.0));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.LeftShin]), glm::vec3(0.0, 0.0, 1.0));
		LeftShin(modelMatrix, light, camera, projMode);

		// 左脚 
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.19, 0.0));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.LeftFoot]), glm::vec3(0.0, 0.0, 1.0));
		LeftFoot(modelMatrix, light, camera, projMode);

		modelMatrix = mstack.pop(); // 恢复躯干变换矩阵V

		mstack.push(modelMatrix);   // 保存躯干变换矩阵
		// 右大腿
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.05, -0.15, 0.09));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(isMove ? -1 * (robot.theta[robot.RightThigh] - delta - 10) : robot.theta[robot.RightThigh]), glm::vec3(0.0, 0.0, 1.0));
		RightThigh(modelMatrix, light, camera, projMode);

		// 右小腿
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.25, 0.0));
		modelMatrix = glm::rotate(modelMatrix, glm::radians( robot.theta[robot.RightShin]), glm::vec3(0.0, 0.0, 1.0));
		RightShin(modelMatrix, light, camera, projMode);

		// 右脚 
		modelMatrix = glm::translate(modelMatrix, glm::vec3(0.0, -0.19, 0.0));
		modelMatrix = glm::rotate(modelMatrix, glm::radians(robot.theta[robot.RightFoot]), glm::vec3(0.0, 0.0, 1.0));
		RightFoot(modelMatrix, light, camera, projMode);

		modelMatrix = mstack.pop(); // 恢复躯干变换矩阵V
	}

	// 相机视角
	// constructor with vectors
	wukong(glm::vec3 position = glm::vec3(0.0f, 0.0f, 0.0f),
		glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f),
		float yaw = wk_YAW,
		float pitch = wk_PITCH)
		: Front(glm::vec3(0.0f, 0.0f, -1.0f)),
		MovementSpeed(wk_SPEED),
		MouseSensitivity(wk_SENSITIVITY),
		Zoom(wk_ZOOM)
	{
		Position = position;
		WorldUp = up;
		Yaw = yaw;
		Pitch = pitch;
		updateCameraVectors();
	}
	// constructor with scalar values
	wukong(float posX, float posY, float posZ,
		float upX, float upY, float upZ,
		float yaw, float pitch)
		: Front(glm::vec3(0.0f, 0.0f, -1.0f)),
		MovementSpeed(wk_SPEED),
		MouseSensitivity(wk_SENSITIVITY),
		Zoom(wk_ZOOM)
	{
		Position = glm::vec3(posX, posY, posZ);
		WorldUp = glm::vec3(upX, upY, upZ);
		Yaw = yaw;
		Pitch = pitch;
		updateCameraVectors();
	}

	// returns the view matrix calculated using Euler Angles and the LookAt Matrix
	glm::mat4 getViewMatrix() {
		return glm::lookAt(Position, Position + Front, Up);
	}

	// processes input received from any keyboard-like input system. Accepts input parameter in the form of camera defined ENUM (to abstract it from windowing systems)
	void ProcessKeyboard(Camera_Movement direction, float deltaTime) {
		float velocity = MovementSpeed * deltaTime * 0.2;
		glm::vec3 location = this->body->getTranslation();
		if (direction == FOR) // 前移
		{
			robot.theta[robot.Body] = -90.0f;
			this->Yaw = wk_YAW;
			location -= Front * velocity;
			this->body->setTranslation(location);
		}
		if (direction == BACK) // 后移
		{
			this->Yaw = -270.0f;
			robot.theta[robot.Body] = -270.0f;
			location += Front * velocity;
			this->body->setTranslation(location);
		}
		if (direction == LEFT) // 左移
		{
			robot.theta[robot.Body] = -360.0f;
			this->Yaw = -360.0f;
			location += Right * velocity;
			this->body->setTranslation(location);
		}
		if (direction == RIGHT) // 右移
		{
			robot.theta[robot.Body] = -180.0f;
			this->Yaw = -180.0f;
			location -= Right * velocity;
			this->body->setTranslation(location);
		}
		if (direction == UP)  // 上移
		{
			location.y += velocity;
			this->body->setTranslation(location);
		}
		Position.y += velocity;
		if (direction == DOWN)  // 下移
		{
			location.y -= velocity;
			this->body->setTranslation(location);
		}
	}

	// processes input received from a mouse input system. Expects the offset value in both the x and y direction.
	void ProcessMouseMovement(float xoffset, float yoffset, GLboolean constrainPitch = true) {
		xoffset *= MouseSensitivity;
		yoffset *= MouseSensitivity;

		Yaw += xoffset;
		Pitch += yoffset;

		// make sure that when pitch is out of bounds, screen doesn't get flipped
		if (constrainPitch) {
			if (Pitch > 89.0f)
				Pitch = 89.0f;
			if (Pitch < -89.0f)
				Pitch = -89.0f;
		}

		// update Front, Right and Up Vectors using the updated Euler angles
		updateCameraVectors();
	}

	// 处理滚轮输入
	void ProcessMouseScroll(float yoffset) {
		// 滚轮控制摄像机缩放, 视野在 [1.0, 45.0] 范围内
		Zoom -= (float)yoffset;
		if (Zoom < 1.0f)
			Zoom = 1.0f;
		if (Zoom > 45.0f)
			Zoom = 45.0f;
		// 使得正交投影和透视投影都生效
		scale = Zoom;
	}

	// calculates the front vector from the Camera's (updated) Euler Angles
	void updateCameraVectors() {
		// calculate the new Front vector
		glm::vec3 front;
		front.x = cos(glm::radians(Yaw)) * cos(glm::radians(Pitch));
		front.y = sin(glm::radians(Pitch));
		front.z = sin(glm::radians(Yaw)) * cos(glm::radians(Pitch));
		Front = glm::normalize(front);
		// also re-calculate the Right and Up vector
		Right = glm::normalize(glm::cross(Front, WorldUp));  // normalize the vectors, because their length gets closer to 0 the more you look up or down which results in slower movement.
		Up = glm::normalize(glm::cross(Right, Front));
	}

	glm::mat4 getProjectionMatrix(bool isOrtho)
	{
		if (isOrtho) {
			return this->ortho(-Zoom, Zoom, -Zoom, Zoom, this->zNear, this->zFar);
		}
		else {
			return this->perspective(Zoom, aspect, this->zNear, this->zFar);
		}
	}

	// 正交投影矩阵
	glm::mat4 ortho(const GLfloat left, const GLfloat right,
		const GLfloat bottom, const GLfloat top,
		const GLfloat zNear, const GLfloat zFar)
	{
		glm::mat4 c = glm::mat4(1.0f);
		c[0][0] = 2.0 / (right - left);
		c[1][1] = 2.0 / (top - bottom);
		c[2][2] = -2.0 / (zFar - zNear);
		c[3][3] = 1.0;
		c[0][3] = -(right + left) / (right - left);
		c[1][3] = -(top + bottom) / (top - bottom);
		c[2][3] = -(zFar + zNear) / (zFar - zNear);

		c = glm::transpose(c);
		return c;
	}

	// 透视投影矩阵
	glm::mat4 perspective(const GLfloat fovy, const GLfloat aspect,
		const GLfloat zNear, const GLfloat zFar)
	{
		GLfloat top = tan(fovy * M_PI / 180 / 2) * zNear;
		GLfloat right = top * aspect;

		glm::mat4 c = glm::mat4(1.0f);
		c[0][0] = zNear / right;
		c[1][1] = zNear / top;
		c[2][2] = -(zFar + zNear) / (zFar - zNear);
		c[2][3] = -(2.0 * zFar * zNear) / (zFar - zNear);
		c[3][2] = -1.0;
		c[3][3] = 0.0;

		c = glm::transpose(c);
		return c;
	}

	glm::mat4 frustum(const GLfloat left, const GLfloat right,
		const GLfloat bottom, const GLfloat top,
		const GLfloat zNear, const GLfloat zFar)
	{
		// 任意视锥体矩阵
		glm::mat4 c = glm::mat4(1.0f);
		c[0][0] = 2.0 * zNear / (right - left);
		c[0][2] = (right + left) / (right - left);
		c[1][1] = 2.0 * zNear / (top - bottom);
		c[1][2] = (top + bottom) / (top - bottom);
		c[2][2] = -(zFar + zNear) / (zFar - zNear);
		c[2][3] = -2.0 * zFar * zNear / (zFar - zNear);
		c[3][2] = -1.0;
		c[3][3] = 0.0;

		c = glm::transpose(c);
		return c;
	}


	// 恢复默认的动作参数
	void reset() {
		robot.theta[robot.Gun] = 110.0f;
		robot.theta[robot.LeftArm] = 0.0f;
		robot.theta[robot.LeftHand] = 0.0f;
		robot.theta[robot.RightArm] = 0.0f;
		robot.theta[robot.RightHand] = 0.0f;
		robot.theta[robot.LeftThigh] = 0.0f;
		robot.theta[robot.LeftShin] = 0.0f;
		robot.theta[robot.LeftFoot] = 0.0f;
		robot.theta[robot.RightThigh] = 0.0f;
		robot.theta[robot.RightShin] = 0.0f;
		robot.theta[robot.RightFoot] = 0.0f;
	}
};
