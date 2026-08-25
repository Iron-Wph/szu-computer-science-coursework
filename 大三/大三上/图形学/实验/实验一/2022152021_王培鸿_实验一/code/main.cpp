#include "Angel.h"
#include <string>

const glm::vec3 WHITE(1.0, 1.0, 1.0);
const glm::vec3 BLACK(0.0, 0.0, 0.0);
const glm::vec3 RED(1.0, 0.0, 0.0);
const glm::vec3 GREEN(0.0, 1.0, 0.0);
const glm::vec3 BLUE(0.0, 0.0, 1.0); 
const int CIRCLE_NUM_POINTS = 100;
const int ELLIPSE_NUM_POINTS = 100;
const int TRIANGLE_NUM_POINTS  = 3;
const int SQUARE_NUM  = 6;
const int SQUARE_NUM_POINTS  = 4 * SQUARE_NUM;
const int LINE_NUM_POINTS = 2;

// 每当窗口改变大小，GLFW会调用这个函数并填充相应的参数
void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
	glViewport(0, 0, width, height);
}

// 根据角度生成颜色
float generateAngleColor(double angle)
{
	return 1.0 / (2 * M_PI) * angle;
}

// 获得三角形的每个角度
double getTriangleAngle(int point)
{
	return 2 * M_PI / 3 * point;
}

// 获得正方形的每个角度
double getSquareAngle(int point)
{
	return M_PI / 4 + (M_PI / 2 * point);
}

// 计算椭圆/圆上的点
glm::vec2 getEllipseVertex(glm::vec2 center, double scale, double verticalScale, double angle)
{
	glm::vec2 vertex(sin(angle), cos(angle));
	vertex *= scale;
	vertex.y *= verticalScale;
	vertex += center;
	return vertex;
}

// 获得三角形的每个顶点
void generateTrianglePoints(glm::vec2 vertices[], glm::vec3 colors[], int startVertexIndex)
{
	glm::vec2 scale(0.25, 0.25);
	glm::vec2 center(0.0, 0.70);

	for (int i = 0; i < 3; ++i) {
		double currentAngle = getTriangleAngle(i);
		vertices[startVertexIndex + i] = glm::vec2(sin(currentAngle), cos(currentAngle)) * scale + center;
	}

	colors[startVertexIndex] = RED;
	colors[startVertexIndex + 1] = GREEN;
	colors[startVertexIndex + 2] = BLUE;
}

// 获得正方形的每个顶点
void generateSquarePoints(glm::vec2 vertices[], glm::vec3 colors[], int squareNumber, int startVertexIndex)
{
	glm::vec2 scale(0.90, 0.90);
	double scaleDecrease = 0.15;
	glm::vec2 center(0.0, -0.25);
	int vertexIndex = startVertexIndex;

	for (int i = 0; i < squareNumber; ++i) {
		glm::vec3 currentColor;
		currentColor = (i % 2) ? BLACK : WHITE;
		for (int j = 0; j < 4; ++j) {
			double currentAngle = getSquareAngle(j);
			vertices[vertexIndex] = glm::vec2(sin(currentAngle), cos(currentAngle)) * scale + center;
			colors[vertexIndex] = currentColor;
			vertexIndex++;
		}
		scale -= scaleDecrease;
	}
}

void generateLinePoints(glm::vec2 vertices[], glm::vec3 colors[], int startVertexIndex)
{
	vertices[startVertexIndex] = glm::vec2(-1.0, -1.0);
	vertices[startVertexIndex + 1] = glm::vec2(1.0, 1.0);


	colors[startVertexIndex] = WHITE;
	colors[startVertexIndex + 1] = BLUE;
}

// 获得椭圆/圆的每个顶点
void generateEllipsePoints(glm::vec2 vertices[], glm::vec3 colors[], int startVertexIndex, int numPoints,
	glm::vec2 center, double scale, double verticalScale)
{
	double angleIncrement = (2 * M_PI) / numPoints;
	double currentAngle = M_PI / 2;

	for (int i = startVertexIndex; i < startVertexIndex + numPoints; ++i) {
		vertices[i] = getEllipseVertex(center, scale, verticalScale, currentAngle);
		if (verticalScale == 1.0) {
			colors[i] = glm::vec3(generateAngleColor(currentAngle), 0.0, 0.0);
		}
		else {
			colors[i] = RED;
		}
		currentAngle += angleIncrement;
	}
}

