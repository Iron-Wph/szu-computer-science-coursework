#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
% Instructions: You should first compute the covariance matrix. Then, you
%               should use the "svd" function to compute the eigenvectors
%               and eigenvalues of the covariance matrix.
%
% Note: When computing the covariance matrix, remember to divide by m (the
%       number of examples).
"""

import numpy as np


def pca(X):
    m, n = X.shape
    U = np.zeros((n, n))
    S = np.zeros(n)
    # pass
    # ====================== YOUR CODE HERE ======================
    # You should change this
    # 协防差矩阵
    Sigma = (1/m) * (X.T @ X)
    # 特征向量矩阵和特征值向量
    U, S, _ = np.linalg.svd(Sigma)
    # ======================END ======================
    return U, S
