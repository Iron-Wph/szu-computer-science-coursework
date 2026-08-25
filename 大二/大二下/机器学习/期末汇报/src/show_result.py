import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from CycleGNN import CycleGAN

with tf.keras.utils.custom_object_scope({'CycleGAN': CycleGAN}):
    # Load the CycleGAN model
    model = tf.keras.models.load_model('./model/cycle_gan.h5')

# Function to preprocess the input image
def preprocess_image(image_path):
    # Load the image using PIL
    image = Image.open(image_path)
    # Resize the image to match the model input size
    image = image.resize((256, 256))
    # Convert the image to numpy array and normalize it to the range [-1, 1]
    image = np.array(image, dtype=np.float32) / 127.5 - 1.0
    # Expand the dimensions to match the model input shape (add batch dimension)
    image = np.expand_dims(image, axis=0)
    return image

# Function to postprocess the output image
def postprocess_image(output_image):
    # Rescale the output image from [-1, 1] to [0, 255]
    output_image = (output_image + 1.0) * 127.5
    # Convert the image to uint8 data type
    output_image = np.uint8(output_image)
    return output_image

# Function to perform image prediction
def predict_image(input_image):
    # Perform prediction using the model
    output_image = model.predict(input_image)
    return output_image

# Path to the input image
input_image_path = 'input_image.jpg'

# Preprocess the input image
input_image = preprocess_image(input_image_path)

# Perform prediction
output_image = predict_image(input_image)

# Postprocess the output image
output_image = postprocess_image(output_image)

# Display the input and output images using matplotlib
plt.figure(figsize=(10, 5))

# Display input image
plt.subplot(1, 2, 1)
plt.imshow(Image.open(input_image_path))
plt.title('Input Image')
plt.axis('off')

# Display output image
plt.subplot(1, 2, 2)
plt.imshow(output_image[0])
plt.title('Output Image')
plt.axis('off')

plt.show()
