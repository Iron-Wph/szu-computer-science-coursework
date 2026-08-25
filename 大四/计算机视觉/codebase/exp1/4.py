# import torch 
# import torch.nn as nn
# import matplotlib.pyplot as plt

# class DeepNetSigmoid(nn.Module):
#     def __init__(self):
#         super(DeepNetSigmoid, self).__init__()
#         self.layers = nn.Sequential(
#             nn.Linear(10, 10),
#             nn.Sigmoid(),
#             nn.Linear(10, 10),
#             nn.Sigmoid(),
#             nn.Linear(10, 10),
#             nn.Sigmoid(),
#             nn.Linear(10, 10),
#             nn.Sigmoid(),
#             nn.Linear(10, 1)
#         )
    
#     def forward(self, x):
#         return self.layers(x)

# class DeepNetReLU(nn.Module):
#     def __init__(self):
#         super(DeepNetReLU, self).__init__()
#         self.layers = nn.Sequential(
#             nn.Linear(10, 10),
#             nn.ReLU(),
#             nn.Linear(10, 10),
#             nn.ReLU(),
#             nn.Linear(10, 10),
#             nn.ReLU(),
#             nn.Linear(10, 10),
#             nn.ReLU(),
#             nn.Linear(10, 1),
#         )
    
#     def forward(self, x):
#         return self.layers(x)

# # 计算各层梯度
# def get_gradient_magniutdes(model, input):
#     model.zero_grad()
#     output = model(input)
#     output.backward()
    
#     gradients = []
#     # 收集各层权重的梯度范数
#     for i, layer in enumerate(model.layers):
#         if isinstance(layer, nn.Linear):
#             grad_norm = torch.norm(layer.weight.grad).item()
#             gradients.append(grad_norm)
    
#     return gradients

# # 随机输入
# input = torch.randn(1, 10, requires_grad=True)

# # 测试Sigmoid激活函数
# sigmoid_model = DeepNetSigmoid()
# sigmoid_grads = get_gradient_magniutdes(sigmoid_model, input)

# # 测试ReLU激活函数
# relu_model = DeepNetReLU()
# relu_grads = get_gradient_magniutdes(relu_model, input)

# # 绘制梯度比较图
# plt.figure(figsize=(12, 5))
# plt.subplot(1, 2, 1)
# plt.plot(range(1, len(sigmoid_grads)+1), sigmoid_grads, 'o-')
# plt.title('Gradient Magnitudes with Sigmoid Activation')
# plt.xlabel('Layer')
# plt.ylabel('Gradient Norm')
# plt.grid(True)

# plt.subplot(1, 2, 2)
# plt.plot(range(1, len(relu_grads)+1), relu_grads, 'o-', color='orange')
# plt.title('Gradient Magnitudes with ReLU Activation')
# plt.xlabel('Layer')
# plt.ylabel('Gradient Norm')
# plt.grid(True)

# plt.tight_layout()
# plt.savefig('gradient_vanishing_comparison.png')
# plt.show()

# print(f"Sigmoid激活的梯度大小为：{sigmoid_grads}")
# print(f"ReLU激活的梯度大小为：{relu_grads}")


import torch 
import torch.nn as nn
import matplotlib.pyplot as plt

class DeepNetSigmoid(nn.Module):
    def __init__(self, layer_nums=5):
        super(DeepNetSigmoid, self).__init__()
        self.layers = nn.ModuleList()
        for _ in range(layer_nums - 1):
            self.layers.append(nn.Linear(10, 10))
            self.layers.append(nn.Sigmoid())
        self.layers.append(nn.Linear(10, 1))
   
    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    
class DeepNetReLU(nn.Module):
    def __init__(self, layer_nums=5):
        super(DeepNetReLU, self).__init__()
        
        self.layers = nn.ModuleList()
        for _ in range(layer_nums - 1):
            self.layers.append(nn.Linear(10, 10))
            self.layers.append(nn.ReLU())
        self.layers.append(nn.Linear(10, 1))


    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x

# 计算各层梯度
def get_gradient_magniutdes(model, input):
    model.zero_grad()
    output = model(input)
    output.backward()
    
    gradients = []
    # 收集各层权重的梯度范数
    for i, layer in enumerate(model.layers):
        if isinstance(layer, nn.Linear):
            grad_norm = torch.norm(layer.weight.grad).item()
            gradients.append(grad_norm)
    
    return gradients

# 随机输入
input = torch.randn(1, 10, requires_grad=True)

# 测试Sigmoid激活函数
sigmoid_model_3 = DeepNetSigmoid(layer_nums=3)          # 测试3层
sigmoid_grads_3 = get_gradient_magniutdes(sigmoid_model_3, input)
sigmoid_model_5 = DeepNetSigmoid(layer_nums=5)          # 测试5层
sigmoid_grads_5 = get_gradient_magniutdes(sigmoid_model_5, input)
sigmoid_model_7 = DeepNetSigmoid(layer_nums=7)          # 测试7层
sigmoid_grads_7 = get_gradient_magniutdes(sigmoid_model_7, input)

# 测试ReLU激活函数
relu_model_3 = DeepNetReLU(layer_nums=3)                # 测试3层
relu_grads_3 = get_gradient_magniutdes(relu_model_3, input)
relu_model_5 = DeepNetReLU(layer_nums=5)                # 测试5层
relu_grads_5 = get_gradient_magniutdes(relu_model_5, input)
relu_model_7 = DeepNetReLU(layer_nums=7)                # 测试7层
relu_grads_7 = get_gradient_magniutdes(relu_model_7, input)

# 绘制梯度比较图
plt.figure(figsize=(5, 15))

plt.subplot(1, 3, 1)
plt.plot(range(1, len(sigmoid_grads_3)+1), sigmoid_grads_3, 'o-', color = 'blue', label='Sigmoid')
plt.plot(range(1, len(relu_grads_3)+1), relu_grads_3, 'o-', color='orange', label='ReLU')
plt.title('Gradient Magnitudes with 3 layers Network')
plt.xlabel('Layer')
plt.ylabel('Gradient Norm')
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(range(1, len(sigmoid_grads_5)+1), sigmoid_grads_5, 'o-', color = 'blue', label='Sigmoid')
plt.plot(range(1, len(relu_grads_5)+1), relu_grads_5, 'o-', color='orange', label='ReLU')
plt.title('Gradient Magnitudes with 5 layers Network')
plt.xlabel('Layer')
plt.ylabel('Gradient Norm')
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(range(1, len(sigmoid_grads_7)+1), sigmoid_grads_7, 'o-', color = 'blue', label='Sigmoid')
plt.plot(range(1, len(relu_grads_7)+1), relu_grads_7, 'o-', color='orange', label='ReLU')
plt.title('Gradient Magnitudes with 7 layers Network')
plt.xlabel('Layer')
plt.ylabel('Gradient Norm')
plt.grid(True)

plt.legend()
plt.tight_layout()
plt.savefig('gradient_vanishing_comparison2.png')
plt.show()

print(f"3层layers的Sigmoid激活的梯度大小为：{sigmoid_grads_3}")
print(f"5层layers的Sigmoid激活的梯度大小为：{sigmoid_grads_5}")
print(f"7层layers的Sigmoid激活的梯度大小为：{sigmoid_grads_7}")

print(f"3层layers的ReLU激活的梯度大小为：{relu_grads_3}")
print(f"5层layers的ReLU激活的梯度大小为：{relu_grads_5}")
print(f"7层layers的ReLU激活的梯度大小为：{relu_grads_7}")

    