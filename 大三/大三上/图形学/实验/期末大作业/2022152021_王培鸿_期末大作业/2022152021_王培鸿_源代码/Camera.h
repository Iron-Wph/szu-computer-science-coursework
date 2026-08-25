#ifndef _CAMERA_H_
#define _CAMERA_H_
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include "Angel.h"

enum Camera_Movement {
	FORWARD, BACKWARD, LEFTWARD, RIGHTWARD, UPWARD, DOWNWARD
};

const float YAW = -90.0f;
const float PITCH = 0.0f;
const float SPEED = 50.0f;
const float SENSITIVITY = 0.1f;
const float ZOOM = 2.0f;

class Camera {
public:
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

    // 构造函数
    Camera(glm::vec3 position = glm::vec3(0.0f, 0.0f, 1.5f),
        glm::vec3 up = glm::vec3(0.0f, 1.0f, 0.0f),
        float yaw = YAW,
        float pitch = PITCH)
        : Front(glm::vec3(0.0f, 0.0f, -1.0f)),
        MovementSpeed(SPEED),
        MouseSensitivity(SENSITIVITY),
        Zoom(ZOOM)
    {
        Position = position;
        WorldUp = up;
        Yaw = yaw;
        Pitch = pitch;
        updateCameraVectors();
    }

    Camera(float posX, float posY, float posZ,
        float upX, float upY, float upZ,
        float yaw, float pitch)
        : Front(glm::vec3(0.0f, 0.0f, -1.0f)),
        MovementSpeed(SPEED),
        MouseSensitivity(SENSITIVITY),
        Zoom(ZOOM)
    {
        Position = glm::vec3(posX, posY, posZ);
        WorldUp = glm::vec3(upX, upY, upZ);
        Yaw = yaw;
        Pitch = pitch;
        updateCameraVectors();
    }

    // 返回视图矩阵
    glm::mat4 getViewMatrix() {
        return glm::lookAt(Position, Position + Front, Up);
    }

    // 处理键盘输入
    void ProcessKeyboard(Camera_Movement direction, float deltaTime) {
        float velocity = MovementSpeed * deltaTime * 0.3;
        if (direction == FORWARD) // 前移
            Position += Front * velocity;
        if (direction == BACKWARD) // 后移
            Position -= Front * velocity;
        if (direction == LEFTWARD) // 左移
            Position -= Right * velocity;
        if (direction == RIGHTWARD) // 右移
            Position += Right * velocity;
        if (direction == UPWARD)  // 上移
            Position.y += velocity;
        if (direction == DOWNWARD)  // 下移
            Position.y -= velocity;
    }

    // 处理鼠标输入
    void ProcessMouseMovement(float xoffset, float yoffset, GLboolean constrainPitch = true) {
        xoffset *= MouseSensitivity;
        yoffset *= MouseSensitivity;

        Yaw += xoffset;
        Pitch += yoffset;
        // 确保当俯仰角超出范围时，摄像机不会翻转
        if (constrainPitch) {
            if (Pitch > 89.0f)
                Pitch = 89.0f;
            if (Pitch < -89.0f)
                Pitch = -89.0f;
        }
        // 更新相机向量
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

    // 更新相机向量
    void updateCameraVectors() {
        // 计算新的前向量
        glm::vec3 front;
        front.x = cos(glm::radians(Yaw)) * cos(glm::radians(Pitch));
        front.y = sin(glm::radians(Pitch));
        front.z = sin(glm::radians(Yaw)) * cos(glm::radians(Pitch));
        Front = glm::normalize(front);
        // 更新右轴和上轴
        Right = glm::normalize(glm::cross(Front, WorldUp));  
        Up = glm::normalize(glm::cross(Right, Front));
    }

    // 获取投影矩阵
    glm::mat4 Camera::getProjectionMatrix(bool isOrtho)
    {
        if (isOrtho) {
            return this->ortho(-Zoom, Zoom, -Zoom, Zoom, this->zNear, this->zFar);
        }
        else {
            return this->perspective(Zoom, aspect, this->zNear, this->zFar);
        }
    }

    // 正交投影矩阵
    glm::mat4 Camera::ortho(const GLfloat left, const GLfloat right,
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
    glm::mat4 Camera::perspective(const GLfloat fovy, const GLfloat aspect,
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

    glm::mat4 Camera::frustum(const GLfloat left, const GLfloat right,
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
};
#endif