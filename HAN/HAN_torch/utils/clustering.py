# -*- coding: utf-8 -*-
# @Time : 2023/3/21 20:36
# @Author : yysgz
# @File : clustering.py
# @Project : HAN_torch
# @Description :

import numpy as np
import torch

from sklearn.cluster import KMeans
from sklearn.metrics import normalized_mutual_info_score, adjusted_mutual_info_score, adjusted_rand_score

# 交集
def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def run_kmeans(extract_features, extract_labels, indices, isoPath=None):
    # extract the features and labels of the test tweets
    if isoPath is not None:
        # Remove isolated points
        temp = torch.load(isoPath)
        temp = temp.cpu().detach().numpy()  # detach()阻断反向传播，返回值为tensor；numpy()将tensor转换为numpy
        non_isolated_index = list(np.where(temp != 1)[0])  # np.where返回符合条件元素的索引index
        indices = intersection(indices, non_isolated_index)  # 取交集
    # Extract labels
    extract_labels = extract_labels.cpu().numpy()
    labels_true = extract_labels[indices]

    # Extrac features
    X = extract_features.cpu().detach().numpy()
    assert labels_true.shape[0] == X.shape[0]  # assert断言，在判断式false时触发异常
    n_test_tweets = X.shape[0]  # 100

    # Get the total number of classes
    n_classes = len(set(labels_true.tolist()))  # unique()和nunique()不香吗？

    # k-means clustering
    kmeans = KMeans(n_clusters=n_classes, random_state=0).fit(X)
    labels = kmeans.labels_

    nmi = normalized_mutual_info_score(labels_true, labels)  # 计算归一化互信息
    ami = adjusted_mutual_info_score(labels_true, labels)
    ari = adjusted_rand_score(labels_true, labels)  # 计算兰德系数

    # Return number of test tweets, number of classes covered by the test tweets, and KMeans clustering NMI
    return n_test_tweets, n_classes, nmi, ami, ari