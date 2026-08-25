#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
% Instructions: Compute the projection of the data using only the top K
%               eigenvectors in U (first K columns).
%               For the i-th example X(i,:), the projection on to the k-th
%               eigenvector is given as follows:
%                    x = X(i, :)';
%                    projection_k = x' * U(:, k);
"""
import numpy as np

# 将n维投影到k维
def projectData(X, U, K):
    # 找K个最能代表原数据的向量，投影成(m, k)。假设X为（m, n）
    Z = np.zeros((X.shape[0], K))
    # pass
    # ====================== YOUR CODE HERE ======================
    # You should change this
    U_reduce = U[:, 0: K]
    # 投影
    Z = X @ U_reduce
    # ======================END ======================
    return Z
