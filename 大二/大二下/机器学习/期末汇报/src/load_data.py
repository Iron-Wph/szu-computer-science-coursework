import tensorflow as tf
from tensorflow.io.gfile import glob

# 设置图像的大小
IMAGE_SIZE = [128, 128]
AUTOTUNE = tf.data.experimental.AUTOTUNE

# 编码图片为（128，128，3）
def decode_image(image):
    image = tf.image.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize(image, IMAGE_SIZE)
    image = tf.reshape(image, [*IMAGE_SIZE, 3])
    return image

# 读取TFRecord文件
def read_tfrecord(example):
    tfrecord_format = {
        "image_name": tf.io.FixedLenFeature([], tf.string),
        "image": tf.io.FixedLenFeature([], tf.string),
        "target": tf.io.FixedLenFeature([], tf.string)
    }
    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example['image'])
    return image

# 加载TFRecord文件中的数据集
def load_dataset(filenames, labeled=True, ordered=False, repeat=False):
    dataset = tf.data.TFRecordDataset(filenames)
    dataset = dataset.map(read_tfrecord, num_parallel_calls=AUTOTUNE)
    if repeat:
        dataset = dataset.repeat(count = 20)
    # 随机打乱样本
    dataset = dataset.shuffle(1000)
    # prefetch训练时高效加载数据
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return dataset