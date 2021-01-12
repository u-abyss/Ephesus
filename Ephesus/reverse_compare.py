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

# reversed_wave_path_list = [
#     "../ismir04_genre/wave/artist_100_album_1_track_1.wav",
#     "../ismir04_genre/wave/artist_100_album_1_track_2.wav",
#     "../ismir04_genre/wave/artist_100_album_1_track_3.wav",
#     # "../ismir04_genre/wave/artist_100_album_1_track_4.wav",
#     # "../ismir04_genre/wave/artist_100_album_2_track_1.wav",
# ]


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

# # (3) 類似度計算
LIST_LEN = len(reversed_wave_path_list)

# def compute_similarity(reference, target):
#     ac, wp = librosa.sequence.dtw(reference, target)
#     eval = 1 - (ac[-1][-1] / np.array(ac).max())
#     return eval

# start = time.time()

# test = [compute_similarity(x, y) for x in feature_list for y in feature_list]
# print(test)

# end = time.time()
# # 処理時間表示
# print("Total elapsed time : {}[sec]".format(round(end - start, 4)))

not_need = [
    "artist_9_album_3_track_5",
    "artist_46_album_1_track_3",
    "artist_106_album_2_track_3",
]

for index in range(LIST_LEN):
    # 比較の基準とする特徴量
    reference_feature = feature_list[index]
    audio_name = reversed_wave_path_list[index]
    audio_name = audio_name.split("/")[3]
    audio_name = audio_name.split(".")[0]

    if audio_name in not_need:
        print('continue')
        continue

    # 類似度を計算し、リストに格納
    eval_list = []
    eval_list_append = eval_list.append
    for idx in range(LIST_LEN):
        target_feature = feature_list[idx]
        if index == idx:
            eval = 1
            eval_list_append(eval)
        elif idx < index:
            eval = 10
            eval_list_append(eval)
        else:
            ac, wp = librosa.sequence.dtw(reference_feature, target_feature)
            eval = 1 - (ac[-1][-1] / np.array(ac).max())
            eval_list_append(eval)

    np.save(f'../ismir04_genre/npy/reverse/{audio_name}', eval_list)
    print("good")

