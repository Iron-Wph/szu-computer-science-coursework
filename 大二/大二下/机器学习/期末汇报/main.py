import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import tensorflow as tf
from tensorflow.io.gfile import glob
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from sklearn.decomposition import PCA
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import shutil
import PIL
# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory
import os
## Setting my path to the input file
#os.chdir("/kaggle/input/gan-getting-started")
for dirname, _, filenames in os.walk('/data'):
    print(dirname, len(os.listdir(dirname)))
AUTOTUNE = tf.data.experimental.AUTOTUNE

# 加载图像数据
Monet_files = glob(str('./data/monet_tfrec/*.tfrec'))
print('Monet TFRecord Files:', len(Monet_files))
Photo_files = glob(str('./data/photo_tfrec/*.tfrec'))
print('Photo TFRecord Files:', len(Photo_files))

# 获取特征名字
raw_dataset = tf.data.TFRecordDataset(Monet_files[0])
for raw_record in raw_dataset.take(1):
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())
    Monet_features = [i for i in example.features.feature]

raw_dataset = tf.data.TFRecordDataset(Photo_files[0])
for raw_record in raw_dataset.take(1):
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())
    Photo_features = [i for i in example.features.feature]

print('Monet tfrecord Features:', Monet_features)
print('Photo tfrecord Features:', Photo_features)

IMAGE_SIZE = [256, 256]

def decode_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.reshape(image, [*IMAGE_SIZE, 3])
    return image

def read_tfrecord(example):
    tfrecord_format = {
        "image_name": tf.io.FixedLenFeature([], tf.string),
        "image": tf.io.FixedLenFeature([], tf.string),
        "target": tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image'])
    return image

def load_dataset(filenames, labeled=True, ordered=False, repeat = False):
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=AUTOTUNE)
    if repeat:
        dataset = dataset.repeat(count = 20)
    # 随机打乱样本
    dataset = dataset.shuffle(1000)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return dataset



# 这一部分看到部分的莫奈图片和待转换图像
batch_size = 15
photo_ds = load_dataset(Photo_files, labeled = True).batch(15)
monet_ds = load_dataset(Monet_files, labeled = True, repeat = True).batch(15)
example_monet = next(iter(monet_ds))
example_photo = next(iter(photo_ds))

fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 6))
fig.suptitle('Image Categories', fontsize=16)

for i in range(0,5):
    ax = axes[0, i]
    ax.imshow(example_monet[i])
    ax.axis('off')

for i in range(0,5):
    ax = axes[1, i]
    ax.imshow(example_photo[i])
    ax.axis('off')

axes[0, 2].set_title('Monet', size='large', loc='center')
axes[1, 2].set_title('Photo', size='large', loc='center')
plt.tight_layout()  # Adjust layout to make room for the main title
plt.show()

# 继承keras.layers.Layer类
class Downsample(keras.layers.Layer):
    def __init__(self, filters, kernel_size=(2, 2), strides=(2, 2), padding='same', activation='leaky_relu', **kwargs):
        super(Downsample, self).__init__(**kwargs)
        # 使用tf.random_normal_initializer.RandomNormal来随机初始化权重
        self.initializer = tf.random_normal_initializer(0., 0.02)
        self.gamma_init = keras.initializers.RandomNormal(mean=0.0, stddev=0.02)
        # 初始化一些层,包括keras.layers.Conv2D、keras.layers.BatchNormalization和keras.layers.Activation
        self.conv = layers.Conv2D(filters, kernel_size=kernel_size,
                                  strides=strides, padding=padding, kernel_initializer=self.initializer)
        self.bn = layers.BatchNormalization()
        self.activation = layers.Activation(activation=activation)

    # 定义前向前向传播过程
    def call(self, inputs, training=False):
        x = self.conv(inputs)
        x = self.bn(x, training=training)
        x = self.activation(x)
        return x

    # 返回所有配置参数的字典
    def get_config(self):
        config = super(Downsample, self).get_config()
        config.update({
            'filters': self.conv.filters,
            'kernel_size': self.conv.kernel_size,
            'strides': self.conv.strides,
            'padding': self.conv.padding,
            'activation': self.activation.activation,
        })
        return config

