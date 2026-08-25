#pragma once

#include "TriMesh.h"
#include "Angel.h"
#include "openGLObject.h"
#include "Camera.h"
#include <vector>


class MeshPainter
{

public:
    MeshPainter();
    ~MeshPainter();

    std::vector<std::string> getMeshNames();

    std::vector<TriMesh *> getMeshes();
    std::vector<openGLObject> getOpenGLObj();

	// 读取纹理文件
    void load_texture_STBImage(const std::string &file_name, GLuint& texture);

	// 传递光线材质数据
    void bindLightAndMaterial(TriMesh* mesh, openGLObject& object, Light* light, Camera* camera);

    void bindObjectAndData(TriMesh *mesh, openGLObject &object, const std::string &texture_image, const std::string &vshader, const std::string &fshader);

	// 添加物体
    void addMesh( TriMesh* mesh, const std::string &name, const std::string &texture_image, const std::string &vshader, const std::string &fshader, bool shadow);

	// 绘制物体
    void drawMesh(TriMesh* mesh, openGLObject &object, Light *light, Camera* camera, bool projMode, bool shadow);

	// 绘制多个物体
    void drawMeshes(Light *light, Camera* camera, bool projMode);

	// 清空数据
    void cleanMeshes();

private:
    std::vector<std::string> mesh_names;
    std::vector<TriMesh *> meshes;
    std::vector<openGLObject> opengl_objects;
    std::vector<bool> shadows;
};

