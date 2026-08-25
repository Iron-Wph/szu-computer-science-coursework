import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from Downsample import Downsample
from Upsample import Upsample
# 生成器继承keras.Model类
class Generator(keras.Model):
    def __init__(self, name='Generator', **kwargs):
        super(Generator, self).__init__(name=name, **kwargs)

        ### Downsampling layers
        self.downsample3 = Downsample(64, name='Donwsample_1', strides=(1, 1),
                                      kernel_size=(5, 5))  ## (bs,128,128,64)
        self.downsample4 = Downsample(128, name='Donwsample_2')  ## (bs,64,64,128)
        self.downsample5 = Downsample(128, name='Donwsample_3')  ## (bs,32,32,128)
        self.downsample6 = Downsample(256, name='Donwsample_4')  ## (bs,16,16,256)
        self.downsample7 = Downsample(256, name='Donwsample_5')  ## (bs,8,8,256)
        self.downsample8 = Downsample(256, name='Donwsample_6')  ## (bs,4,4,256)
        self.downsample9 = Downsample(512, name='Donwsample_7')  ## (bs,2,2,512)
        self.downsample10 = Downsample(512, name='Donwsample_8')  ## (bs,1,1,512)

        ## Upsampling layers
        self.upsample1 = Upsample(512, dropout=True, name='Upsample_2')  ## (bs,2,2,512)
        self.upsample2 = Upsample(256, dropout=True, name='Upsample_4')  ## (bs,4,4,256)
        self.upsample3 = Upsample(256, name='Upsample_8')  ## (bs,8,8,256)
        self.upsample4 = Upsample(256, name='Upsample_16')  ## (bs,16,16,256)
        self.upsample5 = Upsample(128, name='Upsample_32')  ## (bs,32,32,128)
        self.upsample6 = Upsample(128, name='Upsample_64')  ## (bs,64,64,128)
        self.upsample7 = Upsample(64, name='Upsample_64')  ## (bs,128,128,64)
        self.final_upsample = Upsample(3, activation='sigmoid', name='Output_layer')  # (bs,128,128,3)

    def call(self, inputs, training=False):
        # # 下采样部分与之前一致
        d1 = self.downsample3(inputs, training=training)
        # print(f"d1 shape: {tf.shape(d1)}")
        d2 = self.downsample4(d1, training=training)
        # print(f"d2 shape: {tf.shape(d2)}")
        d3 = self.downsample5(d2, training=training)
        # print(f"d3 shape: {tf.shape(d3)}")
        d4 = self.downsample6(d3, training=training)
        # print(f"d4 shape: {tf.shape(d4)}")
        d5 = self.downsample7(d4, training=training)
        # print(f"d5 shape: {tf.shape(d5)}")
        d6 = self.downsample8(d5, training=training)
        # print(f"d6 shape: {tf.shape(d6)}")
        d7 = self.downsample9(d6, training=training)
        # print(f"d7 shape: {tf.shape(d7)}")
        d8 = self.downsample10(d7, training=training)
        # print(f"d5 shape: {tf.shape(d8)}")
        # # 上采样部分做相应调整
        u1 = self.upsample1(d8, training=training)
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