# 将高维的特征图压缩为一维图像
def apply_pca_and_visualize(convolved_images):
    # Flatten the convolved images
    shape = convolved_images.shape
    normalized_image = convolved_images / 255.0
    reshaped_image = tf.reshape(normalized_image, (-1, shape[-1]))
    reshaped_array = reshaped_image.numpy()
    # Apply PCA
    pca = PCA(n_components=1)
    # 保留一个主成分的图像显示
    pca_result = pca.fit_transform(reshaped_array)
    # Reshape back
    pca_image_reshaped = pca_result.reshape(shape[0], shape[1], 1)
    return pca_image_reshaped


# 对Downsample模块的可视化
filters = [32, 64, 128, 256]
convolutions = []
convolutions.append(example_monet)
for count, element in enumerate(filters):
    Block = Downsample(element)
    convolutions.append(Block(convolutions[count]))

fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(15, 3))
fig.suptitle('Downsampling', fontsize=16)

batch_number = 3
## Original visualization
ax = axes[0]
ax.imshow(convolutions[0][batch_number])
axes[0].set_title('Original Monet', size='large', loc='center')

# PCA of original
ax = axes[1]
ax.imshow(apply_pca_and_visualize(convolutions[0][batch_number]) * 255.0, cmap='winter')
axes[1].set_title('PCA', size='large', loc='center')

#
for i in range(1, len(convolutions)):
    ax = axes[i + 1]
    ax.imshow(apply_pca_and_visualize(convolutions[i][batch_number]) * 255.0, cmap='winter')
    axes[i + 1].set_title(f'Downsample {convolutions[i].shape[-1]} filters', size='medium', loc='center')

plt.show()


# 继承keras.layers.Layer类
class Upsample(keras.layers.Layer):
    def __init__(self, filters, kernel_size=(2, 2), strides=(2, 2), padding='same', activation='leaky_relu',
                 dropout=0.2, **kwargs):
        super(Upsample, self).__init__(**kwargs)

        self.initializer = tf.random_normal_initializer(0., 0.02)
        # 转置卷积（Conv2DTranspose）
        self.conv = layers.Conv2DTranspose(filters, kernel_size=kernel_size,
                                           strides=strides, padding=padding, kernel_initializer=self.initializer)
        # 批量归一化
        self.bn = layers.BatchNormalization()
        # dropout随机失活，避免过拟合
        self.dropout = layers.Dropout(dropout)
        # 激活层
        self.activation = layers.Activation(activation=activation)

    # 网络层的前向传播
    def call(self, inputs, training=False, dropout=False):
        # 转置卷积
        x = self.conv(inputs)
        # 批量归一化
        x = self.bn(x, training=training)
        if dropout:
            x = self.dropout(x)
        x = self.activation(x)

        return x

    # 返回序列化层的配置参数
    def get_config(self):
        config = super(Upsample, self).get_config()
        config.update({
            'filters': self.conv.filters,
            'kernel_size': self.conv.kernel_size,
            'strides': self.conv.strides,
            'padding': self.conv.padding,
            'activation': self.activation.activation,
        })
        return config

# 对upsample模块的可视化
upsample_filters = [512, 256, 128, 3]
upsample_test = []
upsample_test.append(convolutions[-1])
for count, element in enumerate(upsample_filters):
    upsample_block = Upsample(element)
    upsample_test.append(upsample_block(upsample_test[count], dropout=True, training=False))

fig, axes = plt.subplots(nrows=1, ncols=6, figsize=(15, 3))
fig.suptitle('Upsampling', fontsize=16)

batch_number = 3

for i in range(0, len(upsample_test) - 1):
    ax = axes[i]
    ax.imshow(apply_pca_and_visualize(upsample_test[i][batch_number]) * 255.0, cmap='winter')
    axes[i].set_title(f'Upsample {upsample_test[i].shape[-1]} filters', size='medium', loc='center')

# PCA of the predicted original
ax = axes[4]
ax.imshow(apply_pca_and_visualize(upsample_test[-1][batch_number]) * 255.0, cmap='winter')
axes[4].set_title('PCA', size='large', loc='center')

# PCA of the predicted original
ax = axes[5]
ax.imshow(upsample_test[-1][batch_number] * 255.0)
axes[5].set_title('Original', size='large', loc='center')

plt.show()


