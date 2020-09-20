"""
This is the recommendation algorithm based on Matrix Decomposition.
"""

import pandas as pd
from getMusicLists import get_music_lists
import numpy as np
import torch
import torch.nn as nn

lst2music, music2lst = get_music_lists()


def getRatingMatrix(music_list):
    """
    music_list is a List composed of input songs
    """
    ratingMatrix = np.zeros((len(lst2music)+1, len(music2lst)), dtype=np.float32)
    # print(f'ratingMatrix.shape: {ratingMatrix.shape}')

    music2num, num2music = {}, {}  # dict converting music and num
    cnt = 0
    for music in music2lst:
        music2num[music] = cnt
        num2music[cnt] = music
        cnt += 1
    # print(f'cnt: {cnt}')

    cnt = 0
    for lst in lst2music.keys():
        for music in lst2music[lst]:
            ratingMatrix[cnt, music2num[music]] = 1
        cnt += 1
    for music in music_list:
        ratingMatrix[cnt, music2num[music]] = 1
    # print(ratingMatrix.sum(1))

    return ratingMatrix, num2music


def matrixDecomposition(matrix, k):
    User = torch.rand((matrix.shape[0], k), requires_grad=True)
    Item = torch.rand((k, matrix.shape[1]), requires_grad=True)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam([User, Item], lr=0.1, weight_decay=0.1)

    for cnt in range(50):
        matrix_ = torch.mm(User, Item)
        # print(matrix.shape, matrix_.shape)
        loss = criterion(matrix_, torch.tensor(matrix))
        # if cnt % 10 == 9:
        #     # print(matrix_[:5, :5])
        #     print(f'loss of {cnt} step: {loss.item()}')
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    return User.detach().numpy(), Item.detach().numpy()


def recommend(music_list):
    matrix, num2music = getRatingMatrix(music_list)
    User, Item = matrixDecomposition(matrix, 50)
    predRating = np.matmul(User[-1], Item)
    recommendation = []
    for i in range(predRating.shape[0]):
        recommendation.append((num2music[i], predRating[i]))
    recommendation.sort(key=lambda val: val[1], reverse=True)
    return set([x[0] for x in recommendation[:10]]) - music_list


# print('Matrix:', recommend({'呼吸', '无人之岛（翻自 任然）', '水星记', '像鱼', '大鱼 - (动画电影《大鱼海棠》印象曲)',
        #    '千千阙歌(Live)', '心はいつもあなたのそばに Piano'}))
