import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
# 生成器继承keras.Model类
class Generator(keras.Model):
    def __init__(self, name='Generator', **kwargs):
        super(Generator, self).__init__(name=name, **kwargs)

        ### Downsampling layers
        self.downsample1 = Downsample(16, name='Donwsample_64')  ## (bs,64,64,16)
        self.downsample2 = Downsample(32, name='Donwsample_32')  ## (bs,32,32,32)
        self.downsample3 = Downsample(64, name='Donwsample_16')  ## (bs,16,16,64)
        self.downsample4 = Downsample(128, name='Donwsample_8')  ## (bs,8,8,128)
        self.downsample5 = Downsample(256, name='Donwsample_4')  ## (bs,4,4,256)
        self.downsample6 = Downsample(256, name='Donwsample_2')  ## (bs,2,2,256)
        self.downsample7 = Downsample(256, name='Donwsample_1')  ## (bs,1,1,256)

        ## Upsampling layers
        self.upsample1 = Upsample(256, dropout=True, name='Upsample_2')  ## (bs,2,2,256)
        self.upsample2 = Upsample(256, dropout=True, name='Upsample_4')  ## (bs,4,4,256)
        self.upsample3 = Upsample(128, name='Upsample_8')  ## (bs,8,8,128)
        self.upsample4 = Upsample(64, name='Upsample_16')  ## (bs,16,16,64)
        self.upsample5 = Upsample(32, name='Upsample_32')  ## (bs,32,32,32)
        self.upsample6 = Upsample(16, name='Upsample_64')  ## (bs,64,64,16)
        self.final_upsample = Upsample(3, activation='sigmoid', name='Output_layer')  # (bs,128,128,3)

    def call(self, inputs, training=False):
        # 下采样部分与之前一致
        d1 = self.downsample1(inputs, training=training)
        d2 = self.downsample2(d1, training=training)
        d3 = self.downsample3(d2, training=training)
        d4 = self.downsample4(d3, training=training)
        d5 = self.downsample5(d4, training=training)
        d6 = self.downsample6(d5, training=training)
        d7 = self.downsample7(d6, training=training)
        # 上采样部分做相应调整
        u1 = self.upsample1(d7, training=training)
        # print(f"u1 shape: {tf.shape(u1)}")
        # print(f"d6 shape: {tf.shape(d6)}")

        u1_concat = tf.concat([u1, d6], axis=-1)

        u2 = self.upsample2(u1_concat, training=training)
        u2_concat = tf.concat([u2, d5], axis=-1)
        u3 = self.upsample3(u2_concat, training=training)
        u3_concat = tf.concat([u3, d4], axis=-1)
        u4 = self.upsample4(u3_concat, training=training)
        u4_concat = tf.concat([u4, d3], axis=-1)
        u5 = self.upsample5(u4_concat, training=training)
        u5_concat = tf.concat([u5, d2], axis=-1)
        u6 = self.upsample6(u5_concat, training=training)
        u6_concat = tf.concat([u6, d1], axis=-1)
        x = self.final_upsample(u6_concat, training=training)
        return x