# 生成器继承keras.Model类
class Generator(keras.Model):
    def __init__(self, name='Generator', **kwargs):
        super(Generator, self).__init__(name=name, **kwargs)

        ### Downsampling layers
        # 下采样层，依次将特征图的空间尺寸从（128，128，3）搞到（1，1，512）
        self.downsample1 = Downsample(32, name='Donwsample_128')  ## (bs,128,128,32)
        self.downsample2 = Downsample(64, name='Donwsample_64')  ## (bs,64,64,64)
        self.downsample3 = Downsample(128, name='Donwsample_32')  ## (bs,32,32,128)
        self.downsample4 = Downsample(256, name='Donwsample_16')  ## (bs,16,16,256)
        self.downsample5 = Downsample(512, name='Donwsample_8')  ## (bs,8,8,512)
        self.downsample6 = Downsample(512, name='Donwsample_4')  ## (bs,4,4,512)
        self.downsample7 = Downsample(512, name='Donwsample_2')  ## (bs,2,2,512)
        self.downsample8 = Downsample(512, name='Donwsample_1')  ## (bs,1,1,512)   Goal

        ## Upsampling layers
        # 逐步将压缩的特征图放大到原始输入图像的尺寸
        # 同时通过跳跃连接和 dropout 等方法来丰富特征表达,从而生成高质量的输出图像
        self.upsample1 = Upsample(512, dropout=True, name='Upsample_2')  ## (bs,2,2,512)
        self.upsample2 = Upsample(512, dropout=True, name='Upsample_4')  ## (bs,4,4,512)
        self.upsample3 = Upsample(512, name='Upsample_8')  ## (bs,8,8,512)
        self.upsample4 = Upsample(256, name='Upsample_16')  ## (bs,16,16,256)
        self.upsample5 = Upsample(128, name='Upsample_32')  ## (bs,32,32,128)
        self.upsample6 = Upsample(64, name='Upsample_64')  ## (bs,64,64,64)
        self.upsample7 = Upsample(32, name='Upsample_128')  ## (bs,128,128,32)
        self.final_upsample = Upsample(3, activation='sigmoid', name='Output_layer')  # (bs,256,256,3)

    #
    def call(self, inputs, training=False):
        ### Downsampling
        d1 = self.downsample1(inputs, training=training)
        d2 = self.downsample2(d1, training=training)
        d3 = self.downsample3(d2, training=training)
        d4 = self.downsample4(d3, training=training)
        d5 = self.downsample5(d4, training=training)
        d6 = self.downsample6(d5, training=training)
        d7 = self.downsample7(d6, training=training)
        d8 = self.downsample8(d7, training=training)
        ## Upsampling
        u1 = self.upsample1(d8, training=training)
        # 将u1、d7的结果进行连接，得到新的特征图
        u1_concat = tf.concat([u1, d7], axis=-1)
        u2 = self.upsample2(u1_concat, training=training)
        u2_concat = tf.concat([u2, d6], axis=-1)
        u3 = self.upsample3(u2_concat, training=training)
        u3_concat = tf.concat([u3, d5], axis=-1)
        u4 = self.upsample4(u3_concat, training=training)
        u4_concat = tf.concat([u4, d4], axis=-1)
        u5 = self.upsample5(u4_concat, training=training)
        u5_concat = tf.concat([u5, d3], axis=-1)
        u6 = self.upsample6(u5_concat, training=training)
        u6_concat = tf.concat([u6, d2], axis=-1)
        u7 = self.upsample7(u6_concat, training=training)
        u7_concat = tf.concat([u7, d1], axis=-1)
        x = self.final_upsample(u7_concat, training=training)
        return x

g = Generator()
# 设置优化器为 Adam 优化器,损失函数为均方误差(MSE)
g.compile(optimizer='adam', loss='mse')
x = g(example_photo, training=False)  ## to build the generator you need to pass an input trough the network
g.summary()


# 可视化生成器，因为没有训练所以是黑色图像，只是为了检验图像的大小一致
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 6))
fig.suptitle('Monet Generator', fontsize=16)
ax = axes[0]
ax.imshow(example_photo[1])
axes[0].set_title('Photo', size='large', loc='center')
ax = axes[1]
ax.imshow(x[1])
axes[1].set_title('Photo as a Monet', size='large', loc='center')
plt.show()


