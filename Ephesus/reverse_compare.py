import time
from enum import Enum
import numpy as np
import librosa
import os

import csv
import pprint
import pandas as pd


# 自動でリサンプリングされるときのサンプリング周波数
DEFAULT_FS = 44100

# 特徴量の種類
class Feature_Types(Enum):
    SPECTRUM = 1
    SPECTRUM_CENTROID = 2
    MFCC = 3

# 使用する特徴量の種類
feature_type = Feature_Types.MFCC

wave_path_npy = np.load("../ismir04_genre/wave_path_list.npy")

wave_path_list = wave_path_npy.tolist()

reversed_wave_path_list = list(reversed(wave_path_list))


# 各wavファイルの振幅データ列とサンプリング周波数を取得し、リストに格納
x_and_fs_list = []
for path in reversed_wave_path_list:
    x, fs = librosa.load(path, DEFAULT_FS)
    x_and_fs_list.append((x, fs))

# # (2) 特徴抽出

# 使用する特徴量を抽出し、リストに格納
feature_list = []
for x_and_fs in x_and_fs_list:
    x = x_and_fs[0]
    fs = x_and_fs[1]
    feature = librosa.feature.mfcc(x, fs)
    feature_list.append(feature)

# np.save("../ismir04_genre/feature_list", feature_list)

# print(feature_list)
# print(len(feature_list))

# # (3) 類似度計算
LIST_LEN = len(reversed_wave_path_list)

eval_list_append = eval_list.append

for index in range(LIST_LEN):
    # 比較の基準とする特徴量
    reference_feature = feature_list[index]
    audio_name = reversed_wave_path_list[index]
    audio_name = audio_name.split("/")[3]
    audio_name = audio_name.split(".")[0]

    # 類似度を計算し、リストに格納
    eval_list = []
    for target_feature in feature_list:
        ac, wp = librosa.sequence.dtw(reference_feature, target_feature)
        eval = 1 - (ac[-1][-1] / np.array(ac).max())
        eval_listappend(eval)

    np.save(f'../ismir04_genre/npy/reverse/{audio_name}', eval_list)
    print("good")
