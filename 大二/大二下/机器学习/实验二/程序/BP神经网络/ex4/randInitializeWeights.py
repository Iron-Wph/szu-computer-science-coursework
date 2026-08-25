#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np


def randInitializeWeights(L_in, L_out):
    W = np.zeros((L_out, 1 + L_in))
    # ====================== YOUR CODE HERE ======================
    # You should change this
    e = 0.12
    # 随机种子
    rd = np.random.RandomState(888)
    # 在[-e,e]之间生成随机值
    W = rd.random((L_out, 1 + L_in)) * 2 * e - e
    # ========== END ==========
    return W