# 判别器继承keras.Model类
class Discriminator(keras.Model):
    def __init__(self, name='Discriminator', dense=64, activation='leaky_relu', **kwargs):
        super(Discriminator, self).__init__(name=name, **kwargs)
        # 初始化器为随机正太分布初始化器，均值为0，标准差为0.02
        self.initializer = tf.random_normal_initializer(0., 0.02)
        # 定义下采样层
        self.downsample1 = Downsample(64, name='Downsample_128')  ## (bs,128,128,64)
        self.downsample2 = Downsample(128, name='Downsample_64')  ## (bs, 64,64,128)
        self.downsample3 = Downsample(256, name='Downsample_32')  ## (bs, 32,32,256)
        self.downsample4 = Downsample(256, name='Downsample_16')  ## (bs, 32,32,256)
        # 零填充-->>对卷积后图像边缘进行补0的填充，防止卷积后图像大小改变
        self.zeropad = layers.ZeroPadding2D(name='Zero_Padding')
        self.downsample5 = Downsample(512, strides=(1, 1), kernel_size=(2, 2),
                                      name='Downsample_stride_1')  ## (bs,32,32,512)
        # 展平层，为全连接Dense层准备一维输入
        self.flatten = layers.Flatten(name='Flatten_layer')
        self.dense = layers.Dense(dense, name=f'Hiden_layer_{dense}')
        # dropout层随机丢弃20%的神经元
        self.dropout = layers.Dropout(0.2, name='Dropout')
        self.activation = layers.Activation(activation, name=f'{activation}')
        # 输出只有1个神经元的最终层
        self.last = layers.Dense(1, activation='sigmoid')

    # 前向传播
    def call(self, inputs, training=False):
        x = self.downsample1(inputs, training=training)
        x = self.downsample2(x, training=training)
        x = self.downsample3(x, training=training)
        x = self.downsample4(x, training=training)
        x = self.zeropad(x)
        x = self.downsample5(x, training=training)
        x = self.flatten(x)
        x = self.dense(x)
        x = self.dropout(x)
        x = self.activation(x)
        x = self.last(x)
        return x

# 编译生成器
d = Discriminator()
d.compile(optimizer='adam', loss='mse')
y = d(example_monet, training=False)
d.summary()


# 生成器的损失函数
# 最小化生成器输出与真实样本之间的差异，使得判别器认为生成器生成的样本是真实的
def generator_loss(disc_output):
    ### BinaryCrossentropy二分类交叉熵函数用于二分类问题
    ### 二分类交叉熵用于(1 和 disc_output)之间
    return keras.losses.BinaryCrossentropy(from_logits=False)(tf.ones_like(disc_output), disc_output)

print('Generator loss: ', generator_loss(y))

# 判别器的损失函数
# 最小化这个总损失,即最大化它对真实样本的预测概率,同时最小化它对生成样本的预测概率
def discriminator_loss(real_output, fake_output):
    ### 二分交叉熵函数用于分类为真样本的情况
    real_loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)(tf.ones_like(real_output), real_output)
    ### 二分交叉熵函数用于分类为假样本的情况
    fake_loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss

print('Discriminator loss: ', discriminator_loss(y,y))


# 循环一致性损失：最小化原始图像和循环生成图像之间的差异
def cycle_loss(real_image, cycled_image, lambda_cycle=10):
    # 求取原始图像与循环图像的平均绝对误差 并 乘于权重lambda_cycle
    return lambda_cycle * tf.reduce_mean(tf.abs(real_image - cycled_image))
# 当比较相同的图像时，返回的损失应该是0
print('Cycle loss: ', cycle_loss(x[0], x[0]))


# 身份损失：最小化原始图像和生成器处理后仍然在同一域的图像之间的差异
def identity_loss(real_image, same_image, lambda_identity=5):
    # 真实图像和相同域图像的平均绝对差 并 乘于 权重lambda_identity
    return lambda_identity * tf.reduce_mean(tf.abs(real_image - same_image))

# 当比较相同的图像时，返回的损失应该是0
print('Identity Loss: ', identity_loss(x[0], x[0]))


