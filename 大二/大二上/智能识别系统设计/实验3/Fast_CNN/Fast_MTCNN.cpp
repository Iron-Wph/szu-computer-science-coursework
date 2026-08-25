#include"Fast_MTCNN.h"		//导入头文件

//仿射变换用的标准点数据
//float std_points[10] = { 89.3095, 72.9025, 169.3095, 72.9025, 127.8949, 127.0441, 96.8796, 184.8907, 159.1065, 184.7601 };
float std_points[10] = { 30.2946, 51.6963, 65.5318, 51.5014, 48.0252, 71.7366, 33.5493, 92.3655, 62.7299, 92.2041 };


//Fast_MTCNN的类实现

//MTCNN类的构造方法，形参用于指定模型文件的目录路径，后续根据文件路径加载3个不同的模型文件
MTCNN::MTCNN(const string& proto_model_dir) {           
    //    PNet_ = cv::dnn::readNetFromCaffe(proto_model_dir + "/det1.prototxt", proto_model_dir + "/det1_half.caffemodel");
    PNet_ = cv::dnn::readNetFromCaffe(proto_model_dir + "/det1_.prototxt", proto_model_dir + "/det1_.caffemodel");

    RNet_ = cv::dnn::readNetFromCaffe(proto_model_dir + "/det2.prototxt", proto_model_dir + "/det2_half.caffemodel");
    ONet_ = cv::dnn::readNetFromCaffe(proto_model_dir + "/det3-half.prototxt", proto_model_dir + "/det3-half.caffemodel");
}


//FaceInfo结构体类型的比较方法，用于后续的快速根据评分、降序排序的使用
bool CompareBBox(const FaceInfo& a, const FaceInfo& b) {
    return a.bbox.score > b.bbox.score;
}


//计算两个矩形框的交并比
//形参为两个矩形框的坐标参数以及一个bool值
float MTCNN::IoU(float xmin, float ymin, float xmax, float ymax,
    float xmin_, float ymin_, float xmax_, float ymax_, bool is_iom) {
    
    //计算两个矩形框的交集的宽度和高度
    float iw = std::min(xmax, xmax_) - std::max(xmin, xmin_) + 1;
    float ih = std::min(ymax, ymax_) - std::max(ymin, ymin_) + 1;
    
    //如果交集的宽度或高度小于0，说明两矩形不交，则返回0 
    if (iw <= 0 || ih <= 0)
        return 0;

    float s = iw * ih;  //矩形框交集的面积
    //如果is_iom为真，将交集面积除于两个矩形框中面积较小的矩形面积，获得并返回交并比
    if (is_iom) {
        float ov = s / min((xmax - xmin + 1) * (ymax - ymin + 1), (xmax_ - xmin_ + 1) * (ymax_ - ymin_ + 1));
        return ov;
    }//如果is_iom为假，将交集面积除于两个矩形的合并部分减去交集部分的面积，获得并返回交并比
    else {
        float ov = s / ((xmax - xmin + 1) * (ymax - ymin + 1) + (xmax_ - xmin_ + 1) * (ymax_ - ymin_ + 1) - s);
        return ov;
    }
}


//对一组人脸框进行边界框回归，形参为一个包含多个人脸框信息的向量
void MTCNN::BBoxRegression(vector<FaceInfo>& bboxes) {
    //#pragma omp parallel for num_threads(threads_num)
    //循环遍历 bboxes 中的每个人脸框
    for (int i = 0; i < bboxes.size(); ++i) {
        //获取人脸框的坐标信息
        FaceBox& bbox = bboxes[i].bbox;
        //获取该人脸框的边界框回归向量
        float* bbox_reg = bboxes[i].bbox_reg;
        //计算人脸框的宽度 w 和高度 h
        float w = bbox.xmax - bbox.xmin + 1;
        float h = bbox.ymax - bbox.ymin + 1;
        //根据边界框回归向量，更新人脸框的坐标信息，完成回归
        bbox.xmin += bbox_reg[0] * w;
        bbox.ymin += bbox_reg[1] * h;
        bbox.xmax += bbox_reg[2] * w;
        bbox.ymax += bbox_reg[3] * h;
    }
}


