import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
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