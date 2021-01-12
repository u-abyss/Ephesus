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

def get_wave_file_path_list():
    path = "../ismir04_genre/wave"
    wave_files = os.listdir(path)
    wave_path_list = []

    for wave_file in wave_files:
        wave_path = path + "/" + wave_file
        wave_path_list.append(wave_path)

    return wave_path_list

# np.save('../ismir04_genre/wave_path_list', wave_path_list)

feature_type = Feature_Types.MFCC

wave_path_npy = np.load("../ismir04_genre/wave_path_list.npy")

wave_path_list = wave_path_npy.tolist()

# reversed_wave_path_list = list(reversed(wave_path_list))

# 各wavファイルの振幅データ列とサンプリング周波数を取得し、リストに格納
x_and_fs_list = []
for path in wave_path_list:
    x, fs = librosa.load(path, DEFAULT_FS)
    x_and_fs_list.append((x, fs))

# np.save("../ismir04_genre/x_and_fs_list", x_and_fs_list)

# test = np.load("../ismir04_genre/x_and_fs_list.npy", allow_pickle=True)

# x_and_fs_list = test.tolist()

# 使用する特徴量を抽出し、リストに格納
feature_list = []
for x_and_fs in x_and_fs_list:
    x = x_and_fs[0]
    fs = x_and_fs[1]
    feature = librosa.feature.mfcc(x, fs)
    feature_list.append(feature)

# # # print("")

# # (3) 類似度計算
# # print("#3 [Evaluation]")

LIST_LEN = len(wave_path_list)

not_need = [
    "artist_6_album_2_track_2",
    "artist_26_album_1_track_2",
    "artist_33_album_2_track_3",
    "artist_40_album_3_track_3",
    "artist_73_album_1_track_5",
    "artist_77_album_1_track_2",
    "artist_84_album_1_track_2",
    "artist_115_album_3_track_2",
    "artist_122_album_1_track_3",
    "artist_124_album_4_track_2",
]

for index in range(LIST_LEN):
    # 比較の基準とする特徴量
    reference_feature = feature_list[index]
    audio_name = wave_path_list[index]
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

    np.save(f'../ismir04_genre/similarities/{audio_name}', eval_list)
    print("good")