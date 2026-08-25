#include "Angel.h"
#include "TriMesh.h"
#include "Camera.h"
#include "MeshPainter.h"
#include <vector>
#include <string>
#include <algorithm>
#include "wukong.h"
#include <windows.h>
#include <mmsystem.h>
#pragma execution_character_set("utf-8") 


int WIDTH = 1000;
int HEIGHT = 1000;

int mainWindow;

// 释放技能
bool skills[2] = { false, false};					// 同一时间只能释放一个技能
// 保持按键一直变化
bool cons[6] = { false,false,false,false,false,false };

float lastX = WIDTH / 2.0f, lastY = HEIGHT / 2.0f;  // 上一次焦点的坐标，初始为屏幕中心
bool firstMouse = true;  // 窗口是否是第一次获取焦点

bool projMode = true;	// true为正交投影，false为透视投影

// 视角: 1 为自由摄像机, 2 为悟空
int cameraMode = 1;
// 控制：1为相机，2为悟空
int moveMode = 1;
// 相机切换时使用，使相机灵活切换
glm::vec3 camera_pos;
float camera_yaw = -90.0f;

// 第一个为自由相机，第二个为第三人称
Camera* camera_1 = new Camera();
Camera* camera_2 = new Camera();

Light* light = new Light();
MeshPainter *painter = new MeshPainter();

wukong* wk = new wukong();			// wukong 模型

// 控制摄像机速度的变量
float deltaTime = 0.0f;	 // 当前帧与上一帧的时间差
float lastFrame = 0.0f;  // 上一帧的时间

