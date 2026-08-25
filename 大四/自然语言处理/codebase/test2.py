import numpy as np

# 给定句子
sentence = "The quick brown fox jumps"
# 下一个预测字符（用于计算损失）
next_chars = " over the lazy dog."

# 提取所有唯一字符并排序
chars = sorted(list(set(sentence + next_chars)))
char_to_idx = {char: i for i, char in enumerate(chars)}
idx_to_char = {i: char for i, char in enumerate(chars)}
vocab_size = len(chars)

print(f"词汇表大小: {vocab_size}")
print(f"字符到索引映射: {char_to_idx}")
print(f"索引到字符映射: {idx_to_char}")

# 将句子转换为索引序列
sentence_indices = [char_to_idx[char] for char in sentence]
next_char_indices = [char_to_idx[char] for char in next_chars]
max_len = min(len(sentence_indices), len(next_char_indices))
sentence_indices = sentence_indices[:max_len]
next_char_indices = next_char_indices[:max_len]

# 转换为独热编码
def one_hot_encode(indices, vocab_size):
    """将索引序列转换为独热编码矩阵"""
    encoding = np.zeros((len(indices), vocab_size))
    for i, idx in enumerate(indices):
        encoding[i, idx] = 1
    return encoding

# 输入的独热编码
X = one_hot_encode(sentence_indices, vocab_size)
# 目标输出的独热编码
Y = one_hot_encode(next_char_indices, vocab_size)


# 初始化权重和参数
hidden_size = 10  # 隐藏层大小
input_size = vocab_size
output_size = vocab_size

# 随机初始化权重
np.random.seed(42)  # 设置随机种子，确保结果可重现
W1 = np.random.randn(hidden_size, input_size) * 0.01  # 输入到隐藏层权重
W2 = np.random.randn(hidden_size, hidden_size) * 0.01  # 隐藏层到隐藏层权重
W3 = np.random.randn(output_size, hidden_size) * 0.01  # 隐藏层到输出层权重

b1 = np.zeros((hidden_size, 1))  # 隐藏层偏置
b3 = np.zeros((output_size, 1))  # 输出层偏置

print("权重和偏置已初始化")

# 前向传播
def forward_propagation(X, pre_hidden, w1, w2, w3, b1, b3):
    # 计算当前隐藏状态
    hidden = np.tanh(np.dot(w1, X) + np.dot(w2, pre_hidden) + b1)
    output = np.dot(w3, hidden) + b3
    # 使用softmax获得概率分布
    output = np.exp(output) / np.sum(np.exp(output))
    return hidden, output 

# 计算交叉熵损失函数
def compute_loss(outputs, targets):
    loss = 0
    for output, target in zip(outputs, targets):
        target = target.reshape(-1, 1)      # 确保为列向量
        loss -= np.sum(target * np.log(output + 1e-8))
    return loss / len(outputs)

# 反向传播和梯度更新
def backward_propagation(X, Y, hidden_states, outputs, w1, w2, w3, b1, b3, learning_rate=0.01):
    # 初始化梯度
    dW1 = np.zeros_like(w1)
    dW2 = np.zeros_like(w2)
    dW3 = np.zeros_like(w3)
    db1 = np.zeros_like(b1)
    db3 = np.zeros_like(b3)
    # 最后一个时间步的隐藏状态梯度初始化为0
    dh_next = np.zeros_like(hidden_states[0])
    
    # 反向遍历每个时间步
    for t in reversed(range(len(X))):
        # 当前时间步的输出和目标
        output = outputs[t]
        target = Y[t].reshape(-1, 1)
        # 输出层梯度
        dy = output - target
        dW3 += np.dot(dy, hidden_states[t].T)
        db3 += dy
        # 隐藏层梯度
        dh = np.dot(W3.T, dy) + dh_next
        dh_raw = (1 - hidden_states[t] ** 2) * dh  # tanh导数是1-tanh^2
        dW1 += np.dot(dh_raw, X[t].reshape(1, -1))
        db1 += dh_raw
        # 如果不是第一个时间步，计算隐藏层到隐藏层的梯度
        if t > 0:
            dW2 += np.dot(dh_raw, hidden_states[t-1].T)
        dh_next = np.dot(W2.T, dh_raw)
    # 梯度归一化
    num_timesteps = len(X)
    dW1 /= num_timesteps
    dW2 /= num_timesteps
    dW3 /= num_timesteps
    db1 /= num_timesteps
    db3 /= num_timesteps
    # 更新权重和偏置
    w1 -= learning_rate * dW1
    w2 -= learning_rate * dW2
    w3 -= learning_rate * dW3
    b1 -= learning_rate * db1
    b3 -= learning_rate * db3

    return w1, w2, w3, b1, b3

# 模型训练
def train(X, Y, W1, W2, W3, b1, b3, epochs=1000, learning_rate=0.01):
    losses = []
    for epoch in range(epochs):
        # 初始化隐藏状态
        hidden = np.zeros((hidden_size, 1))
        hidden_states = []
        outputs = []
        
        # 前向传播
        for t in range(len(X)):
            x = X[t].reshape(-1, 1)  # 将输入转换为列向量
            hidden, output = forward_propagation(x, hidden, W1, W2, W3, b1, b3)
            hidden_states.append(hidden)
            outputs.append(output)
        
        # 计算损失
        loss = compute_loss(outputs, Y)
        losses.append(loss)
        
        # 反向传播
        W1, W2, W3, b1, b3 = backward_propagation(
            X, Y, hidden_states, outputs, W1, W2, W3, b1, b3)
        

        # 每100个epoch打印一次损失
        if (epoch + 1) % 100 == 0:
            print(f"Epoch {epoch+1}/{epochs}, 损失: {loss:.4f}")
    
    return W1, W2, W3, b1, b3, losses

def generate_text(seed_text, length, W1, W2, W3, b1, b3, char_to_idx,
                  idx_to_char, vocab_size, hidden_size):
    """使用训练好的模型生成文本"""
    # 初始化隐藏状态
    hidden = np.zeros((hidden_size, 1))
    generated_text = seed_text
    
    # 将种子文本输入模型，更新隐藏状态
    for char in seed_text:
        x = np.zeros((vocab_size, 1))
        x[char_to_idx[char]] = 1
        hidden, _ = forward_propagation(x, hidden, W1, W2, W3, b1, b3)
    
    # 生成新文本
    current_char = seed_text[-1]
    for _ in range(length):
        # 准备当前字符的输入
        x = np.zeros((vocab_size, 1))
        x[char_to_idx[current_char]] = 1
        
        # 前向传播获取下一个字符的概率分布
        hidden, output = forward_propagation(x, hidden, W1, W2, W3, b1, b3)
        
        # 根据概率分布采样下一个字符
        idx = np.random.choice(range(vocab_size), p=output.ravel())
        current_char = idx_to_char[idx]
        generated_text += current_char
    
    return generated_text

# 执行训练
print("\n开始训练...")
W1_trained, W2_trained, W3_trained, b1_trained, b3_trained, losses = train(
    X, Y, W1, W2, W3, b1, b3, epochs=1000, learning_rate=0.1)

# 生成文本
print("\n生成文本:")
generated = generate_text("The quick brown fox jumps", len(next_chars), 
                          W1_trained, W2_trained, W3_trained, b1_trained, b3_trained,
                          char_to_idx, idx_to_char, vocab_size, hidden_size)
print(f"原始句子: {sentence}{next_chars}")
print(f"生成句子: {generated}")