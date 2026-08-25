#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
% Instructions: Go over every example, find its closest centroid, and store
%               the index inside idx at the appropriate location.
%               Concretely, idx(i) should contain the index of the centroid
%               closest to example i. Hence, it should be a value in the
%               range 1..K
%
% Note: You can use a for-loop over the examples to compute this.
"""
import sys
import numpy as np


def findClosestCentroids(X, centroids):
    # Set K
    K = centroids.shape[0]
    # You need to return the following variables correctly.
    idx = np.zeros((X.shape[0], 1), dtype=int)

    for i in range(X.shape[0]):
        min_dist = sys.maxsize#初始化最小距离
        for j in range(K):
            # ====================== YOUR CODE HERE ======================
            # You should change this
            #You should update min_dist and find the right idx[i]
            distance = ((X[i][0]-centroids[j][0])**2) + ((X[i][1]-centroids[j][1])**2)
            if distance < min_dist:
                min_dist = distance
                idx[i] = j
            # ======================END ======================
    return idx