// GGbond专用椭圆定制
void generateGGbond(glm::vec2 vertices[], glm::vec3 colors[], int startVertexIndex, int numPoints,
	glm::vec2 center, double scale, double verticalScale, glm::vec3 color)
{
	double angleIncrement = (2 * M_PI) / numPoints;
	double currentAngle = M_PI / 2;

	for (int i = startVertexIndex; i < startVertexIndex + numPoints; ++i) {
		vertices[i] = getEllipseVertex(center, scale, verticalScale, currentAngle);
		// 填充指定的颜色
		colors[i] = color;
		currentAngle += angleIncrement;
	}
}

// GGbond专用三角形定制
void generateGGbondTriangle(glm::vec2 vertices[], glm::vec3 colors[], int startVertexIndex)
{
	glm::vec2 scale(0.55, 0.55);
	glm::vec2 center(0.0, -0.10);

	for (int i = 0; i < 3; ++i) {
		double currentAngle = getTriangleAngle(i) + M_PI;
		vertices[startVertexIndex + i] = glm::vec2(sin(currentAngle), cos(currentAngle)) * scale + center;
	}
	colors[startVertexIndex] = RED;
	colors[startVertexIndex + 1] = GREEN;
	colors[startVertexIndex + 2] = BLUE;
}
// GGbond专用正方形绘制
void generateGGbondSquare(glm::vec2 vertices[], glm::vec3 colors[], int squareNumber, int startVertexIndex)
{
	glm::vec2 scale(0.05, 0.90);
	double scaleDecrease = 0.15;
	glm::vec2 center(0.0, -0.25);
	int vertexIndex = startVertexIndex;
	glm::vec3 currentColor = WHITE;
	for (int j = 0; j < 4; ++j) {
		double currentAngle = getSquareAngle(j);
		vertices[vertexIndex] = glm::vec2(sin(currentAngle), cos(currentAngle)) * scale + center;
		colors[vertexIndex] = currentColor;
		vertexIndex++;
	}
	scale -= scaleDecrease;
}
GLuint vao1[5], program1;
void init1()
{
	// 定义三角形的点
	glm::vec2 triangle_vertices[TRIANGLE_NUM_POINTS];
	glm::vec3 triangle_colors[TRIANGLE_NUM_POINTS];
	// 定义矩形的点
	glm::vec2 square_vertices[SQUARE_NUM_POINTS];
	glm::vec3 square_colors[SQUARE_NUM_POINTS];
	// 定义线的点
	glm::vec2 line_vertices[LINE_NUM_POINTS];
	glm::vec3 line_colors[LINE_NUM_POINTS];

	// 调用生成形状顶点位置的函数
	generateTrianglePoints(triangle_vertices, triangle_colors, 0);
	generateSquarePoints(square_vertices, square_colors, SQUARE_NUM, 0);
	generateLinePoints(line_vertices, line_colors, 0);

	// @TODO: 生成圆形和椭圆上的点和颜色
	// 定义圆形的点和颜色
	glm::vec2 circle_vertices[CIRCLE_NUM_POINTS];
	glm::vec3 circle_colors[CIRCLE_NUM_POINTS];
	// 定义椭圆的点和颜色
	glm::vec2 ellipse_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 ellipse_colors[ELLIPSE_NUM_POINTS];
	// 生成圆形和椭圆顶点位置的函数
	generateEllipsePoints(circle_vertices, circle_colors, 0, CIRCLE_NUM_POINTS, glm::vec2 (0.5,0.7), 0.2, 1);
	generateEllipsePoints(ellipse_vertices, ellipse_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.5, 0.7), 0.3, 0.4);

	// 读取着色器并使用
	std::string vshader, fshader;
	vshader = "shaders/vshader.glsl";
	fshader = "shaders/fshader.glsl";
	program1 = InitShader(vshader.c_str(), fshader.c_str());
	glUseProgram(program1);

	// 创建顶点缓存对象，vbo[2]是因为我们将要使用两个缓存对象
	GLuint vbo1[2];
	/*
	* 初始化三角形的数据
	*/
	glGenVertexArrays(1, &vao1[0]);		
	glBindVertexArray(vao1[0]);			

	glGenBuffers(1, &vbo1[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(triangle_vertices), triangle_vertices, GL_STATIC_DRAW);
	GLuint location  = glGetAttribLocation(program1, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo1[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(triangle_colors), triangle_colors, GL_STATIC_DRAW);
	GLuint cLocation  = glGetAttribLocation(program1, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	/*
	* 初始化正方形的数据
	*/  

	glGenVertexArrays(1, &vao1[1]);      
	glBindVertexArray(vao1[1]);         

	glGenBuffers(1, &vbo1[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(square_vertices), square_vertices, GL_STATIC_DRAW);
	location  = glGetAttribLocation(program1, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo1[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(square_colors), square_colors, GL_STATIC_DRAW);
	cLocation  = glGetAttribLocation(program1, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	/*
	* 初始化线的数据
	*/

	glGenVertexArrays(1, &vao1[2]);
	glBindVertexArray(vao1[2]);

	glGenBuffers(1, &vbo1[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(line_vertices), line_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program1, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo1[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(line_colors), line_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program1, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化圆形的数据
	glGenVertexArrays(1, &vao1[3]);
	glBindVertexArray(vao1[3]);

	glGenBuffers(1, &vbo1[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(circle_vertices), circle_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program1, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo1[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(circle_colors), circle_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program1, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化椭圆的数据
	glGenVertexArrays(1, &vao1[4]);
	glBindVertexArray(vao1[4]);

	glGenBuffers(1, &vbo1[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ellipse_vertices), ellipse_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program1, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo1[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo1[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ellipse_colors), ellipse_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program1, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 设置背景颜色
	glClearColor(0.0, 0.0, 0.0, 1.0);
}

void display1(void)
{

	glClear(GL_COLOR_BUFFER_BIT);

	glUseProgram(program1);

	// 三角形
	glBindVertexArray(vao1[0]);
	glDrawArrays(GL_TRIANGLES, 0, TRIANGLE_NUM_POINTS);
	
	// 正方形
	glBindVertexArray(vao1[1]);
	for (int i = 0; i  < SQUARE_NUM; ++i) {
		glDrawArrays(GL_TRIANGLE_FAN, (i * 4), 4);
	}

	// 线型
	glBindVertexArray(vao1[2]);
	glDrawArrays(GL_LINES, 0, LINE_NUM_POINTS);

	// @TODO: 绘制圆
	glBindVertexArray(vao1[3]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, CIRCLE_NUM_POINTS);

	// @TODO: 绘制椭圆
	glBindVertexArray(vao1[4]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);

	glFlush();
}


GLuint vao2[20], program2;
void init2()
{
	// 绘制黄色红领巾
	glm::vec2 jin_vertices[TRIANGLE_NUM_POINTS];
	glm::vec3 jin_colors[TRIANGLE_NUM_POINTS];
	generateGGbondTriangle(jin_vertices, jin_colors, 0);

	// 绘制枝干
	glm::vec2 shu_vertices[SQUARE_NUM_POINTS];
	glm::vec3 shu_colors[SQUARE_NUM_POINTS];
	generateGGbondSquare(shu_vertices, shu_colors, SQUARE_NUM, 0);
	

	// 绘制脸部：定义椭圆的点和颜色
	glm::vec2 face_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 face_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(face_vertices, face_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0, 0.40), 0.6, 0.8, glm::vec3 (0.6, 0.6, 0.4));
	// 绘制耳朵 
	glm::vec2 ear1_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 ear1_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(ear1_vertices, ear1_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.45, 0.55), 0.2, 0.5, glm::vec3(0.6, 0.6, 0.4));
	glm::vec2 ear2_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 ear2_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(ear2_vertices, ear2_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.45, 0.55), 0.2, 0.5, glm::vec3(0.6, 0.6, 0.4));
	// 绘制眼镜
	glm::vec2 glass_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 glass_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(glass_vertices, glass_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.0, 0.75), 0.55, 0.2, glm::vec3(1.0, 0.0, 0.0));
	// 绘制帽子
	glm::vec2 mao1_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 mao1_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(mao1_vertices, mao1_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.20, 0.85), 0.22, 0.5, glm::vec3(1.0, 0.0, 0.0));
	glm::vec2 mao2_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 mao2_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(mao2_vertices, mao2_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.20, 0.85), 0.22, 0.5, glm::vec3(1.0, 0.0, 0.0));
	// 黄色眼睛
	glm::vec2 h1_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 h1_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(h1_vertices, h1_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.20, 0.85), 0.15, 0.35, glm::vec3(1.0, 1.0, 0.0));
	glm::vec2 h2_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 h2_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(h2_vertices, h2_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.20, 0.85), 0.15, 0.35, glm::vec3(1.0, 1.0, 0.0));
	// 黑色眼睛
	glm::vec2 b1_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 b1_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(b1_vertices, b1_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.20, 0.55), 0.10, 0.70, glm::vec3(0.0, 0.0, 0.0));
	glm::vec2 b2_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 b2_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(b2_vertices, b2_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.20, 0.55), 0.10, 0.70, glm::vec3(0.0, 0.0, 0.0));
	// 鼻子部分
	glm::vec2 n1_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 n1_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(n1_vertices, n1_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.00, 0.30), 0.20, 0.50, glm::vec3(0.8, 0.5, 0.2));
	glm::vec2 n2_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 n2_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(n2_vertices, n2_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(-0.06, 0.30), 0.05, 0.60, glm::vec3(0.0, 0.0, 0.0));
	glm::vec2 n3_vertices[ELLIPSE_NUM_POINTS];
	glm::vec3 n3_colors[ELLIPSE_NUM_POINTS];
	generateGGbond(n3_vertices, n3_colors, 0, ELLIPSE_NUM_POINTS, glm::vec2(0.06, 0.30), 0.05, 0.60, glm::vec3(0.0, 0.0, 0.0));


	// 读取着色器并使用
	std::string vshader, fshader;
	vshader = "shaders/vshader.glsl";
	fshader = "shaders/fshader.glsl";
	program2 = InitShader(vshader.c_str(), fshader.c_str());
	glUseProgram(program2);
	
	// 创建顶点缓存对象，vbo[2]是因为我们将要使用两个缓存对象
	GLuint vbo[2];

	// 初始化脸部的数据
	glGenVertexArrays(1, &vao2[0]);
	glBindVertexArray(vao2[0]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(face_vertices), face_vertices, GL_STATIC_DRAW);
	GLuint location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(face_colors), face_colors, GL_STATIC_DRAW);
	GLuint cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化第一只耳朵的数据
	glGenVertexArrays(1, &vao2[1]);
	glBindVertexArray(vao2[1]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ear1_vertices), ear1_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ear1_colors), ear1_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化第二只耳朵的数据
	glGenVertexArrays(1, &vao2[2]);
	glBindVertexArray(vao2[2]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ear2_vertices), ear2_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(ear2_colors), ear2_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化眼镜的数据
	glGenVertexArrays(1, &vao2[3]);
	glBindVertexArray(vao2[3]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(glass_vertices), glass_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(glass_colors), glass_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化帽子1的数据
	glGenVertexArrays(1, &vao2[4]);
	glBindVertexArray(vao2[4]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(mao1_vertices), mao1_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(mao1_colors), mao1_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化帽子2的数据
	glGenVertexArrays(1, &vao2[5]);
	glBindVertexArray(vao2[5]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(mao2_vertices), mao2_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(mao2_colors), mao2_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化眼睛1的数据
	glGenVertexArrays(1, &vao2[6]);
	glBindVertexArray(vao2[6]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(h1_vertices), h1_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(h1_colors), h1_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));
	// 初始化眼睛2的数据
	glGenVertexArrays(1, &vao2[7]);
	glBindVertexArray(vao2[7]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(h2_vertices), h2_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(h2_colors), h2_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化黑色眼睛1的数据
	glGenVertexArrays(1, &vao2[8]);
	glBindVertexArray(vao2[8]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(b1_vertices), b1_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(b1_colors), b1_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化黑色眼睛2的数据
	glGenVertexArrays(1, &vao2[9]);
	glBindVertexArray(vao2[9]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(b2_vertices), b2_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(b2_colors), b2_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化鼻子1的数据
	glGenVertexArrays(1, &vao2[10]);
	glBindVertexArray(vao2[10]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n1_vertices), n1_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n1_colors), n1_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化鼻子2的数据
	glGenVertexArrays(1, &vao2[11]);
	glBindVertexArray(vao2[11]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n2_vertices), n2_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n2_colors), n2_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化鼻子3的数据
	glGenVertexArrays(1, &vao2[12]);
	glBindVertexArray(vao2[12]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n3_vertices), n3_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(n3_colors), n3_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化红领巾的数据
	glGenVertexArrays(1, &vao2[13]);
	glBindVertexArray(vao2[13]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(jin_vertices), jin_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(jin_colors), jin_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 初始化枝干的数据
	glGenVertexArrays(1, &vao2[14]);
	glBindVertexArray(vao2[14]);

	glGenBuffers(1, &vbo[0]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[0]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(shu_vertices), shu_vertices, GL_STATIC_DRAW);
	location = glGetAttribLocation(program2, "vPosition");
	glEnableVertexAttribArray(location);
	glVertexAttribPointer(
		location,
		2,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec2),
		BUFFER_OFFSET(0));

	glGenBuffers(1, &vbo[1]);
	glBindBuffer(GL_ARRAY_BUFFER, vbo[1]);
	glBufferData(GL_ARRAY_BUFFER, sizeof(shu_colors), shu_colors, GL_STATIC_DRAW);
	cLocation = glGetAttribLocation(program2, "vColor");
	glEnableVertexAttribArray(cLocation);
	glVertexAttribPointer(
		cLocation,
		3,
		GL_FLOAT,
		GL_FALSE,
		sizeof(glm::vec3),
		BUFFER_OFFSET(0));

	// 设置背景颜色
	glClearColor(0.0, 0.0, 0.0, 1.0);
}

void display2(void) 
{
	glClear(GL_COLOR_BUFFER_BIT);

	glUseProgram(program2);

	// 绘制枝干
	glBindVertexArray(vao2[14]);
	for (int i = 0; i < SQUARE_NUM; ++i) {
		glDrawArrays(GL_TRIANGLE_FAN, (i * 4), 4);
	}
	glDrawArrays(GL_TRIANGLES, 0, TRIANGLE_NUM_POINTS);
	// 绘制红领巾
	glBindVertexArray(vao2[13]);
	glDrawArrays(GL_TRIANGLES, 0, TRIANGLE_NUM_POINTS);

	// 绘制脸部
	glBindVertexArray(vao2[0]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制耳朵
	glBindVertexArray(vao2[1]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[2]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制眼镜
	glBindVertexArray(vao2[3]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制帽子
	glBindVertexArray(vao2[4]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[5]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制黄色眼睛
	glBindVertexArray(vao2[6]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[7]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制黑色眼睛
	glBindVertexArray(vao2[8]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[9]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	// 绘制鼻子
	glBindVertexArray(vao2[10]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[11]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);
	glBindVertexArray(vao2[12]);
	glDrawArrays(GL_TRIANGLE_FAN, 0, ELLIPSE_NUM_POINTS);

	glFlush();
}

int main(int argc, char **argv)
{
	// 初始化GLFW库
	glfwInit();

	// 配置GLFW
	glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
	glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
	glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

	#ifdef __APPLE__
		glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
	#endif

	// 配置窗口属性
	// 配置第一个窗口
	GLFWwindow* window1 = glfwCreateWindow(512, 512, "2022152021_王培鸿_实验一", NULL, NULL);
	// 配置第二个窗口
	GLFWwindow* window2 = glfwCreateWindow(800, 800, "2022152021_王培鸿_实验一", NULL, NULL);
	if (window1 == NULL)
	{
		std::cout << "Failed to create GLFW window1" << std::endl;
		glfwTerminate();
		return -1;
	}
	if (window2 == NULL)
	{
		std::cout << "Failed to create GLFW window2" << std::endl;
		glfwTerminate();
		return -1;
	}

	glfwMakeContextCurrent(window1);
	// 调用任何OpenGL的函数之前初始化GLAD
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}
	glfwSetFramebufferSizeCallback(window1, framebuffer_size_callback);

	glfwMakeContextCurrent(window2);
	// 调用任何OpenGL的函数之前初始化GLAD
	if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
	{
		std::cout << "Failed to initialize GLAD" << std::endl;
		return -1;
	}
	glfwSetFramebufferSizeCallback(window2, framebuffer_size_callback);


	std::cout << "OpenGL Vendor: " << glGetString(GL_VENDOR) << std::endl;
	std::cout << "OpenGL Renderer: " << glGetString(GL_RENDERER) << std::endl;
	std::cout << "OpenGL Version: " << glGetString(GL_VERSION) << std::endl;
	std::cout << "Supported GLSL version is: " << glGetString(GL_SHADING_LANGUAGE_VERSION) << std::endl;
	
	
	while (!glfwWindowShouldClose(window1) && !glfwWindowShouldClose(window2))
	{	
		// 交换颜色缓冲 以及 检查有没有触发什么事件（比如键盘输入、鼠标移动等）
		// 绘制窗口1
		glfwMakeContextCurrent(window1);
		init1();
		display1();
		glfwSwapBuffers(window1);

		// 绘制窗口2
		glfwMakeContextCurrent(window2);
		init2();
		display2();
		glfwSwapBuffers(window2);
		
		glfwPollEvents();
	}

	return 0;

}
