import tensorflow.keras as keras
import tensorflow as tf
# 生成器的损失函数
# 最小化生成器输出与真实样本之间的差异，使得判别器认为生成器生成的样本是真实的
def generator_loss(disc_output):
    ### BinaryCrossentropy二分类交叉熵函数用于二分类问题
    ### 二分类交叉熵用于(1 和 disc_output)之间
    return keras.losses.BinaryCrossentropy(from_logits=False)(tf.ones_like(disc_output), disc_output)

# 判别器的损失函数
# 最小化这个总损失,即最大化它对真实样本的预测概率,同时最小化它对生成样本的预测概率
def discriminator_loss(real_output, fake_output):
    ### 二分交叉熵函数用于分类为真样本的情况
    real_loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)(tf.ones_like(real_output), real_output)
    ### 二分交叉熵函数用于分类为假样本的情况
    fake_loss = tf.keras.losses.BinaryCrossentropy(from_logits=False)(tf.zeros_like(fake_output), fake_output)
    return real_loss + fake_loss


# 循环一致性损失：最小化原始图像和循环生成图像之间的差异
def cycle_loss(real_image, cycled_image, lambda_cycle=10):
    # 求取原始图像与循环图像的平均绝对误差 并 乘于权重lambda_cycle
    return lambda_cycle * tf.reduce_mean(tf.abs(real_image - cycled_image))


# 身份损失：最小化原始图像和生成器处理后仍然在同一域的图像之间的差异
def identity_loss(real_image, same_image, lambda_identity=5):
    # 真实图像和相同域图像的平均绝对差 并 乘于 权重lambda_identity
    return lambda_identity * tf.reduce_mean(tf.abs(real_image - same_image))

