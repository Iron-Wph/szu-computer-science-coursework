#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
% Instructions: Go over every centroid and compute mean of all points that
%               belong to it. Concretely, the row vector centroids(i, :)
%               should contain the mean of the data points assigned to
%               centroid i.
"""

import numpy as np


def computeCentroids(X, idx, K):
    m, n = X.shape
    centroids = np.zeros((K, n))            # 维度为(k,2)
    # pass
    # ====================== YOUR CODE HERE ======================
    # You should change this
    # 提示ravel()函数将数据拉伸为一维数组
    length = np.zeros((K, 1), int)           # 存放每一类的个数，维度为(K, 1)
    i = 0
    while i < m:
        centroids[idx[i]] += X[i]
        length[idx[i]] += 1
        i += 1
    # 取均值
    centroids /= length
    # ======================END ======================
    return centroids