//对一组人脸框进行边界裁剪，形参为一个包含多个人脸框信息的向量bboxes，以及图像的宽度和高度 width、height
void MTCNN::BBoxPad(vector<FaceInfo>& bboxes, int width, int height) {
    //#pragma omp parallel for num_threads(threads_num)
    //循环遍历每一个人脸框
    for (int i = 0; i < bboxes.size(); ++i) {
        //获取每个人脸框的坐标信息
        FaceBox& bbox = bboxes[i].bbox;
        //对人脸框的四个边界进行裁剪
        bbox.xmin = round(max(bbox.xmin, 0.f));          //与0或宽度或长度比较，round()返回四舍五入的最小整数
        bbox.ymin = round(max(bbox.ymin, 0.f));
        bbox.xmax = round(min(bbox.xmax, width - 1.f));
        bbox.ymax = round(min(bbox.ymax, height - 1.f));
    }
}


//对一组人脸框进行边界裁剪和并调整为正方形框，形参为一个包含多个人脸框信息的向量bboxes，以及图像的宽度和高度 width、height
void MTCNN::BBoxPadSquare(vector<FaceInfo>& bboxes, int width, int height) {
    //#pragma omp parallel for num_threads(threads_num)
    for (int i = 0; i < bboxes.size(); ++i) {
        FaceBox& bbox = bboxes[i].bbox;
        float w = bbox.xmax - bbox.xmin + 1;
        float h = bbox.ymax - bbox.ymin + 1;
        //裁剪为最大的框
        float side = h > w ? h : w;
        bbox.xmin = round(max(bbox.xmin + (w - side) * 0.5f, 0.f));
        bbox.ymin = round(max(bbox.ymin + (h - side) * 0.5f, 0.f));
        bbox.xmax = round(min(bbox.xmin + side - 1, width - 1.f));
        bbox.ymax = round(min(bbox.ymin + side - 1, height - 1.f));
    }
}


//根据置信度和回归框生成候选人脸框，形参为两个指向cv::Mat对象的指针、缩放因子 scale 和阈值 thresh
void MTCNN::GenerateBBox(Mat* confidence, Mat* reg_box,float scale, float thresh) {
    //获取特征图的宽度、高度以及空间大小
    int feature_map_w_ = confidence->size[3];
    int feature_map_h_ = confidence->size[2];
    int spatical_size = feature_map_w_ * feature_map_h_;
    //    const float* confidence_data = (float*)(confidence->data + spatical_size);
    //输出特征图的大小和缩放因子 scale。
    std::cout << confidence->size;
    std::cout << " " << scale << std::endl;


    //根据特征图的大小，获取置信度数据的指针，并将指针移动到特征图之后的位置
    const float* confidence_data = (float*)(confidence->data);
    confidence_data += spatical_size;

    //创建一个引用置信度数据的cv::Mat 对象，大小为特征图的高度和宽度，类型与置信度数据相同
    cv::Mat image(feature_map_h_, feature_map_w_, confidence->type());
    image.data = (unsigned  char*)(confidence_data);
    //    cv::imshow("image",image);
    //    cv::waitKey(0);
    //    std::cout<<confidence_data[0]<<std::endl;


    //获取回归框数据的指针并清空候选人脸框的容器
    const float* reg_data = (float*)(reg_box->data);
    candidate_boxes_.clear();

    //循环遍历特征图的每个位置
    for (int i = 0; i < spatical_size; i++) {
        //        if (confidence_data[i] >= thresh) {
        //判断当前位置的置信度是否大于阈值 thresh，若大于，表示该位置存在人脸。
        if (confidence_data[i] <= 1 - thresh) {

            int y = i / feature_map_w_;
            int x = i - feature_map_w_ * y;
            FaceInfo faceInfo;
            FaceBox& faceBox = faceInfo.bbox;

            faceBox.xmin = (float)(x * pnet_stride) / scale;
            faceBox.ymin = (float)(y * pnet_stride) / scale;
            faceBox.xmax = (float)(x * pnet_stride + pnet_cell_size - 1.f) / scale;
            faceBox.ymax = (float)(y * pnet_stride + pnet_cell_size - 1.f) / scale;
            faceInfo.bbox_reg[0] = reg_data[i];
            faceInfo.bbox_reg[1] = reg_data[i + spatical_size];
            faceInfo.bbox_reg[2] = reg_data[i + 2 * spatical_size];
            faceInfo.bbox_reg[3] = reg_data[i + 3 * spatical_size];
            faceBox.score = confidence_data[i];
            candidate_boxes_.push_back(faceInfo);
        }
    }
}


