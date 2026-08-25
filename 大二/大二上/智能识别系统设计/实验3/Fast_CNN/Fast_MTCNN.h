#pragma once
#include <fstream>
#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
using namespace std;
using namespace cv;

const float pnet_stride = 2;
const float pnet_cell_size = 12;
const int pnet_max_detect_num = 5000;				//
//mean & std
const float mean_val = 127.5f;						//均值
const float std_val = 0.0078125f;					//标准差
//minibatch size
const int step_size = 128;							//迭代步长


//名字为FaceBox的人脸框结构体
typedef struct FaceBox {
    //xmin、ymin为矩形的左上角、xmax、ymax为矩形的右上角，都表示框的边界坐标
    //score 表示框的置信度或评分
    float xmin;
    float ymin;
    float xmax;
    float ymax;
    float score;
} FaceBox;

typedef struct FaceInfo {
    //存储人脸框的边界框回归值
    float bbox_reg[4];
    //存储人脸关键点的回归值
    float landmark_reg[10];
    //存储人脸的关键点坐标
    float landmark[10];
    //人脸的边界框
    FaceBox bbox;
} FaceInfo;


//MTCNN模型类
class MTCNN
{
public:
    //MTCNN类的构造方法，传入存放模型的文件路径（model文件夹）
    MTCNN(const string& proto_model_dir);  
    
    //人脸检测操作，根据检测阶段的不同返回不同的检测结果
    vector<FaceInfo>Detect_mtcnn(const cv::Mat& img, const int min_size, const float* threshold, const float factor, const int stage);
    
    //protected:
    //在P_Net层面上，对输入图像上进行多尺度的人脸提取
    vector<FaceInfo> ProposalNet(const cv::Mat& img, int min_size, float threshold, float factor);
    //阶段处理函数 
    vector<FaceInfo> NextStage(const cv::Mat& image, vector<FaceInfo>& pre_stage_res, int input_w, int input_h, int stage_num, const float threshold);
    //对一组人脸框进行边界框回归
    void BBoxRegression(vector<FaceInfo>& bboxes);
    //对一组人脸框进行边界裁剪和并调整为正方形框
    void BBoxPadSquare(vector<FaceInfo>& bboxes, int width, int height);
    //对一组人脸框进行边界裁剪
    void BBoxPad(vector<FaceInfo>& bboxes, int width, int height);
    //根据置信度和回归框生成候选人脸框
    void GenerateBBox(Mat* confidence, Mat* reg_box, float scale, float thresh);
    ////非最大值抑制（NMS）算法，用于在一组候选人脸框中选择最具代表性的人脸框
    std::vector<FaceInfo> NMS(std::vector<FaceInfo>& bboxes, float thresh, char methodType);
    //计算两个矩形框的交并比
    float IoU(float xmin, float ymin, float xmax, float ymax, float xmin_, float ymin_, float xmax_, float ymax_, bool is_iom = false);


    //计算仿射变换矩阵，用于将特征点 feat_points 对齐到标准点 std_points
    Mat getTformMatrix(float* std_points, float* feat_points);
    //使用人脸检测器 fd 检测输入图像中的人脸，然后根据检测到的人脸位置裁剪出人脸图像
    vector<Mat> cropFace(Mat src, vector<FaceInfo>& faces);

//    std::shared_ptr<dnn::Net> PNet_;      //shared_ptr为智能指针类型，会为未被引用的指针进行回收，防止内存泄漏
//    std::shared_ptr<dnn::Net> ONet_;
//    std::shared_ptr<dnn::Net> RNet_;
public:
    //不同阶段的用于人脸检测的神经网络模型
    dnn::Net PNet_;
    dnn::Net RNet_;
    dnn::Net ONet_;

    std::vector<FaceInfo> candidate_boxes_;    //存储候选人脸框的信息
    std::vector<FaceInfo> total_boxes_;        //存储最终人脸框的信息           
};