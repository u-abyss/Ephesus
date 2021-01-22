import math
import numpy as np
import pandas as pd
from typing import List, Dict

from category import get_tracks_by_category
from dijkstra import normalize, compute_path_weight, run_dijkstra
from route import create_dijkstra_list
from similarity import get_track_ids_in_order
from index import get_indexes


"""
1. ソースカテゴリの入力
2. 1.のカテゴリに属するtrack_idのwave_path_list配列でのインデックスを求める(start_indexes)
3. ターゲットカテゴリの入力
4. 3.のカテゴリに属するtrack_idのwave_path_list配列でのインデックスを求める(goal_indexes)
5. 2. 4. をそうあたりで提案アルゴリズムを適応できるような配列を生成する
6. 5.で求めた配列に対して提案アルゴリズムを適応させる（類似度のみを考慮）(類似度 + ノードが属するソース分野の数を考慮)
"""
SOURCE_CATEGORY = "classical"
TARGET_CATEGORY = "world"

# 基準となるファイルパスの順番
waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
waves_path_list = waves_path_npy.tolist()

# get only track_id
track_ids_in_order = get_track_ids_in_order(waves_path_list)

# ターゲットカテゴリに属するtrack_idのwave_path_list配列でのインデックスを求める

target_category_track_ids = get_tracks_by_category(TARGET_CATEGORY)
# goal_indexの対象となるもの
goal_indexes = get_indexes(target_category_track_ids, track_ids_in_order)

# 1
source_category_track_ids = get_tracks_by_category(SOURCE_CATEGORY)

# 2
# start_indexの対象となるもの
start_indexes = get_indexes(source_category_track_ids, track_ids_in_order)
print("fdafafada:",len(start_indexes))

"""
ある一点のスタート地点（ソースカテゴリ）から
到達しうる全てのゴール地点（ターゲットカテゴリ）までグラフ構造を探索する
"""

print(start_indexes[0])
print(goal_indexes)

# all_results = []
# for start_index in start_indexes:
results = []
for goal_index in goal_indexes:
    index_weight_list, passed_index = create_dijkstra_list(start_indexes[100], goal_index)
    results.append([index_weight_list, passed_index])
# all_results.append(results)

# np.save("../../ismir04_genre/result/world_classical", all_results)

# ================================================================================================================================================


"""
通過したtrackのインデックスから，track_id + .mp3の形式に変換する関数
"""
def get_passed_mp3_files(passed_index):
    passed_mp3_files = []
    for index in passed_index:
        path = waves_path_list[index]
        splited_path = path.split("/")[3]
        track_id = splited_path.split(".")[0]
        mp3_name = track_id + ".mp3"
        passed_mp3_files.append(mp3_name)
    return passed_mp3_files

"""
mp3ファイルから，そのtrackが属するカテゴリを返す関数
"""
def get_track_category(mp3_files):
    categories = []
    for mp3_file in mp3_files:
        row = category_and_file_path_df.query('file_path == @mp3_file')
        category = (row.category).to_list()
        categories.append(category[0])
    return categories

"""
グラフ構造上における各ノードが属するソースカテゴリの数の配列を返す関数
"""
def get_source_category_nums(categories):
    source_category_nums = []
    for category in categories:
        if category == SOURCE_CATEGORY:
            source_category_nums.append(1)
        else:
            source_category_nums.append(0)
    return source_category_nums

audio_metadata_df = pd.read_csv('../../ismir04_genre/metadata/development/tracklist.csv', names=('category', 'artist_id', 'album_id', 'track_id', 'track_number', 'file_path'))
category_and_file_path_df = audio_metadata_df.loc[:,['category','file_path']]

"""
任意のスタート地点一点から到達する可能性のあるターゲットカテゴリに属するノードまでの経路を計算する
"""

def get_all_recommended_routes(results, param):
    # min_total_weight = 100
    RESULT_LEN = len(results)
    for idx in range(RESULT_LEN):
        # アルゴリズムの適応対象となるグラフ構築をする際のデータ
        result = results[idx]
        index_weight_list = result[0]
        passed_index = result[1]

        # 全ノードのmp3名を取得する
        passed_track_mp3_names = get_passed_mp3_files(passed_index)

        # mp3名からその音楽のカテゴリを取得する
        categories = get_track_category(passed_track_mp3_names)

        # エッジの重みを計算する際のパラメータが0の時は，類似度のみを考慮する．（各ノードが属するソースカテゴリの数は考慮しない）
        if param == 0:
            # ダイクストラアルゴリズムを実行する
            recommended_track_ids, total_weight = run_dijkstra(index_weight_list, passed_index)
            print("類似度のみ:",recommended_track_ids)
        else:
            # 各ノードがいくつのソースカテゴリに属しているのかを調べる
            source_category_nums = get_source_category_nums(categories)
            normalized_values = normalize(source_category_nums)
            computed_index_weight_list = compute_path_weight(index_weight_list, normalized_values, param)

            # ダイクストラアルゴリズムを実行する
            # recommended_track_ids, total_weight = run_dijkstra(index_weight_list, passed_index)
            # print("x:",recommended_track_ids)
            recommended_track_ids, total_weight = run_dijkstra(computed_index_weight_list, passed_index)
            print(recommended_track_ids, total_weight)
            # if total_weight < min_total_weight:
            #     min_total_weight = total_weight
            # print("y:",recommended_track_ids)
            # print("========================================================================")
        # return recommended_track_ids, min_total_weight



# all_results = np.load("../../ismir04_genre/result/world_jazz.npy", allow_pickle=True)

# print(results)

get_all_recommended_routes(results, 0)

# min_weight_and_recommened_track_ids = []
# for results in all_results:
#     # start_indexesの中の任意のstart_indexからターゲットカテゴリに属するノードまでの最小コスト(total_weight)
#     _recommended_track_ids, _min_total_weight = get_all_recommended_routes(results, 0.5)
#     min_weight_and_recommened_track_ids.append([_recommended_track_ids, _min_total_weight])

# # print(min_weight_and_recommened_track_ids)
# sorted_min_weight_and_recommened_track_ids = sorted(min_weight_and_recommened_track_ids, reverse=True, key=lambda x: x[1])
# print(sorted_min_weight_and_recommened_track_ids)
# # get_all_recommended_routes(results, 0)
