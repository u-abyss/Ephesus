import glob
import pandas as pd
import numpy as np

"""
１ベクトルが全ての音楽との類似度の値を要素とする行列を作成する関数

"../ismir04_genre/final_similarity_matrix"へnpy形式で保存する．

ex>
# [0, 9, 8, 5],
# [9, 0, 3, 6],
# [8, 3, 0, 1],
# [5, 6, 1, 0],
"""

waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")

# 基準となるファイルパスの順番
waves_path_list = waves_path_npy.tolist()

def get_track_ids_in_order(path_lists):
    track_ids = []
    for path in waves_path_list:
        splited_path = path.split("/")[3]
        track_id = splited_path.split(".")[0]
        track_ids.append(track_id)
    return track_ids

track_ids = get_track_ids_in_order(waves_path_list)

# sorted_path_npy = []

# for track_id in track_ids:
#     path = "../../ismir04_genre/similarities/" + track_id + ".npy"
#     sorted_path_npy.append(path)

# def create_similarity_matrix():
#     audio_similarity_matrix = []
#     for path in sorted_path_npy:
#         similarity_list = np.load(path)
#         audio_similarity_matrix.append(similarity_list)
#     return audio_similarity_matrix

# similarity_matrix = np.load("../../ismir04_genre/similarity_matrix.npy")
# similarity_matrix_list = similarity_matrix.tolist()

# def replace_eles_of_similarity_list(arr):
#     new_similarities_list = []
#     for idx, row in enumerate(arr):
#         if idx == 0:
#             new_similarities_list.append(row)
#             continue
#         else:
#             replaced_eles = []
#             for i in range(idx):
#                 ele = arr[i][idx]
#                 replaced_eles.append(ele)
#             for i in range(idx):
#                 row[i] = replaced_eles[i]
#             new_similarities_list.append(row)
#     return new_similarities_list

# new_similarities_list = replace_eles_of_similarity_list(similarity_matrix_list)