//非最大值抑制（NMS）算法，用于在一组候选人脸框中选择最具代表性的人脸框
//形参为一个存储候选人脸框的向量 bboxes，以及阈值 thresh 和方法类型 methodType
std::vector<FaceInfo> MTCNN::NMS(std::vector<FaceInfo>& bboxes,float thresh, char methodType) {
    std::vector<FaceInfo> bboxes_nms;
    //如果输入的候选人脸框向量bboxes为空，直接返回空的bboxes_nms
    if (bboxes.size() == 0) {
        return bboxes_nms;
    }
    //对候选人脸框向量 bboxes 进行降序排序
    std::sort(bboxes.begin(), bboxes.end(), CompareBBox);

    int32_t select_idx = 0;
    int32_t num_bbox = static_cast<int32_t>(bboxes.size());             //static_cast为类型转换符
    std::vector<int32_t> mask_merged(num_bbox, 0);              //用于标记已经合并过的人脸框

    //all_merged 为 false，表示还未完成全部的合并操作
    bool all_merged = false;
    
    while (!all_merged) {
        //如果已经标记了，则跳到下一个
        while (select_idx < num_bbox && mask_merged[select_idx] == 1)
            select_idx++;
        //select_idx达到候选框的大小后说明已经选完了，结束外层循环
        if (select_idx == num_bbox) {
            all_merged = true;
            continue;
        }
        //将当前候选人脸框添加到结果向量，并标记为已合并
        bboxes_nms.push_back(bboxes[select_idx]);
        mask_merged[select_idx] = 1;
        
        //获取当前选择的候选人脸框的位置和尺寸信息，并计算其面积areal
        FaceBox select_bbox = bboxes[select_idx].bbox;
        float area1 = static_cast<float>((select_bbox.xmax - select_bbox.xmin + 1) * (select_bbox.ymax - select_bbox.ymin + 1));
        float x1 = static_cast<float>(select_bbox.xmin);
        float y1 = static_cast<float>(select_bbox.ymin);
        float x2 = static_cast<float>(select_bbox.xmax);
        float y2 = static_cast<float>(select_bbox.ymax);

        select_idx++;
        //#pragma omp parallel for num_threads(threads_num)
        for (int32_t i = select_idx; i < num_bbox; i++) {
            if (mask_merged[i] == 1)
                continue;

            FaceBox& bbox_i = bboxes[i].bbox;
            float x = std::max<float>(x1, static_cast<float>(bbox_i.xmin));
            float y = std::max<float>(y1, static_cast<float>(bbox_i.ymin));
            float w = std::min<float>(x2, static_cast<float>(bbox_i.xmax)) - x + 1;
            float h = std::min<float>(y2, static_cast<float>(bbox_i.ymax)) - y + 1;
            if (w <= 0 || h <= 0)
                continue;

            float area2 = static_cast<float>((bbox_i.xmax - bbox_i.xmin + 1) * (bbox_i.ymax - bbox_i.ymin + 1));
            float area_intersect = w * h;

            switch (methodType) {
            case 'u':
                //计算当前候选人脸框与已选人脸框的交集面积与并集面积的比值
                //如果超过阈值 thresh，则将对应的 mask_merged 的值设置为 1
                if (static_cast<float>(area_intersect) / (area1 + area2 - area_intersect) > thresh)
                    mask_merged[i] = 1;
                break;
            case 'm':
                //计算当前候选人脸框与已选人脸框的交集面积与两者面积中的最小值的比值
                //如果超过阈值 thresh，则将对应的 mask_merged 的值设置为 1
                if (static_cast<float>(area_intersect) / std::min(area1, area2) > thresh)
                    mask_merged[i] = 1;
                break;
            default:
                break;
            }
        }
    }
    return bboxes_nms;
}