// 这个用来回收和删除我们创建的物体对象
std::vector<TriMesh *> meshList;
// 加载天空盒
void load_Sky() {
	std::string vshader, fshader;
	// 读取着色器并使用
	#ifdef __APPLE__	// for MacOS
		vshader = "shaders/vshader_mac.glsl";
		fshader = "shaders/fshader_mac.glsl";
	#else				// for Windows
		vshader = "shaders/vshader_win.glsl";
		fshader = "shaders/fshader_win.glsl";
	#endif

	// 顶面
	TriMesh* top = new TriMesh();
	top->setNormalize(true);
	//
	top->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	top->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	top->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	top->setShininess(10.0f);
	//
	top->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	top->setTranslation(glm::vec3(0.0, 22.5, 0.0));
	top->setRotation(glm::vec3(90.0, 0.0, 0.0));
	top->setScale(glm::vec3(100.0, 100.0, 100.0));
	// 加到painter中
	painter->addMesh(top, "sky_top", "./assets/sky/top.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(top);

	// 底部
	TriMesh* bottom = new TriMesh();
	bottom->setNormalize(true);
	bottom->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	//
	bottom->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	bottom->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	bottom->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	bottom->setShininess(10.0f);
	//
	bottom->setTranslation(glm::vec3(0.0, -0.02, 0.0));
	bottom->setRotation(glm::vec3(90.0, 0.0, 0.0));
	bottom->setScale(glm::vec3(100.0, 100.0, 100.0));
	// 加到painter中
	painter->addMesh(bottom, "sky_bottom", "./assets/sky/bottom.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(bottom);

	// 左边
	TriMesh* left = new TriMesh();
	left->setNormalize(true);
	left->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	//
	left->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	left->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	left->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	left->setShininess(10.0f);
	//
	left->setTranslation(glm::vec3(-35.0, 5, 0.0));
	left->setRotation(glm::vec3(0.0, 90.0, 0.0));
	left->setScale(glm::vec3(100.0, 50.0, 100.0));
	// 加到painter中
	painter->addMesh(left, "sky_left", "./assets/sky/left.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(left);

	// 右边
	TriMesh* right = new TriMesh();
	right->setNormalize(true);
	right->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	//
	right->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	right->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	right->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	right->setShininess(10.0f);
	//
	right->setTranslation(glm::vec3(35.0, 5, 0.0));
	right->setRotation(glm::vec3(0.0, -90.0, 0.0));
	right->setScale(glm::vec3(100.0, 50.0, 100.0));
	// 加到painter中
	painter->addMesh(right, "sky_right", "./assets/sky/right.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(right);

	// 前面
	TriMesh* front = new TriMesh();
	front->setNormalize(true);
	front->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	//
	front->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	front->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	front->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	front->setShininess(10.0f);
	//
	front->setTranslation(glm::vec3(0.0, 5, -35.0));
	front->setRotation(glm::vec3(0.0, 0.0, 0.0));
	front->setScale(glm::vec3(100.0, 50.0, 100.0));
	// 加到painter中
	painter->addMesh(front, "sky_front", "./assets/sky/front.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据  
	meshList.push_back(front);

	// 背面
	TriMesh* back = new TriMesh();
	back->setNormalize(true);
	back->generateSquare(glm::vec3(1.0, 1.0, 1.0));
	//
	back->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	back->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	back->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	back->setShininess(10.0f);
	//
	back->setTranslation(glm::vec3(0.0, 5, 35.0));
	back->setRotation(glm::vec3(0.0, 180.0, 0.0));
	back->setScale(glm::vec3(100.0, 50.0, 100.0));
	// 加到painter中
	painter->addMesh(back, "sky_back", "./assets/sky/back.jpg", vshader, fshader, false); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(back);
}

// 加载场景
void load_Scene() {
	std::string vshader, fshader;
	// 读取着色器并使用
	#ifdef __APPLE__	// for MacOS
		vshader = "shaders/vshader_mac.glsl";
		fshader = "shaders/fshader_mac.glsl";
	#else				// for Windows
		vshader = "shaders/vshader_win.glsl";
		fshader = "shaders/fshader_win.glsl";
	#endif

	// 古树模型
	TriMesh* tree = new TriMesh();
	tree->setNormalize(true);
	tree->readObj("./assets/tree/tree.obj");
	tree->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	tree->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	tree->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	tree->setShininess(10.0f);
	// 设置物体的旋转位移
	tree->setTranslation(glm::vec3(6.0, 2.5, -10.0));
	tree->setRotation(glm::vec3(0.0, 0.0, 0.0));
	tree->setScale(glm::vec3(10.0, 10.0, 10.0));
	// 加到painter中
	painter->addMesh(tree, "tree", "./assets/tree/tree.png", vshader, fshader, true); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(tree);

	// 读取房屋模型
	TriMesh* house = new TriMesh();
	house->setNormalize(true);
	house->readObj("./assets/house/house.obj");
	house->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	house->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	house->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	house->setShininess(10.0f);
	// 设置物体的旋转位移
	house->setTranslation(glm::vec3(0.0, 1.8, -15.0));
	house->setRotation(glm::vec3(0.0, 260.0, 0.0));
	house->setScale(glm::vec3(10.0, 10.0, 10.0));
	// 加到painter中
	painter->addMesh(house, "house", "./assets/house/house.png", vshader, fshader, true); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(house);


	// 杂物
	TriMesh* za = new TriMesh();
	za->setNormalize(true);
	za->readObj("./assets/za/za.obj");
	za->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	za->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	za->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	za->setShininess(10.0f);
	// 设置物体的旋转位移
	za->setTranslation(glm::vec3(-2.0, 2.8, -4.0));
	za->setRotation(glm::vec3(0.0, -30.0, 0.0));
	za->setScale(glm::vec3(10.0, 10.0, 10.0));
	// 加到painter中
	painter->addMesh(za, "za", "./assets/za/za.png", vshader, fshader, true); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(za);

	// 大圣雕塑
	TriMesh* dasheng = new TriMesh();
	dasheng->setNormalize(true);
	dasheng->readObj("./assets/dasheng/dasheng.obj");
	dasheng->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	dasheng->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	dasheng->setSpecular(glm::vec4(0.0, 0.0, 0.0, 1.0)); // 环境光
	dasheng->setShininess(10.0f);
	// 设置物体的旋转位移
	dasheng->setTranslation(glm::vec3(6.6, 0.7, -7.0));
	dasheng->setRotation(glm::vec3(0.0, -90.0, 0.0));
	dasheng->setScale(glm::vec3(2.0, 2.0, 1.0));
	// 加到painter中
	painter->addMesh(dasheng, "mesh_a", "./assets/dasheng/dasheng.png", vshader, fshader, true); 	// 指定纹理与着色器
	// 程序结束时回收物体数据 
	meshList.push_back(dasheng);
}

void init()
{
	std::string vshader, fshader;
	// 读取着色器并使用
	#ifdef __APPLE__	// for MacOS
		vshader = "shaders/vshader_mac.glsl";
		fshader = "shaders/fshader_mac.glsl";
	#else				// for Windows
		vshader = "shaders/vshader_win.glsl";
		fshader = "shaders/fshader_win.glsl";
	#endif

	// 设置光源位置
	light->setTranslation(glm::vec3(0.0, 30.0, 2.0));

	light->setAmbient(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 环境光
	light->setDiffuse(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 漫反射
	light->setSpecular(glm::vec4(1.0, 1.0, 1.0, 1.0)); // 镜面反射
	light->setAttenuation(1.0, 0.045, 0.0075); // 衰减系数

	// 加载天空
	load_Sky();
	// 加载场景
	load_Scene();
	// 加载人物模型
	wk->init();
	//glClearColor(1.0, 1.0, 1.0, 1.0);
	glClearColor(0.0, 0.0, 0.0, 1.0);
}


void display1()
{
	glViewport(WIDTH * 3 / 8, HEIGHT * 3 / 8, WIDTH * 5 / 8, HEIGHT * 5 / 8);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	// true 为使用正交投影，false为使用透视投影
	if (cameraMode == 1) { 
		// 实现持续按键
		if (cons[0])
			camera_1->ProcessKeyboard(FORWARD, deltaTime);
		if (cons[1])
			camera_1->ProcessKeyboard(BACKWARD, deltaTime);
		if (cons[2])
			camera_1->ProcessKeyboard(LEFTWARD, deltaTime);
		if (cons[3])
			camera_1->ProcessKeyboard(RIGHTWARD, deltaTime);
		if (cons[4])
			camera_1->ProcessKeyboard(UPWARD, deltaTime);
		if (cons[5])
			camera_1->ProcessKeyboard(BACKWARD, deltaTime);
	}
	else if (cameraMode == 2) {
		// 改为物体的信息
		glm::vec3 location = wk->body->getTranslation();
		glm::vec3 Direction = glm::normalize(glm::vec3(sin(glm::radians(wk->Yaw)), 0.0f, cos(glm::radians(wk->Yaw))));
		camera_1->Position = glm::vec4(location + Direction , 1.0);
		camera_1->Yaw = -wk->Yaw;
	}
	// std::cout << "gun: " << robot.theta[robot.Gun] << std::endl;
	// 渲染
	painter->drawMeshes(light, camera_1, projMode);
	wk->show(light, camera_1, projMode);
	//glutSwapBuffers();
}

void display2() {
	glViewport(0, 0, WIDTH * 3 / 8, HEIGHT * 3 / 8);
	// 实现持续按键
	if (cons[0])
		camera_2->ProcessKeyboard(FORWARD, deltaTime);
	if (cons[1])
		camera_2->ProcessKeyboard(BACKWARD, deltaTime);
	if (cons[2])
		camera_2->ProcessKeyboard(LEFTWARD, deltaTime);
	if (cons[3])
		camera_2->ProcessKeyboard(RIGHTWARD, deltaTime);
	if (cons[4])
		camera_2->ProcessKeyboard(UPWARD, deltaTime);
	if (cons[5])
		camera_2->ProcessKeyboard(BACKWARD, deltaTime);

	// 渲染
	painter->drawMeshes(light, camera_2, projMode);
	wk->show(light, camera_2, projMode);
}

void printHelp() {
    std::cout << "================================================" << std::endl << std::endl;
    std::cout << "Perspective Switching" << std::endl;
    std::cout << "Tab: Switch between free camera and Wukong perspective" << std::endl << std::endl;

    std::cout << "Object Movement Switching" << std::endl;
    std::cout << "F1: Current moving object is the camera" << std::endl;
    std::cout << "F2: Current moving object is Wukong" << std::endl << std::endl;

    std::cout << "Camera Movement" << std::endl;
    std::cout << "W, A, S, D: Move the camera forward, left, backward, right" << std::endl;
    std::cout << "UP↑: Move the camera up" << std::endl;
    std::cout << "DOWN↓: Move the camera down" << std::endl;
    std::cout << "Number 0 + (Shift): Adjust the camera's field of view (FOV)" << std::endl;
    std::cout << "Mouse move: Adjust the camera's perspective (left and right rotation)" << std::endl;
    std::cout << "Mouse wheel: Adjust the camera's field of view (FOV)" << std::endl << std::endl;

    std::cout << "Wukong Movement" << std::endl;
    std::cout << "Basic Movement" << std::endl;
    std::cout << "W, A, S, D: Move Wukong forward, left, backward, right" << std::endl;
    std::cout << "UP↑: Move Wukong up" << std::endl;
    std::cout << "DOWN↓: Move Wukong down" << std::endl;
    std::cout << "Mouse move: Adjust Wukong's perspective (up and down rotation)" << std::endl;
    std::cout << "Mouse wheel: Adjust Wukong's field of view (FOV)" << std::endl << std::endl;

    std::cout << "Body Part Rotation" << std::endl;
    std::cout << "1: Select torso" << std::endl;
    std::cout << "2: Select head" << std::endl;
    std::cout << "3, 4: Select left arm, left hand" << std::endl;
    std::cout << "5, 6: Select right arm, right hand" << std::endl;
    std::cout << "7, 8: Select left thigh, left lower leg" << std::endl;
    std::cout << "9, 0: Select right thigh, right lower leg" << std::endl;
    std::cout << "Z: Select left foot" << std::endl;
    std::cout << "X: Select right foot" << std::endl;
    std::cout << "C: Select the Golden Cudgel" << std::endl;
    std::cout << "+, -: Increase or decrease the angle" << std::endl << std::endl;

    std::cout << "Skill Release" << std::endl;
    std::cout << "J + (Shift): Release the spinning staff skill" << std::endl;
    std::cout << "K + (Shift): Release the flying Golden Cudgel skill" << std::endl;
    std::cout << "L + (Shift): Release the enlarging Golden Cudgel skill" << std::endl;
    std::cout << "P + (Shift): Summon the somersault cloud" << std::endl;
    std::cout << "R: Reset action parameters" << std::endl << std::endl;

    std::cout << "Perspective Projection" << std::endl;
    std::cout << "Enter: Switch between orthographic and perspective projection" << std::endl;
    std::cout << "Default projection method is orthographic, press Enter to switch" << std::endl;
    std::cout << "Perspective projection is recommended for better effect" << std::endl;
    std::cout << "================================================" << std::endl;
}

// 键盘响应函数
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mode)
{
	// 投影方式切换
	if (glfwGetKey(window, GLFW_KEY_ENTER))
		projMode = !projMode;

	// 相机视角切换
	if (glfwGetKey(window, GLFW_KEY_TAB)) {
		if (cameraMode == 1) {
			cameraMode = 2;
		}
		else if (cameraMode == 2) {
			cameraMode = 1;
			// 恢复第三人称视角
			camera_1->Position = camera_2->Position;
			camera_1->Yaw = camera_2->Yaw;
		}
		std::cout << "camera mode: " << cameraMode << std::endl;
	}

	// 移动对象切换
	if (glfwGetKey(window, GLFW_KEY_F1)) {
		moveMode = 1;
	}
	else if (glfwGetKey(window, GLFW_KEY_F2)) {
		moveMode = 2;
	}
	
	//  控制相应的物体运动
	if (moveMode == 1) {
		if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
			cons[0] = true;
		if (glfwGetKey(window, GLFW_KEY_W) == GLFW_RELEASE) 
			cons[0] = false;
		if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
			cons[1] = true;
		if (glfwGetKey(window, GLFW_KEY_S) == GLFW_RELEASE) 
			cons[1] = false;
		if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
			cons[2] = true;
		if (glfwGetKey(window, GLFW_KEY_A) == GLFW_RELEASE)
			cons[2] = false;
		if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
			cons[3] = true;
		if (glfwGetKey(window, GLFW_KEY_D) == GLFW_RELEASE)
			cons[3] = false;
		if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
			cons[4] = true;
		if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_RELEASE)
			cons[4] = false;
		if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
			cons[5] = true;
		if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_RELEASE)
			cons[5] = false;
		if (key == GLFW_KEY_O && action == GLFW_PRESS && mode == 0x0000)
		{
			camera_1->Zoom = camera_1->Zoom + 0.1f <= 10.0f ? camera_1->Zoom + 0.1f : 10.0f;
			camera_2->Zoom = camera_2->Zoom + 0.1f <= 10.0f ? camera_2->Zoom + 0.1f : 10.0f;
		}
		if (key == GLFW_KEY_O && action == GLFW_PRESS && mode == GLFW_MOD_SHIFT)
		{
			camera_1->Zoom = camera_1->Zoom - 0.1f >= 0.5f ? camera_1->Zoom - 0.1f : 0.5f;
			camera_2->Zoom = camera_2->Zoom - 0.1f >= 0.5f ? camera_2->Zoom - 0.1f : 0.5f;
		}
	}
	else if (moveMode == 2) {
		isMove = false;
		if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS)
		{
			wk->ProcessKeyboard(FORWARD, deltaTime);
			isMove = true;
		}
		if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS)
		{
			wk->ProcessKeyboard(BACKWARD, deltaTime);
			isMove = true;
		}
		if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS)
		{
			wk->ProcessKeyboard(LEFTWARD, deltaTime);
			isMove = true;
		}
		if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS)
		{
			wk->ProcessKeyboard(RIGHTWARD, deltaTime);
			isMove = true;
		}
		if (glfwGetKey(window, GLFW_KEY_UP) == GLFW_PRESS)
			wk->ProcessKeyboard(UPWARD, deltaTime);
		if (glfwGetKey(window, GLFW_KEY_DOWN) == GLFW_PRESS)
			wk->ProcessKeyboard(DOWNWARD, deltaTime);
	}

	// 控制wukong
	if (action == GLFW_PRESS) {
		switch (key)
		{
		case GLFW_KEY_ESCAPE: exit(EXIT_SUCCESS); break;
		case GLFW_KEY_Q: exit(EXIT_SUCCESS); break;
		case GLFW_KEY_1: Selected_mesh = robot.Body; break;
		case GLFW_KEY_2: Selected_mesh = robot.Head; break;
		case GLFW_KEY_3: Selected_mesh = robot.LeftArm; break;
		case GLFW_KEY_4: Selected_mesh = robot.LeftHand; break;
		case GLFW_KEY_5: Selected_mesh = robot.RightArm; break;
		case GLFW_KEY_6: Selected_mesh = robot.RightHand; break;
		case GLFW_KEY_7: Selected_mesh = robot.LeftThigh; break;
		case GLFW_KEY_8: Selected_mesh = robot.LeftShin; break;
		case GLFW_KEY_9: Selected_mesh = robot.RightThigh; break;
		case GLFW_KEY_0: Selected_mesh = robot.RightShin; break;
		case GLFW_KEY_Z: Selected_mesh = robot.LeftFoot; break;
		case GLFW_KEY_X: Selected_mesh = robot.RightFoot; break;
		case GLFW_KEY_C: Selected_mesh = robot.Gun; break;
		case GLFW_KEY_R: wk->reset(); break;
		// 七十二变----转棍
		case GLFW_KEY_J: {
			if (mode == GLFW_MOD_SHIFT)
			{
				// 恢复默认姿势
				wk->reset();
				skills[0] = false;
				// 如果之前打开了音乐，现在需要停止并关闭它
				mciSendString("stop 72bian", NULL, 0, NULL);
				mciSendString("close 72bian", NULL, 0, NULL);
			}
			else
			{
				skills[0] = true;
				// 首先检查是否已经打开了音乐，如果是，则先关闭
				mciSendString("close 72bian", NULL, 0, NULL);
				// 打开并播放音乐
				mciSendString("open ./music/72bian.mp3 alias 72bian", NULL, 0, NULL);
				mciSendString("play 72bian", NULL, 0, NULL);
			}
			skills[1] = false;
			break;
 		}
		// 七十二变----金箍棒旋转
		case GLFW_KEY_K: {
			if (mode == GLFW_MOD_SHIFT)
			{
				// 重置大小
				skills[1] = false;
				wk->kptraslate = glm::vec3(0.08, -0.25, -0.04);
				robot.theta[robot.Gun] = 110.0f;
				// 如果之前打开了音乐，现在需要停止并关闭它
				mciSendString("stop 72bian", NULL, 0, NULL);
				mciSendString("close 72bian", NULL, 0, NULL);
			}
			else
			{
				skills[1] = true;
				skills[0] = false;
				// 首先检查是否已经打开了音乐，如果是，则先关闭
				mciSendString("close 72bian", NULL, 0, NULL);
				// 打开并播放音乐
				mciSendString("open ./music/72bian.mp3 alias 72bian", NULL, 0, NULL);
				mciSendString("play 72bian", NULL, 0, NULL);
			}
			break;
		}
		// 七十二变----金箍棒变大
		case GLFW_KEY_L: {
			if (mode == GLFW_MOD_SHIFT)
			{
				// 重置大小
				wk->kpscale = glm::vec3(1.0, 2.0, 1.0);				
				// 如果之前打开了音乐，现在需要停止并关闭它
				mciSendString("stop 72bian", NULL, 0, NULL);
				mciSendString("close 72bian", NULL, 0, NULL);
			}
			else
			{
				wk->kpscale += glm::vec3(0.02, 0.1, 0.02);
				// 首先检查是否已经打开了音乐，如果是，则先关闭
				mciSendString("close 72bian", NULL, 0, NULL);
				// 打开并播放音乐
				mciSendString("open ./music/72bian.mp3 alias 72bian", NULL, 0, NULL);
				mciSendString("play 72bian", NULL, 0, NULL);
			}
			break;
		}
		// 召唤筋斗云
		case GLFW_KEY_P: {
			if (mode == GLFW_MOD_SHIFT) {
				wk->yun = false;
				// 如果之前打开了音乐，现在需要停止并关闭它
				mciSendString("stop pao", NULL, 0, NULL);
				mciSendString("close pao", NULL, 0, NULL);
			}
			else {
				// 首先检查是否已经打开了音乐，如果是，则先关闭
				mciSendString("close pao", NULL, 0, NULL);
				// 打开并播放音乐
				mciSendString("open ./music/pao.mp3 alias pao", NULL, 0, NULL);
				mciSendString("play pao", NULL, 0, NULL);
				// 
				wk->body->setTranslation(wk->body->getTranslation() + glm::vec3(0.0, 0.5, 0.0));
				wk->yun = true;
				// 设置动作参数
				robot.theta[robot.Gun] = 30.0f;
				robot.theta[robot.LeftArm] = 310.0f;
				robot.theta[robot.LeftHand] = 305.0f;
				robot.theta[robot.RightArm] = 140.0f;
				robot.theta[robot.RightHand] = 50.0f;
				robot.theta[robot.LeftThigh] = 50.0f;
				robot.theta[robot.LeftShin] = 310.0f;
				robot.theta[robot.LeftFoot] = 360.0f;
				robot.theta[robot.RightThigh] = 325.0f;
				robot.theta[robot.RightShin] = 355.0f;
				robot.theta[robot.RightFoot] = 40.0f;
			}
			break;
		}
		// 通过按键旋转关节部位
		case GLFW_KEY_KP_ADD:
			robot.theta[Selected_mesh] += 5.0;
			if (robot.theta[Selected_mesh] > 360.0)
				robot.theta[Selected_mesh] -= 360.0;
			break;
		case GLFW_KEY_KP_SUBTRACT:
			robot.theta[Selected_mesh] -= 5.0;
			if (robot.theta[Selected_mesh] < 0.0)
				robot.theta[Selected_mesh] += 360.0;
			break;
		}
	}
}

