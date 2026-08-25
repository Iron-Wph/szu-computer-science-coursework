#include <opencv2/opencv.hpp>  
#include <opencv2/core/core.hpp>  
#include <opencv2/highgui/highgui.hpp>  
#include <opencv2/imgproc.hpp>  
#include <opencv2/imgcodecs.hpp>
#include <iostream>  
#include <math.h>
#include <opencv2/dnn.hpp>
#include <fstream>

#include "Fast_MTCNN.h"
using namespace std;
using namespace cv;
//#pragma comment(lib,"opencv_world450d.lib")

//方便读取数据用的文件名以及每个测试样本对应的测试图像数量
string filename[10] = { "1_BlurFace", "2_ClifBar", "3_David", "4_Dudek", "5_FaceOcc1", "6_FaceOcc2", "7_FleetFace", "8_Girl", "9_Jumping", "10_Mhyang"};
//int totalsum[10] = { 293, 272, 420, 845, 592, 612, 407, 300, 163, 1290 };

vector<Mat>data_Stronger(Mat &image)
{
    vector<Mat>res;
    //顺时针、逆时针45度
    Point2f center(image.cols / 2.0, image.rows / 2.0);
    Mat rotationMatrix = getRotationMatrix2D(center, -45, 1.0);
    Mat rotatedImage1;
    warpAffine(image, rotatedImage1, rotationMatrix, image.size());
    rotationMatrix = getRotationMatrix2D(center, 45, 1.0);
    Mat rotatedImage2;
    warpAffine(image, rotatedImage2, rotationMatrix, image.size());
    res.push_back(rotatedImage1); res.push_back(rotatedImage2);

    //垂直镜像
    Mat mirroredImage;
    flip(image, mirroredImage, 0);
    res.push_back(mirroredImage);

    // 要增强的颜色通道（0：蓝色，1：绿色，2：红色）
    // 增强颜色通道的强度
    Mat redhancedImage = image.clone();
    Mat bluehancedImage = image.clone();
    Mat greenhancedImage = image.clone();
    for (int i = 0; i < image.rows; i++)
    {
        for (int j = 0; j < image.cols; j++)
        {
            //蓝色处理
            Vec3b& pixel0 = bluehancedImage.at<Vec3b>(i, j);
            pixel0[0] = saturate_cast<uchar>(pixel0[0] + 100); // 调整增强强度
            //绿色处理
            Vec3b& pixel1 = greenhancedImage.at<Vec3b>(i, j);
            pixel1[1] = saturate_cast<uchar>(pixel1[1] + 100); // 调整增强强度
            //红色处理
            Vec3b& pixel2 = redhancedImage.at<Vec3b>(i, j);
            pixel2[2] = saturate_cast<uchar>(pixel2[2] + 100); // 调整增强强度
        }
    }
    res.push_back(redhancedImage);
    res.push_back(bluehancedImage);
    res.push_back(greenhancedImage);

    return res;
}