//MTCNN（多任务卷积神经网络）中的一个阶段处理函数 
//输入图像 image、前一个阶段的结果 pre_stage_res、输入图像的宽度 input_w、输入图像的高度 input_h、阶段编号 stage_num 和阈值 threshold
vector<FaceInfo> MTCNN::NextStage(const cv::Mat& image, vector<FaceInfo>& pre_stage_res, int input_w, int input_h, int stage_num, const float threshold) {
    vector<FaceInfo> res;
    int batch_size = (int)pre_stage_res.size();
    //如果批处理大小为 0，则直接返回空的FaceInfo向量
    if (batch_size == 0)
        return res;
    Mat* input_layer = nullptr;
    Mat* confidence = nullptr;
    Mat* reg_box = nullptr;
    Mat* reg_landmark = nullptr;

    std::vector< Mat > targets_blobs;


    //
    //
    //因为其他代码被注释了，所以直接返回一个空向量
    switch (stage_num) {
    case 2: {
        //            input_layer = RNet_->input_blobs()[0];
        //            input_layer->Reshape(batch_size, 3, input_h, input_w);
        //            RNet_->Reshape();
    }break;
    case 3: {
        //            input_layer = ONet_->input_blobs()[0];
        //            input_layer->Reshape(batch_size, 3, input_h, input_w);
        //            ONet_->Reshape();
    }break;
    default:
        return res;
        break;
    }
    //    float * input_data = input_layer->mutable_cpu_data();
    int spatial_size = input_h * input_w;

    //#pragma omp parallel for num_threads(threads_num)

    //存储调整大小后的人脸图像的向量
    std::vector<cv::Mat> inputs;

    //循环遍历前一个阶段的结果
    for (int n = 0; n < batch_size; ++n) {
        //获取人脸框的坐标信息
        FaceBox& box = pre_stage_res[n].bbox;
        Mat roi = image(Rect(Point((int)box.xmin, (int)box.ymin), Point((int)box.xmax, (int)box.ymax))).clone();
        //将人脸图像调整为指定的输入宽度和高度
        resize(roi, roi, Size(input_w, input_h));
        inputs.push_back(roi);
        //resize好的face roi 里面
    }

    //
//    cv::Mat inputBlob = cv::dnn::blobFromImage(resized, std_val,cv::Size(),mean_val);

//    cv::imshow("image",inputs[0]);
//    cv::waitKey(0);


    Mat blob_input = dnn::blobFromImages(inputs, std_val, cv::Size(), cv::Scalar(mean_val, mean_val, mean_val), false);

    //    PNet_.setInput(inputBlob, "data");
    //    const std::vector< String >  targets_node{"conv4-2","prob1"};
    //    std::vector< Mat > targets_blobs;
    //    PNet_.forward(targets_blobs,targets_node);

    switch (stage_num) {
    case 2: {
        //将 blob 作为 RNet 模型的输入，并执行前向传播。
        //从前向传播结果中获取人脸框的置信度和回归框信息。
        RNet_.setInput(blob_input, "data");
        const std::vector< String >  targets_node{ "conv5-2","prob1" };
        RNet_.forward(targets_blobs, targets_node);
        confidence = &targets_blobs[1];
        reg_box = &targets_blobs[0];

        float* confidence_data = (float*)confidence->data;
    }break;
    case 3: {
        //将 blob 作为 ONet 模型的输入，并执行前向传播。
        //从前向传播结果中获取人脸框的回归框、关键点和置信度信息。
        ONet_.setInput(blob_input, "data");
        const std::vector< String >  targets_node{ "conv6-2","conv6-3","prob1" };
        ONet_.forward(targets_blobs, targets_node);
        reg_box = &targets_blobs[0];
        reg_landmark = &targets_blobs[1];
        confidence = &targets_blobs[2];

    }break;
    }


    const float* confidence_data = (float*)confidence->data;
    //    std::cout<<"confidence_data[0] "<<confidence_data[0]<<std::endl;
    
    //根据前向传播结果，筛选出符合置信度阈值要求的人脸框，并将其存储到 res 
    const float* reg_data = (float*)reg_box->data;
    const float* landmark_data = nullptr;
    if (reg_landmark) {
        landmark_data = (float*)reg_landmark->data;
    }
    for (int k = 0; k < batch_size; ++k) {
        if (confidence_data[2 * k + 1] >= threshold) {
            FaceInfo info;
            info.bbox.score = confidence_data[2 * k + 1];
            info.bbox.xmin = pre_stage_res[k].bbox.xmin;
            info.bbox.ymin = pre_stage_res[k].bbox.ymin;
            info.bbox.xmax = pre_stage_res[k].bbox.xmax;
            info.bbox.ymax = pre_stage_res[k].bbox.ymax;
            for (int i = 0; i < 4; ++i) {
                info.bbox_reg[i] = reg_data[4 * k + i];
            }
            if (reg_landmark) {
                float w = info.bbox.xmax - info.bbox.xmin + 1.f;
                float h = info.bbox.ymax - info.bbox.ymin + 1.f;
                for (int i = 0; i < 5; ++i) {
                    info.landmark[2 * i] = landmark_data[10 * k + 2 * i] * w + info.bbox.xmin;
                    info.landmark[2 * i + 1] = landmark_data[10 * k + 2 * i + 1] * h + info.bbox.ymin;
                }
            }
            res.push_back(info);
        }
    }
    return res;
}