// 滚轮输入的回调函数
void scroll_callback(GLFWwindow* window, double xoffset, double yoffset) {
	// std::cout << "Scroll: " << yoffset << std::endl; // 测试输出
	camera_1->ProcessMouseScroll(static_cast<float>(yoffset));
	camera_2->ProcessMouseScroll(static_cast<float>(yoffset));
}

// 鼠标输入的回调函数
void mouse_callback(GLFWwindow* window, double xposIn, double yposIn) {
	float xpos = static_cast<float>(xposIn);
	float ypos = static_cast<float>(yposIn);

	// 若窗口第一次获取焦点, 则直接设置 lastX 和 lastY
	if (firstMouse) {
		lastX = xpos;
		lastY = ypos;
		firstMouse = false;
	}
	// 计算偏移量(单位: 像素)
	float xoffset = xpos - lastX;
	float yoffset = lastY - ypos;  
	lastX = xpos;
	lastY = ypos;

	camera_1->ProcessMouseMovement(xoffset, yoffset);
	camera_2->ProcessMouseMovement(xoffset, yoffset);
}

void cleanData() {
	// 释放内存
	delete camera_1;
	camera_1 = NULL;
	delete camera_2;
	camera_2 = NULL;

	delete light;
	light = NULL;

	painter->cleanMeshes();

	delete painter;
	painter = NULL;
	
	for (int i=0; i<meshList.size(); i++) {
		delete meshList[i];
	}
	meshList.clear();
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int day_time = 0;
float current_time = 0, last_time = 0;
void sunMove() {
	float current_time = static_cast<float>(glfwGetTime());
	if (current_time - last_time > 0.4) {
		day_time++;
		if (day_time > 300) {
			day_time = 0;
		}
		glm::vec3 pos = light->getTranslation();

		//光源位置随时间改变,环境光颜色随时间改变
		if (day_time < 150) {
			pos.x = 3 - 0.04 * day_time;
		}
		else {
			pos.x = -3 + 0.04 * (day_time - 150);
		}
		// 更新时间
		last_time = current_time;
		light->setTranslation(pos);
		return;
	}
}

int main(int argc, char** argv)
{
	// 初始化GLFW库，必须是应用程序调用的第一个GLFW函数
	glfwInit();

	// 配置GLFW
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	#ifdef __APPLE__
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	#endif

	// 配置窗口属性
	GLFWwindow* window = glfwCreateWindow(WIDTH, HEIGHT, "2022152021_王培鸿_期末大作业", NULL, NULL);
	if (window == NULL)
	{
		std::cout << "Failed to create GLFW window" << std::endl;
		glfwTerminate();
		return -1;
	}
	glfwMakeContextCurrent(window);
	glfwSetKeyCallback(window, key_callback);
	glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
	glfwSetScrollCallback(window, scroll_callback);
	glfwSetCursorPosCallback(window, mouse_callback);
	//glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED);

	// 调用任何OpenGL的函数之前初始化GLAD
	// ---------------------------------------
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}

	// Init mesh, shaders, buffer
	init();
	// 输出帮助信息
	printHelp();
	// 启用深度测试
	glEnable(GL_DEPTH_TEST);


	bool increase = true;
	bool dir = true;		// 为真左脚，为假右脚
	bool forw = true;		// 是否往回转
	while (!glfwWindowShouldClose(window))
	{
		// 计算控制摄像机速度的变量
		float currentFrame = static_cast<float>(glfwGetTime());
		deltaTime = currentFrame - lastFrame;
		lastFrame = currentFrame;
		
		// 光源变化
		sunMove();
		// 第一个技能
		if (skills[0]) {
			if (increase) {
				robot.theta[robot.LeftArm] = 70.0;
				robot.theta[robot.LeftHand] = 290.0;
				robot.theta[robot.RightArm] = 55.0;
				robot.theta[robot.RightHand] = 70.0;
				// 如果当前值小于最大值，则增加
				if (robot.theta[robot.Gun] < 120.0f) {
					robot.theta[robot.Gun] += 5.0f;
				}
				else {
					// 达到最大值，反转方向
					increase = false;
				}
			}
			else {
			 	robot.theta[robot.LeftArm] = 55.0;
				robot.theta[robot.LeftHand] = 290.0;
				robot.theta[robot.RightArm] = 65.0;
				robot.theta[robot.RightHand] = 70.0;
				// 如果当前值大于最小值，则减少
				if (robot.theta[robot.Gun] > -120.0f) {
					robot.theta[robot.Gun] -= 5.0f;
				}
				else {
					// 达到最小值，反转方向
					increase = true;
				}
			}
		}
		// 第二个技能
		if (skills[1]) {
			if (forw)
			{
				wk->kptraslate += glm::vec3(0.02, 0.0, 0.0);
				robot.theta[robot.Gun] += 5.0f;
				if (wk->kptraslate[0] > 10.0f)
					forw = false;
			}
			else 
			{
				wk->kptraslate -= glm::vec3(0.02, 0.0, 0.0);
				robot.theta[robot.Gun] -= 5.0f;
				if (wk->kptraslate[0] < 0.8f)
					forw = true;
			}
		}


		// 绘制窗口
		display1();
		display2();

		// 交换颜色缓冲 以及 检查有没有触发什么事件（比如键盘输入、鼠标移动等）
		// -------------------------------------------------------------------------------
		glfwSwapBuffers(window);
		glfwPollEvents();
	}

	cleanData();

	return 0;
}

// 每当窗口改变大小，GLFW会调用这个函数并填充相应的参数供你处理。
// ---------------------------------------------------------------------------------------------
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
	// make sure the viewport matches the new window dimensions; note that width and 
	// height will be significantly larger than specified on retina displays.
	glViewport(0, 0, width, height);
}