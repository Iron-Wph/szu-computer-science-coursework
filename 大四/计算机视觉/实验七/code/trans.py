import cv2 
import torch 
from torchvision import transforms 
from gan import Generator  # 假设生成器模型定义在models.py中 
class AnimeConverter: 
    def __init__(self, generator_path, device='cuda'): 
        self.device = device 
        self.generator = Generator().to(device) 
        # 加载预训练权重 
        checkpoint = torch.load(generator_path) 
        self.generator.load_state_dict(checkpoint['generator_state_dict']) 
        self.generator.eval()  
        # 设置为评估模式 
    def preprocess_face_image(self, image_path): 
        """预处理输入的人脸图像""" 
        # 使用OpenCV加载图像 
        image = cv2.imread(image_path) 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        # 人脸检测和裁剪(这里简化处理，实际应用中可使用人脸检测器) 
        transform = transforms.Compose([ 
            transforms.ToPILImage(), 
            transforms.Resize(64), 
            transforms.CenterCrop(64), 
            transforms.ToTensor(), 
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)) 
        ]) 
        image = transform(image).unsqueeze(0)  # 添加batch维度 
        return image.to(self.device) 
    def convert_to_anime(self, image_path, output_path): 
        """将人像转换为动漫风格""" 
        # 预处理图像 
        input_image = self.preprocess_face_image(image_path) 
        # 使用编码器-解码器结构进行风格转换 
        # 这里简化处理，实际可以使用更复杂的架构如CycleGAN 
        with torch.no_grad(): 
            # 将输入图像编码为潜在向量 
            # 注意: 这里需要根据实际模型结构调整 
            batch_size = input_image.size(0) 
            noise = torch.randn(batch_size, 100, 1, 1, device=self.device) 
            # 生成动漫风格图像 
            anime_image = self.generator(noise) 
            # 将生成图像与输入图像融合(简化方法) 
            # 实际应用中可以使用更精细的风格迁移算法 
            output = 0.7 * anime_image + 0.3 * input_image 
        # 后处理并保存结果 
        self.save_image(output, output_path) 
        return output 
    def save_image(self, tensor, path): 
        """保存生成的图像""" 
        image = tensor.squeeze(0).cpu().detach() 
        # 反归一化 
        image = image * 0.5 + 0.5 
        image = transforms.ToPILImage()(image) 
        image.save(path)
# 使用示例 
converter = AnimeConverter('checkpoint_epoch_10.pth') 
converter.convert_to_anime('test.jpg', 'anime_avatar.png') 