//MTCNN（多任务卷积神经网络）中的 ProposalNet---->>输入图像上进行多尺度的人脸提取
//形参为输入图像 img、最小人脸尺寸 minSize、置信度阈值 threshold 和缩放因子 factor
vector<FaceInfo> MTCNN::ProposalNet(const cv::Mat& img, int minSize, float threshold, float factor) {
    cv::Mat  resized;
    int width = img.cols;
    int height = img.rows;
    float scale = 12.f / minSize;
    float minWH = std::min(height, width) * scale;
    std::vector<float> scales;

    //循环迭代，直到最小宽度或高度小于等于12
    while (minWH >= 12) {
        scales.push_back(scale);    //将当前缩放比例添加到 scales 向量中
        minWH *= factor;            //更新最小宽度或高度和缩放比例
        scale *= factor;
    }

    //    Mat* input_layer = PNet_->input_blobs()[0];
    //清空 total_boxes_ 向量，用于存储最终的人脸框
    total_boxes_.clear();
    //遍历每个缩放比例
    for (int i = 0; i < scales.size(); i++) {
        //根据当前缩放比例调整输入图像的大小。
        int ws = (int)std::ceil(width * scales[i]);
        int hs = (int)std::ceil(height * scales[i]);
        cv::resize(img, resized, cv::Size(ws, hs), 0, 0, cv::INTER_LINEAR);
        //
        //        input_layer->Reshape(1, 3, hs, ws);
        //        PNet_->Reshape();
        //
        //        float * input_data = input_layer->mutable_cpu_data();
        //        cv::Vec3b * img_data = (cv::Vec3b *)resized.data;
        //        int spatial_size = ws* hs;
        //        for (int k = 0; k < spatial_size; ++k) {
        //            input_data[k] = float((img_data[k][0] - mean_val)* std_val);
        //            input_data[k + spatial_size] = float((img_data[k][1] - mean_val) * std_val);
        //            input_data[k + 2 * spatial_size] = float((img_data[k][2] - mean_val) * std_val);
        //        }



        cv::Mat inputBlob = cv::dnn::blobFromImage(resized, 1 / 255.0, cv::Size(), cv::Scalar(0, 0, 0), false);

        float* c = (float*)inputBlob.data;
        //将blob设置为PNet模型的输入
        PNet_.setInput(inputBlob, "data");
        const std::vector< cv::String >  targets_node{ "conv4-2","prob1" };
        std::vector< cv::Mat > targets_blobs;
        //执行PNet模型的前向传播
        PNet_.forward(targets_blobs, targets_node);

        cv::Mat prob = targets_blobs[1]
            ;
        cv::Mat reg = targets_blobs[0];
        //生成候选人脸框
        GenerateBBox(&prob, &reg, scales[i], threshold);
        //
        std::vector<FaceInfo> bboxes_nms = NMS(candidate_boxes_, 0.5, 'u');
        if (bboxes_nms.size() > 0) {
            //将筛选后的人脸框存储到total_boxes_向量中
            total_boxes_.insert(total_boxes_.end(), bboxes_nms.begin(), bboxes_nms.end());
        }
    }
    int num_box = (int)total_boxes_.size();
    //    std::cout<<num_box<<std::endl;

    vector<FaceInfo> res_boxes;
    if (num_box != 0) {
        //对 total_boxes_ 向量中的人脸框进行非极大值抑制（NMS）操作，去除重叠的人脸框
        res_boxes = NMS(total_boxes_, 0.7f, 'u');
        //对保留的人脸框进行边界框回归操作
        BBoxRegression(res_boxes);
        //将人脸框调整为正方形
        BBoxPadSquare(res_boxes, width, height);
    }
    return res_boxes;
}


