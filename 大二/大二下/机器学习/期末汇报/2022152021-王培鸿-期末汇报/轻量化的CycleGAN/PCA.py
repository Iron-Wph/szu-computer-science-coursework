import tensorflow as tf
from sklearn.decomposition import PCA
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