# 创建CycleGAN网络模型
class CycleGAN(keras.Model):
    def __init__(self, name='CycleGAN', lambda_cycle=10, lambda_identity=5):
        super(CycleGAN, self).__init__(name=name)

        self.monet_generator_ = Generator(name='Monet_Generator')
        self.monet_discriminator_ = Discriminator(name='Monet_Discriminator')
        self.photo_generator_ = Generator(name='Photo_Generator')
        self.photo_discriminator_ = Discriminator(name='Photo_Discriminator')
        self.lambda_cycle = lambda_cycle
        self.lambda_identity = lambda_identity

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
        return real_loss + fake_loss

    # 循环网络损失
    def cycle_loss_(self, real_image, cycled_image):
        return self.lambda_cycle * tf.reduce_mean(tf.abs(real_image - cycled_image))

    # 身份损失
    def identity_loss_(self, real_image, same_image):
        return self.lambda_identity * tf.reduce_mean(tf.abs(real_image - same_image))

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
            ### Generators total loss
            total_gen_monet_loss = gen_monet_loss + cycle_loss + identity_loss
            total_gen_photo_loss = gen_photo_loss + cycle_loss + identity_loss

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

        return {
            "monet_gen_loss": total_gen_monet_loss,
            "photo_gen_loss": total_gen_photo_loss,
            "monet_disc_loss": disc_monet_loss,
            "photo_disc_loss": disc_photo_loss}


# 用于训练过程的可视化
class callbacks(keras.callbacks.Callback):
    def on_epoch_end(self, epoch, logs={}):
        ### Every 5 epochs plot the generator
        randomint = np.random.randint(0,15,1)[0]
        if epoch != 0:
            fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(15, 4))
            fig.suptitle(f'Generator evolution epoch #{epoch}', fontsize=16)
            ax = axes[0]
            ax.imshow(example_photo[randomint])
            axes[0].set_title('Original Photo', size='large', loc='center')
            ax.axis('off')
            ax = axes[1]
            ax.imshow(cycle_gan.monet_generator_(example_photo)[randomint])
            axes[1].set_title('Photo to Monet', size='large', loc='center')
            ax.axis('off')
            ax = axes[2]
            ax.imshow(example_monet[randomint])
            axes[2].set_title('Original Monet', size='large', loc='center')
            ax.axis('off')
            ax = axes[3]
            ax.imshow(cycle_gan.photo_generator_(example_monet)[randomint])
            axes[3].set_title('Monet to photo', size='large', loc='center')
            ax.axis('off')
            plt.savefig(f'{epoch}.png')
            plt.show()
        if epoch == 0:
            fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(15, 4))
            fig.suptitle(f'Starting point', fontsize=16)
            ax = axes[0]
            ax.imshow(example_photo[randomint])
            axes[0].set_title('Original Photo', size='large', loc='center')
            ax.axis('off')
            ax = axes[1]
            ax.imshow(cycle_gan.monet_generator_(example_photo)[randomint])
            axes[1].set_title('Photo to Monet', size='large', loc='center')
            ax.axis('off')
            ax = axes[2]
            ax.imshow(example_monet[randomint])
            axes[2].set_title('Original Monet', size='large', loc='center')
            ax.axis('off')
            ax = axes[3]
            ax.imshow(cycle_gan.photo_generator_(example_monet)[randomint])
            axes[3].set_title('Monet to photo', size='large', loc='center')
            ax.axis('off')
            plt.savefig(f'{epoch}.png')
            plt.show()

callback = callbacks()

# using Adam optimizers
m_gen_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
p_gen_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
m_disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
p_disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

# Creating the model and show the information
cycle_gan = CycleGAN()
cycle_gan.compile(m_gen_opt, p_gen_opt, m_disc_opt, p_disc_opt)
cycle_gan.summary()

# 训练模型
cycle_gan.fit(tf.data.Dataset.zip((monet_ds, photo_ds)), epochs=20, verbose=1, callbacks=callback)

# 对部分的图片进行莫奈风格转换后显示
fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 6))
fig.suptitle('Results', fontsize=16)

monet_results = cycle_gan.monet_generator_(example_photo)[0:5]
for i in range(0,5):
    ax = axes[0, i]
    ax.imshow(example_photo[i])
    ax.axis('off')

for count,element in enumerate(monet_results):
    ax = axes[1, count]
    ax.imshow(element)
    ax.axis('off')

axes[0, 2].set_title('Photos', size='large', loc='center')
axes[1, 2].set_title('Photos as Monet', size='large', loc='center')
plt.tight_layout()  # Adjust layout to make room for the main title
plt.show()

