import numpy as np
from conv import Conv3x3
from maxpool import MaxPool2
from softmax import Softmax
from scipy.io import loadmat
import matplotlib.pyplot as plt
from displayData import displayData
# =========== Part 1: Loading and Visualizing Data =============
#  We start the exercise by first loading and visualizing the dataset.
#  You will be working with a dataset that contains handwritten digits.
# Load Training And Testing Data
print('Loading and Visualizing Data ...')
mnist = loadmat('ex3_data.mat')#加载mnist数据集
X_train = mnist['train_images']#读取训练集图片
train_labels = mnist['train_labels'].T.reshape(-1,1).astype(int)#读取训练集标签
X_test = mnist['test_images']#读取测试集图片
test_labels = mnist['test_labels'].T.reshape(-1,1).astype(int)#读取测试集标签
m = train_labels .shape[0]
# Randomly select 100 data points to display
rand_indices = np.random.choice(np.arange(m), 100)
print(X_train.shape)
sel = X_train[:, rand_indices]

displayData(sel)
plt.show()

#训练集太大训练时间会很长
train_len=2000#训练集长度
test_len=500#测试集长度
X_train=X_train[:,:train_len]
train_labels=train_labels[:,:train_len]
X_test=X_test[:,:test_len]
test_labels=test_labels[:,:test_len]
train_images=np.zeros(shape=(train_len,28,28))
test_images=np.zeros(shape=(test_len,28,28))
for i in range(train_len):
    train_images[i,:,:]=X_train[:,i].reshape(28,28)#将数据转化为28*28的图片784->28x28x1

for i in range(test_len):
    test_images[i,:,:]=X_test[:,i].reshape(28,28)#将数据转化为28*28的图片784->28x28x1
print(test_images.shape)
print(train_images.shape)
# =========== Part 2: Instantiation Class =============
conv = Conv3x3(8)#实例化Conv3x3                 # 28x28x1 -> 26x26x8
pool = MaxPool2()#实例化 MaxPool2             # 26x26x8 -> 13x13x8
softmax = Softmax(13*13*8, 10)#实例化Softmax # 13x13x8 -> 10


# =========== Part 3: CNN forward=============
#  Completes a forward pass of the CNN and calculates the accuracy and
#   cross-entropy loss.
def forward(image, label):
  '''
  - image is a 2d numpy array
  - label is a digit
  '''
  # We transform the image from [0, 255] to [-0.5, 0.5] to make it easier
  # to work with. This is standard practice.
  out = conv.forward((image / 255) - 0.5)
  out = pool.forward(out)
  out = softmax.forward(out)
  # Calculate cross-entropy loss and accuracy. np.log() is the natural log.
  loss = -np.log(out[label])
  # Calculate accuracy
  # 根据最大值的索引返回acc
  acc = 1 if np.argmax(out) == label else 0

  # 返回预测结果、交叉熵损失函数、acc
  return out, loss, acc


# =========== Part 4: Training CNN =============
# Completes a full training step on the given image and label.
#   Returns the cross-entropy loss and accuracy.
def train(im, label, lr=.005):
  '''
  - image is a 2d numpy array
  - label is a digit
  - lr is the learning rate
  '''
  # Forward
  out, loss, acc = forward(im, label)
  # Calculate initial gradient
  gradient = np.zeros(10)
  #Cross entropy loss，偏导后的交叉熵求解
  gradient[label] = -1 / out[label]
  # Backprop
  gradient = softmax.backprop(gradient, lr)
  gradient = pool.backprop(gradient)
  gradient = conv.backprop(gradient, lr)

  return loss, acc

print('MNIST CNN initialized!')
# Train the CNN for 3 epochs
for epoch in range(5):
  print('--- Epoch %d ---' % (epoch + 1))
  # Shuffle the training data
  permutation = np.random.permutation(len(train_images))
  train_images = train_images[permutation]
  train_labels = train_labels[permutation]
  # Train!
  loss = 0
  num_correct = 0
  for i, (im, label) in enumerate(zip(train_images, train_labels)):
    if i % 100 == 99:
      print(
        '[Step %d] Past 100 steps: Average Loss %.3f | Accuracy: %d%%' %
        (i + 1, loss / 100, num_correct)
      )
      loss = 0
      num_correct = 0

    l, acc = train(im, label)
    loss += l
    num_correct += acc

# =========== Part 5: Testing CNN =============
# Calculate the loss and accuracy of the test set
print('\n--- Testing the CNN ---')
loss = 0
num_correct = 0
for im, label in zip(test_images, test_labels):
  _, l, acc = forward(im, label)
  loss += l
  num_correct += acc

num_tests = len(test_images)
print('Test Loss:', loss / num_tests)
print('Test Accuracy:', num_correct / num_tests)
print('(this Test Loss should be about[0.37039879])')
print('(this Test Accuracy should be about 0.888)')