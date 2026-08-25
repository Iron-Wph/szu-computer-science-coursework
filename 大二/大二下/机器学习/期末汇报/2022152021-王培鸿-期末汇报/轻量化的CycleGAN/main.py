import numpy as np # linear algebra
from tensorflow.io.gfile import glob
import matplotlib.pyplot as plt
import tensorflow.keras as keras
import os
from CycleGNN import CycleGAN
from Downsample import Downsample
from Upsample import Upsample
from load_data import *
from PCA import *
from Generator import Generator
from Discriminator import Discriminator
from Loss import *
import tensorflow_probability as tfp

## Setting my path to the input file
#os.chdir("/kaggle/input/gan-getting-started")
for dirname, _, filenames in os.walk('/data'):
    print(dirname, len(os.listdir(dirname)))


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



# 每64张图片作为一个batch
batch_size = 64
photo_ds = load_dataset(Photo_files, labeled=True).batch(batch_size)
monet_ds = load_dataset(Monet_files, labeled=True, repeat=True).batch(batch_size)
# 获取一个batch的数据
example_monet = next(iter(monet_ds))
example_photo = next(iter(photo_ds))

fig, axes = plt.subplots(nrows=2, ncols=5, figsize=(15, 6))
fig.suptitle('Image Categories', fontsize=16)

for i in range(0, 5):
    ax = axes[0, i]
    ax.imshow(example_monet[i])
    ax.axis('off')

for i in range(0, 5):
    ax = axes[1, i]
    ax.imshow(example_photo[i])
    ax.axis('off')

axes[0, 2].set_title('Monet', size='large', loc='center')
axes[1, 2].set_title('Photo', size='large', loc='center')
# 自动调整子图的间距
plt.tight_layout()
plt.show()



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




# 编译生成器
d = Discriminator()
d.compile(optimizer='adam', loss='mse')
y = d(example_monet, training=False)
d.summary()

# 损失函数的测试
print('Generator loss: ', generator_loss(y))

print('Discriminator loss: ', discriminator_loss(y,y))

# 当比较相同的图像时，返回的损失应该是0
print('Cycle loss: ', cycle_loss(x[0], x[0]))

# 当比较相同的图像时，返回的损失应该是0
print('Identity Loss: ', identity_loss(x[0], x[0]))



# 定义预测方法签名
@tf.function(input_signature=[
    tf.TensorSpec(shape=[None, 128, 128, 3], dtype=tf.float32)
])
def predict_fn(input_data):
    return cycle_gan(input_data)

class callbacks(keras.callbacks.Callback):
    def __init__(self, fid_interval, generator, example_photo, example_monet):
        self.fid_interval = fid_interval
        self.generator = generator
        self.example_photo = example_photo
        self.example_monet = example_monet
        self.fid_values_monet = []
        self.fid_values_photo = []
        self.losses = []


    def on_epoch_end(self, epoch, logs={}):
        ### Every 5 epochs plot the generator
        randomint = np.random.randint(0, 15, 1)[0]

        # 加入损失
        self.losses.append(logs)
        # print(epoch, logs)
        
        if epoch % self.fid_interval == 0:
            fake_monet = self.generator.monet_generator_(self.example_photo, training=True)
            fake_photo = self.generator.photo_generator_(self.example_monet, training=True)
            fid_monet_value = self.calculate_fid(fake_monet, self.example_monet)
            fid_photo_value = self.calculate_fid(fake_photo, self.example_photo)
            print(f"fid_monet:{fid_monet_value},fid_photo:{fid_photo_value}")
            self.fid_values_monet.append(fid_monet_value)
            self.fid_values_photo.append(fid_photo_value)


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
            # save model
            # save model
            cycle_gan.save(f'{epoch}cycleGAN_model.h5')
#             tf.saved_model.save(cycle_gan, f'mymodel/{epoch}/', signatures={
#                 'serving_default': predict_fn
#             })
            
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

    def calculate_fid(self, real_images, fake_images):
        # 调整图像大小为299x299
        real_images = tf.image.resize(real_images, (299, 299))
        fake_images = tf.image.resize(fake_images, (299, 299))

        # 图像预处理
        real_images = tf.keras.applications.inception_v3.preprocess_input(real_images)
        fake_images = tf.keras.applications.inception_v3.preprocess_input(fake_images)

        # 加载 InceptionV3 模型
        model = tf.keras.applications.InceptionV3(include_top=False, pooling='avg', input_shape=(299, 299, 3))

        # 提取特征
        real_features = model(real_images)
        fake_features = model(fake_images)

        # 计算 FID
        mu_real = tf.reduce_mean(real_features, axis=0)
        mu_fake = tf.reduce_mean(fake_features, axis=0)

        # 计算样本协方差矩阵
        cov_real = tfp.stats.covariance(real_features, sample_axis=0)
        cov_fake = tfp.stats.covariance(fake_features, sample_axis=0)

        diff = mu_real - mu_fake
        # 使用数值稳定的方法计算FID
        cov_sqrtm = tf.linalg.sqrtm(tf.linalg.matmul(cov_real, cov_fake))
        trace = tf.linalg.trace(cov_real + cov_fake - 2 * cov_sqrtm)
        fid = tf.sqrt(tf.reduce_sum(diff ** 2) + tf.clip_by_value(trace, 0, 1e9))

        return fid
