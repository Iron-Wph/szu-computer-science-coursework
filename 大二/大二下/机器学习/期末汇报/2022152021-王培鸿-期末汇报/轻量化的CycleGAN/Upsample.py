import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers
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