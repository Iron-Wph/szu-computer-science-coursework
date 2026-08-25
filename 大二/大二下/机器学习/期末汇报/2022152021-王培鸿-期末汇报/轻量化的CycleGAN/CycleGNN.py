import tensorflow as tf
import tensorflow.keras as keras
import numpy as np
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing import image
from scipy.linalg import sqrtm
# from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2
# 创建CycleGAN网络模型
class CycleGAN(keras.Model):
    def __init__(self, name='CycleGAN', lambda_cycle=10, lambda_identity=5, trainable=False, dtype='float32'):
        super(CycleGAN, self).__init__(name=name, trainable=trainable, dtype=dtype)

        self.monet_generator_ = Generator(name='Monet_Generator')
        self.monet_discriminator_ = Discriminator(name='Monet_Discriminator')
        self.photo_generator_ = Generator(name='Photo_Generator')
        self.photo_discriminator_ = Discriminator(name='Photo_Discriminator')
        self.lambda_cycle = lambda_cycle
        self.lambda_identity = lambda_identity
        # 加载预训练的 VGG16 模型
        # self.vgg = VGG16(weights='imagenet', include_top=False, input_shape=(256, 256, 3))
        # self.vgg.trainable = False
        self.mobilenet = MobileNetV2(weights='imagenet', include_top=False, input_shape=(128, 128, 3))
        self.mobilenet.trainable = False

    def compile(self, m_gen_optimizer, p_gen_optimizer, m_disc_optimizer, p_disc_optimizer, **kwargs):
        super(CycleGAN, self).compile(**kwargs)
        # 初始化生成器、判别器m的优化器
        self.m_gen_optimizer = m_gen_optimizer
        self.m_disc_optimizer = m_disc_optimizer
        # 初始化生成器、判别器p的优化器
        self.p_gen_optimizer = p_gen_optimizer
        self.p_disc_optimizer = p_disc_optimizer
        # 二分类交叉熵
        self.bce_ = tf.keras.losses.BinaryCrossentropy(from_logits=False)


    # 生成器损失
    def generator_loss_(self, disc_output):
        return self.bce_(tf.ones_like(disc_output), disc_output)

    # 判别器损失
    def discriminator_loss_(self, real_output, fake_output):
        real_loss = self.bce_(tf.ones_like(real_output), real_output)
        fake_loss = self.bce_(tf.zeros_like(fake_output), fake_output)
        return (real_loss + fake_loss)*0.5

    # 循环网络损失
    def cycle_loss_(self, real_image, cycled_image):
        return self.lambda_cycle * tf.reduce_mean(tf.abs(real_image - cycled_image))

    # 身份损失
    def identity_loss_(self, real_image, same_image):
        return self.lambda_identity * tf.reduce_mean(tf.abs(real_image - same_image))

    # 计算感知损失
    def perceptual_loss_(self, real_image, generated_image):
        # 通过vgg预训练网络计算L1 loss
        real_features = self.mobilenet(real_image)
        generated_features = self.mobilenet(generated_image)
        loss = tf.reduce_mean(tf.abs(real_features - generated_features))
        return loss

    # 训练过程
    def train_step(self, batch_data):
        real_monet, real_photo = batch_data
        ### Persistent True to compute multiple gradients for the same tape
        with tf.GradientTape(persistent=True) as tape:
            # 前向传播
            fake_monet = self.monet_generator_(real_photo, training=True)  ## Photo to fake Monet
            cycled_photo = self.photo_generator_(fake_monet, training=True)  ## fake Monet to photo
            fake_photo = self.photo_generator_(real_monet, training=True)  ## Monet to fake photo
            cycled_monet = self.monet_generator_(fake_photo, training=True)  ## fake Photo to Monet

            ### Identity mapping (G(x) to x, F(y) to y)
            same_monet = self.monet_generator_(real_monet, training=True)  ## Monet to monet
            same_photo = self.photo_generator_(real_photo, training=True)  ## Photo to photo

            # 判别器预测，4个判别器
            disc_real_monet = self.monet_discriminator_(real_monet, training=True)  ## Monet is real Monet
            disc_fake_monet = self.monet_discriminator_(fake_monet, training=True)  ## Fake Monet is real Monet
            disc_real_photo = self.photo_discriminator_(real_photo, training=True)  ## Photo is a real photo
            disc_fake_photo = self.photo_discriminator_(fake_photo, training=True)  ## Fake Photo is a real photo

            # 计算损失
            ## Generators
            gen_monet_loss = self.generator_loss_(disc_fake_monet)
            gen_photo_loss = self.generator_loss_(disc_fake_photo)
            ## Discriminators
            disc_monet_loss = self.discriminator_loss_(disc_real_monet, disc_fake_monet)
            disc_photo_loss = self.discriminator_loss_(disc_real_photo, disc_fake_photo)
            
            ### Cycle
            cycle_loss = self.cycle_loss_(real_monet, cycled_monet) + self.cycle_loss_(real_photo, cycled_photo)
            ### Identity
            identity_loss = self.identity_loss_(real_monet, same_monet) + self.identity_loss_(real_photo, same_photo)

#             ### Perceptual
#             perceptual_loss_monet = self.perceptual_loss_(real_monet, fake_monet)
#             perceptual_loss_photo = self.perceptual_loss_(real_photo, fake_photo)

            ### Generators total loss
            total_gen_monet_loss = gen_monet_loss + cycle_loss + identity_loss
            total_gen_photo_loss = gen_photo_loss + cycle_loss + identity_loss

#             # perceptual_loss
#             total_gen_monet_loss = gen_monet_loss + cycle_loss + identity_loss + perceptual_loss_monet
#             total_gen_photo_loss = gen_photo_loss + cycle_loss + identity_loss + perceptual_loss_photo

        # Gradients梯度
        # 计算对应损失函数以及模型可训练参数（卷积层、批归一化层、激活函数等网络层的权重和偏置）
        monet_generator_gradients = tape.gradient(total_gen_monet_loss, self.monet_generator_.trainable_variables)
        photo_generator_gradients = tape.gradient(total_gen_photo_loss, self.photo_generator_.trainable_variables)
        monet_discriminator_gradients = tape.gradient(disc_monet_loss, self.monet_discriminator_.trainable_variables)
        photo_discriminator_gradients = tape.gradient(disc_photo_loss, self.photo_discriminator_.trainable_variables)

        # gradients梯度的反向传播
        # 使用zip将梯度和训练参数打包，并对训练参数进行梯度下降操作
        self.m_gen_optimizer.apply_gradients(zip(monet_generator_gradients, self.monet_generator_.trainable_variables))
        self.p_gen_optimizer.apply_gradients(zip(photo_generator_gradients, self.photo_generator_.trainable_variables))
        self.m_disc_optimizer.apply_gradients(
            zip(monet_discriminator_gradients, self.monet_discriminator_.trainable_variables))
        self.p_disc_optimizer.apply_gradients(
            zip(photo_discriminator_gradients, self.photo_discriminator_.trainable_variables))

        # #
        # # 计算FID
        # fid_score = self.calculate_fid(real_monet, fake_monet) + self.calculate_fid(real_photo, fake_photo)
        # # 计算IS
        # is_score = self.calculate_is(fake_monet) + self.calculate_is(fake_photo)

        return {
            "monet_gen_loss": total_gen_monet_loss,
            "photo_gen_loss": total_gen_photo_loss,
            "monet_disc_loss": disc_monet_loss,
            "photo_disc_loss": disc_photo_loss
            }