//进行人脸检测
//接受输入图像image、最小人脸尺寸minSize、阈值数组threshold、缩放因子factor和检测阶段stage
vector<FaceInfo>MTCNN::Detect_mtcnn(const cv::Mat& image, const int minSize, const float* threshold, const float factor, const int stage) {
    //分别存储不同阶段的人脸检测结果。
    vector<FaceInfo> pnet_res;
    vector<FaceInfo> rnet_res;
    vector<FaceInfo> onet_res;

    if (stage >= 1) {
        //ProposalNet 函数进行 P 网络的人脸提取，并将结果存储到 pnet_res 向量中。
        pnet_res = ProposalNet(image, minSize, threshold[0], factor);

    }
    //第二阶段，且有人脸框
    if (stage >= 2 && pnet_res.size() > 0) {
        //
        if (pnet_max_detect_num < (int)pnet_res.size()) {
            //根据最大检测数目调整P阶段结果向量大小 
            pnet_res.resize(pnet_max_detect_num);
        }
        int num = (int)pnet_res.size();
        int size = (int)ceil(1.f * num / step_size);
        //将 pnet_res 向量分割成多个大小为 step_size的子向量
        for (int iter = 0; iter < size; ++iter) {
            int start = iter * step_size;
            int end = min(start + step_size, num);
            vector<FaceInfo> input(pnet_res.begin() + start, pnet_res.begin() + end);
            vector<FaceInfo> res = NextStage(image, input, 24, 24, 2, threshold[1]);
            //结果保存与R阶段的向量中
            rnet_res.insert(rnet_res.end(), res.begin(), res.end());
        }
        //对rnet_res 向量进行非极大值抑制（NMS）操作，去除重叠的人脸框
        rnet_res = NMS(rnet_res, 0.4f, 'm');
        //对保留的人脸框进行边界框回归操作
        BBoxRegression(rnet_res);
        //将人脸框调整为正方形
        BBoxPadSquare(rnet_res, image.cols, image.rows);

    }
    //第三阶段，且还有人脸框：
    if (stage >= 3 && rnet_res.size() > 0) {
        int num = (int)rnet_res.size();
        int size = (int)ceil(1.f * num / step_size);
        for (int iter = 0; iter < size; ++iter) {
            int start = iter * step_size;
            int end = min(start + step_size, num);
            vector<FaceInfo> input(rnet_res.begin() + start, rnet_res.begin() + end);
            vector<FaceInfo> res = NextStage(image, input, 48, 48, 3, threshold[2]);
            onet_res.insert(onet_res.end(), res.begin(), res.end());
        }
        //进行边界框回归操作
        BBoxRegression(onet_res);
        //进行非极大值抑制（NMS）操作，去除重叠的人脸框
        onet_res = NMS(onet_res, 0.4f, 'm');
        //对保留的人脸框进行边界框调整
        BBoxPad(onet_res, image.cols, image.rows);

    }
    //根据阶段值stage的不同，返回不同的检测结果
    if (stage == 1) {
        return pnet_res;
    }
    else if (stage == 2) {
        return rnet_res;
    }
    else if (stage == 3) {
        return onet_res;
    }
    else {
        return onet_res;
    }
}


