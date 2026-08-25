import numpy as np

# 定义词汇表并进行独热编码
words = ["king", "queen", "man", "woman"]
word_to_index = {word: i for i, word in enumerate(words)}
vocab_size = len(words)

# 生成独热编码矩阵
def one_hot_encode(word):
    vector = np.zeros(vocab_size)
    vector[word_to_index[word]] = 1
    return vector

# 为每个词创建独热向量
king_onehot = one_hot_encode("king")
queen_onehot = one_hot_encode("queen")
man_onehot = one_hot_encode("man")
woman_onehot = one_hot_encode("woman")

print("独热编码:")
print(f"king: {king_onehot}")
print(f"queen: {queen_onehot}")
print(f"man: {man_onehot}")
print(f"woman: {woman_onehot}")


# 初始化参数矩阵 - 嵌入矩阵
embedding_dim = 2  # 嵌入维度
np.random.seed(42)  
embedding_matrix = np.random.randn(vocab_size, embedding_dim) * 0.01

print("\n初始嵌入矩阵:")
print(embedding_matrix)

# 通过独热向量与嵌入矩阵相乘得到词嵌入向量
def get_embedding(onehot_vector):
    return np.dot(onehot_vector, embedding_matrix)

# 获取各个词的嵌入向量
king_embedding = get_embedding(king_onehot)
queen_embedding = get_embedding(queen_onehot)
man_embedding = get_embedding(man_onehot)
woman_embedding = get_embedding(woman_onehot)

print("\n词嵌入向量:")
print(f"king: {king_embedding}")
print(f"queen: {queen_embedding}")
print(f"man: {man_embedding}")
print(f"woman: {woman_embedding}")

# 4. 定义损失函数 - 基于"king - man + woman ≈ queen"的优化目标
def loss_function(king, man, woman, queen):
    # 计算king - man + woman的结果
    result = king - man + woman
    # 计算与queen向量的均方误差
    mse_loss = np.mean((result - queen) **2)
    return mse_loss

# 计算当前损失
current_loss = loss_function(king_embedding, man_embedding, woman_embedding, queen_embedding)
print(f"\n当前损失值: {current_loss}")

# 简单的优化过程演示
learning_rate = 0.1
epochs = 1000

# 进行优化
for i in range(epochs):
    # 重新计算嵌入（实际中应该通过反向传播更新嵌入矩阵）
    king_embedding = get_embedding(king_onehot)
    queen_embedding = get_embedding(queen_onehot)
    man_embedding = get_embedding(man_onehot)
    woman_embedding = get_embedding(woman_onehot)
    
    # 计算损失
    current_loss = loss_function(king_embedding, man_embedding, woman_embedding, queen_embedding)
    
    # 计算梯度（简化版）
    result = king_embedding - man_embedding + woman_embedding
    gradient = 2 * (result - queen_embedding)
    
    # 更新嵌入矩阵（简化的梯度下降）
    embedding_matrix[word_to_index["queen"]] -= learning_rate * (-gradient)
    embedding_matrix[word_to_index["king"]] -= learning_rate * gradient
    embedding_matrix[word_to_index["man"]] -= learning_rate * (-gradient)
    embedding_matrix[word_to_index["woman"]] -= learning_rate * gradient
    
    # 每100轮打印一次损失
    if i % 100 == 0:
        print(f"迭代 {i}, 损失值: {current_loss}")

# 优化后的嵌入向量
print("\n优化后的词嵌入向量:")
print(f"king: {get_embedding(king_onehot)}")
print(f"queen: {get_embedding(queen_onehot)}")
print(f"man: {get_embedding(man_onehot)}")
print(f"woman: {get_embedding(woman_onehot)}")

# 验证优化结果
final_result = get_embedding(king_onehot) - get_embedding(man_onehot) + get_embedding(woman_onehot)
print(f"\n优化后 king - man + woman = {final_result}")
print(f"优化后 queen = {get_embedding(queen_onehot)}")