int main()
{
    //30,0.5,0.6,0.7;20,0.6,0.7,0.7
    int minSize = 20;
    MTCNN detector("model");
    //缩放因子，在图像金字塔中对图像进行缩放
    float factor = 0.709f;
    //对应三个阶段的人脸检测器（P-Net、R-Net、O-Net）的置信度阈值。只有置信度高于阈值的人脸框才会被保留。
    float threshold[3] = { 0.6f, 0.7f, 0.7f };

    //std::string dpath = "the0.txt"; // 文件名及路径
    //ofstream file(dpath); // 创建输出文件流对象

    string pre = "D:\\作业\\智能识别系统设计\\实验2\\train\\trainset\\", mid = "\\(", last = ").jpg";

    //保存检测不到人脸的文件路径
    vector<string>failed;

    for (int j = 0; j < 10; j++)
    {
        //file << filename[j] << endl;
        for (int k = 1; k <= 10; k++)
        {
            string filepath = pre + filename[j] + mid + to_string(k) + last;
            cout << filepath << endl;
            Mat image = imread(filepath);
            
            ////从BGR转换为RGB颜色空间
            //cv::cvtColor(image, image, cv::COLOR_BGR2RGB);


            if (image.empty())
                break;


            //检测人脸
            vector<FaceInfo>faceInfo = detector.Detect_mtcnn(image, minSize, threshold, factor, 3);

            //如果检测不到人脸，则跳过/////////////////////
            if (faceInfo.empty())
            {
                failed.push_back(filepath);
                continue;
            }
            Mat show_dis = image.clone();
            for (int i = 0; i < faceInfo.size(); i++)
            {
                int x = (int)faceInfo[i].bbox.xmin;
                int y = (int)faceInfo[i].bbox.ymin;
                int w = (int)(faceInfo[i].bbox.xmax - faceInfo[i].bbox.xmin + 1);
                int h = (int)(faceInfo[i].bbox.ymax - faceInfo[i].bbox.ymin + 1);
                //绘制矩形框
                cv::rectangle(image, cv::Rect(x, y, w, h), cv::Scalar(255, 0, 0), 2);

                // 获取置信度
                float confidence = faceInfo[i].bbox.score;

                // 在矩形框中显示置信度，记录
                std::ostringstream ss;

                ss << "Confidence: " << confidence;
                cv::putText(image, ss.str(), cv::Point(x, y - 10), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 0, 0), 2);
            }
            imshow("quick-test", image);
            //裁剪人脸后显示
            vector<Mat>res = detector.cropFace(show_dis, faceInfo);
            imshow("now", res.front());
            waitKey(10);



            /*vector<Mat>src = data_Stronger(image);
            src.push_back(image);

            //int xu = 0;
            //遍历每张图像
            while (!src.empty())
            {
                Mat dis = src.back();
                Mat show_dis = dis.clone();
                src.pop_back();

                //clock时钟用于计算识别时间
                double start = clock();
                vector<FaceInfo>faceInfo = detector.Detect_mtcnn(dis, minSize, threshold, factor, 3);

                //如果检测不到人脸，则跳过/////////////////////
                if (faceInfo.empty())
                    continue;

                double  end = clock();
                cout << "GetTickCount:" << end - start << endl;
                for (int i = 0; i < faceInfo.size(); i++)
                {
                    int x = (int)faceInfo[i].bbox.xmin;
                    int y = (int)faceInfo[i].bbox.ymin;
                    int w = (int)(faceInfo[i].bbox.xmax - faceInfo[i].bbox.xmin + 1);
                    int h = (int)(faceInfo[i].bbox.ymax - faceInfo[i].bbox.ymin + 1);
                    //绘制矩形框
                    cv::rectangle(image, cv::Rect(x, y, w, h), cv::Scalar(255, 0, 0), 2);

                    // 获取置信度
                    float confidence = faceInfo[i].bbox.score;

                    // 在矩形框中显示置信度，记录
                    std::ostringstream ss;
                    //xu++;
                    file << confidence << "\n";

                    ss << "Confidence: " << confidence;
                    cv::putText(dis, ss.str(), cv::Point(x, y - 10), cv::FONT_HERSHEY_SIMPLEX, 0.6, cv::Scalar(255, 0, 0), 2);
                }
                imshow("quick-test", dis);
                //裁剪人脸后显示
                vector<Mat>res = detector.cropFace(show_dis, faceInfo);
                imshow("now", res.front());
                waitKey(10);
            }*/
            
        }
    }

    //输出不能检测到人脸的图像
    
    if(!failed.empty())
    {
        for (vector<string>::iterator iter = failed.begin(); iter != failed.end(); iter++)
        {
            cout << *iter << endl;
        }
    }



    ////关闭文件
    //file.close();
    return 0;
    /*Mat image;
    int minSize = 40;
    MTCNN detector("model");
    //缩放因子，在图像金字塔中对图像进行缩放
    float factor = 0.709f;
    //对应三个阶段的人脸检测器（P-Net、R-Net、O-Net）的置信度阈值。只有置信度高于阈值的人脸框才会被保留。
    float threshold[3] = { 0.7f, 0.6f, 0.6f };
    int i = 0;
    while (1)
    {
        //cap>>image;
        image = imread("D:\\作业\\智能识别系统设计\\实验2\\train\\testset\\4_Dudek\\test\\(67).jpg");
        //image = imread("test.jpg");
        if (image.empty())
            break;
        
        //clock时钟用于计算识别时间
        double start = clock();
        vector<FaceInfo> faceInfo = detector.Detect_mtcnn(image, minSize, threshold, factor, 3);
        double  end = clock();
        cout << "GetTickCount:" << end - start << endl;
        for (int i = 0; i < faceInfo.size(); i++)
        {
            int x = (int)faceInfo[i].bbox.xmin;
            int y = (int)faceInfo[i].bbox.ymin;
            int w = (int)(faceInfo[i].bbox.xmax - faceInfo[i].bbox.xmin + 1);
            int h = (int)(faceInfo[i].bbox.ymax - faceInfo[i].bbox.ymin + 1);
            //绘制矩形框
            cv::rectangle(image, cv::Rect(x, y, w, h), cv::Scalar(255, 0, 0), 2);
        }
        imshow("quick-test", image);
        //裁剪人脸后显示
        vector<Mat>res = detector.cropFace(image, faceInfo);
        imshow("now", res.front());
        waitKey(0);
    }*/

}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件
