import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
from Downsample import Downsample
from Upsample import Upsample


class Discriminator(keras.Model):
    def __init__(self, name='Discriminator', dense=32, activation='leaky_relu', **kwargs):
        super(Discriminator, self).__init__(name=name, **kwargs)
        self.initializer = tf.random_normal_initializer(0., 0.02)

        # 修改 Downsample 层的参数
        self.downsample1 = Downsample(32, name='Downsample_64')  ## (bs, 64, 64, 64)
        self.downsample2 = Downsample(128, name='Downsample_32')  ## (bs, 32, 32, 128)
        self.downsample3 = Downsample(256, name='Downsample_16')  ## (bs, 16, 16, 256)
        self.downsample4 = Downsample(256, name='Downsample_8')  ## (bs, 256, 256, 128)

        self.zeropad = layers.ZeroPadding2D(name='Zero_Padding')
        self.downsample5 = Downsample(256, strides=(1, 1), kernel_size=(2, 2),
                                      name='Downsample_stride_1')  ## (bs, 32, 32, 256)

        self.flatten = layers.Flatten(name='Flatten_layer')

        # 调整全连接层 dense 的神经元数量
        self.dense = layers.Dense(dense, name=f'Hiden_layer_{dense}')
        self.dropout = layers.Dropout(0.2, name='Dropout')
        self.activation = layers.Activation(activation, name=f'{activation}')
        self.last = layers.Dense(1, activation='sigmoid')

    def call(self, inputs, training=False):
        x = self.downsample1(inputs, training=training)
        print(f"{tf.shape(x)}")
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