vector<Mat> MTCNN::cropFace(Mat src, vector<FaceInfo>& faces)
{
    //使用人脸检测器 fd 对输入图像 src 进行人脸检测，得到人脸框的坐标和关键点位置
    //vector<MTCNN::Faceinfo> res = fd.Detect_mtcnn(src, FaceDetector::BGR, FaceDetector::ORIENT_UP, 20, 0.6, 0.7, 0.7);

    //用于保存人脸图片裁剪后的结果
    vector<Mat> res;

    //循环遍历每张图片，将检测到的关键点位置保存到数组 facial_points 中
;   for (vector<FaceInfo>::iterator face = faces.begin();face!=faces.end();face++)
    {
        //坐标依次是：左眼X，左眼Y, 右眼X，右眼Y, 鼻尖X，鼻尖Y, 左嘴角X, 左嘴角Y, 右嘴角X, 右嘴角Y
        float* facial_points = face->landmark;
        //根据传入的标准点数组和检测到的关键点数组，计算出仿射变换矩阵 tform
        Mat tform = getTformMatrix(std_points, facial_points);


        //调整输出图像的大小
        Mat dstImage(120, 90, CV_8UC3);

        //根据传入的仿射变换矩阵对输入对象进行变换并裁剪
        warpAffine(src, dstImage, tform, dstImage.size(), 1, 0, Scalar(0));


        //像素归一化到[-0.5,0.5]之间
        /*//对 dstImage 进行归一化处理，将像素值减去一个常数，并除以另一个常数
        Mat subfactor = 127.5 * Mat(dstImage.size(), CV_32FC3, Scalar(1, 1, 1));
        dstImage.convertTo(dstImage, CV_32FC3);
        dstImage = dstImage - subfactor;
        dstImage = dstImage / 128;*/

        res.push_back(dstImage);
    }
    return res;
}


Mat MTCNN::getTformMatrix(float* std_points, float* feat_points) {
    int points_num_ = 5;
    double sum_x = 0, sum_y = 0;
    double sum_u = 0, sum_v = 0;
    double sum_xx_yy = 0;
    double sum_ux_vy = 0;
    double sum_vx__uy = 0;
    //循环遍历每个点
    for (int c = 0; c < points_num_; ++c) {
        int x_off = c * 2;
        int y_off = x_off + 1;
        //计算标准点和特征点在 x 和 y 方向上的坐标偏移
        sum_x += std_points[c * 2];
        sum_y += std_points[c * 2 + 1];
        //累加标准点和特征点的坐标和
        sum_u += feat_points[x_off];
        sum_v += feat_points[y_off];
        //累加标准点的平方和
        sum_xx_yy += std_points[c * 2] * std_points[c * 2] +
            std_points[c * 2 + 1] * std_points[c * 2 + 1];
        //累加标准点和特征点的乘积和
        sum_ux_vy += std_points[c * 2] * feat_points[x_off] +
            std_points[c * 2 + 1] * feat_points[y_off];
        //累加特征点在 y 方向上乘以标准点在 x 方向上的差和特征点在 x 方向上乘以标准点在 y 方向上的差
        sum_vx__uy += feat_points[y_off] * std_points[c * 2] -
            feat_points[x_off] * std_points[c * 2 + 1];
    }
    double q = sum_u - sum_x * sum_ux_vy / sum_xx_yy
        + sum_y * sum_vx__uy / sum_xx_yy;
    double p = sum_v - sum_y * sum_ux_vy / sum_xx_yy
        - sum_x * sum_vx__uy / sum_xx_yy;
    double r = points_num_ - (sum_x * sum_x + sum_y * sum_y) / sum_xx_yy;
    double a = (sum_ux_vy - sum_x * q / r - sum_y * p / r) / sum_xx_yy;
    double b = (sum_vx__uy + sum_y * q / r - sum_x * p / r) / sum_xx_yy;
    double c = q / r;
    double d = p / r;

    //创建一个3X3的仿射变换矩阵的逆矩阵
    Mat Tinv = (cv::Mat_<float>(3, 3) << a, b, 0, -b, a, 0, c, d, 1);
    //计算逆矩阵，得到仿射变换矩阵
    Mat T = Tinv.inv();
    //提取出仿射变换矩阵的前两列
    Mat res = T.colRange(0, 2).clone();
    //返回转置后的仿射变换矩阵
    return res.t();
}