initial_learning_rate = 2e-3  # 初始学习率为2e-3
decay_steps = 800
decay_rate = 0.1  # 将衰减率从0.96改为0.1

with strategy.scope():
    # Learning rate schedules for each optimizer
    monet_gen_lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps, decay_rate, staircase=True)

    photo_gen_lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps, decay_rate, staircase=True)

    monet_disc_lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps, decay_rate, staircase=True)

    photo_disc_lr_schedule = tf.keras.optimizers.schedules.ExponentialDecay(
        initial_learning_rate, decay_steps, decay_rate, staircase=True)
    m_gen_opt = tf.keras.optimizers.Adam(learning_rate=monet_gen_lr_schedule, beta_1=0.5)
    p_gen_opt = tf.keras.optimizers.Adam(learning_rate=photo_gen_lr_schedule, beta_1=0.5)
    m_disc_opt = tf.keras.optimizers.Adam(learning_rate=monet_disc_lr_schedule, beta_1=0.5)
    p_disc_opt = tf.keras.optimizers.Adam(learning_rate=photo_disc_lr_schedule, beta_1=0.5)
    
# # 使用Adam优化器，学习率为2e-4，beta_1为0.5
# m_gen_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
# p_gen_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
# m_disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)
# p_disc_opt = tf.keras.optimizers.Adam(2e-4, beta_1=0.5)

# 创建CycleGAN模型并打印信息
cycle_gan = CycleGAN()
cycle_gan.compile(m_gen_opt, p_gen_opt, m_disc_opt, p_disc_opt)
cycle_gan.summary()

# 创建回调函数
fid_interval = 5  # 每隔5个epoch计算一次FID
callback = callbacks(fid_interval, cycle_gan, example_photo, example_monet)

# 训练模型
cycle_gan.fit(tf.data.Dataset.zip((monet_ds, photo_ds)), epochs=30, verbose=1, callbacks=callback)

# 对部分的图片进行莫奈风格转换后显示
fig, axes = plt.subplots(nrows=4, ncols=5, figsize=(15, 6))
fig.suptitle('Results', fontsize=16)

monet_results = cycle_gan.monet_generator_(example_photo)[0:10]
# 显示原始照片
for i in range(20):
    ax = axes[i // 5, i % 5]
    ax.imshow(example_photo[i])
    ax.axis('off')

# 显示莫奈风格的图像
for count, element in enumerate(monet_results):
    ax = axes[2 + count // 5, count % 5]
    ax.imshow(element)
    ax.axis('off')

axes[0, 2].set_title('Photos', size='large', loc='center')
axes[2, 2].set_title('Photos as Monet', size='large', loc='center')
plt.tight_layout()  # Adjust layout to make room for the main title
plt.savefig(f'final.png')
plt.show()



# 可视化损失函数
gen_monet_losses = [epoch['monet_gen_loss'] for epoch in callback.losses]
photo_gen_losses = [epoch['photo_gen_loss'] for epoch in callback.losses]
monet_disc_losses = [epoch['monet_disc_loss'] for epoch in callback.losses]
photo_disc_losses = [epoch['photo_disc_loss'] for epoch in callback.losses]

epochs = range(1, len(callback.losses) + 1)

plt.figure(figsize=(10, 5))
plt.plot(epochs, gen_monet_losses)
plt.plot(epochs, photo_gen_losses)
plt.plot(epochs, monet_disc_losses)
plt.plot(epochs, photo_disc_losses)
plt.scatter(epochs, gen_monet_losses, label='Monet Generator Loss')
plt.scatter(epochs, photo_gen_losses, label='Photo Generator Loss')
plt.scatter(epochs, monet_disc_losses, label='Monet Discriminator Loss')
plt.scatter(epochs, photo_disc_losses, label='Photo Discriminator Loss')
plt.title('CycleGAN Training Losses')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.savefig("loss.png")
plt.show()

# 可视化FID和IS指标
# 创建一个新的图像
plt.figure(figsize=(10, 6))
epochs = range(1, len(callback.losses) + 1, 5)
# 绘制莫奈风格图像的FID值
plt.plot(epochs, callback.fid_values_monet, label='Monet Style')
plt.scatter(epochs, callback.fid_values_monet, label='Monet Style')
# 绘制照片的FID值
plt.plot(epochs, callback.fid_values_photo, label='Photo Style')
plt.scatter(epochs, callback.fid_values_photo, label='Photo Style')

plt.title('CycleGAN FID Score')
plt.xlabel('Epoch')
plt.ylabel('Score')
plt.legend()
plt.savefig("FID_Score.png")
plt.show()

# fid_score_monet = [epoch['fid_score_monet'] for epoch in callback.fid_values_monet]
# fid_score_photo = [epoch['fid_score_photo'] for epoch in callback.fid_values_photo]
# epochs = range(1, len(callback.losses) + 1)
# plt.plot(epochs, fid_score_monet)
# plt.plot(epochs, fid_score_photo)
# plt.scatter(epochs, fid_score_monet, label='fid_score_monet')
# plt.scatter(epochs, fid_score_photo, label='fid_score_photo')
#
# plt.title('CycleGAN FID Score')
# plt.xlabel('Epoch')
# plt.ylabel('Score')
# plt.legend()
# plt.savefig("FID_Score.png")
# plt.show()

# # 保存模型在本地
# cycle_gan.save('model/cycle_gan.h5')
# cycle_gan.summary()

