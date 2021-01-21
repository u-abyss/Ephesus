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

# 基準となるファイルパスの順番
waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
waves_path_list = waves_path_npy.tolist()
# get only track_id
track_ids_in_order = get_track_ids_in_order(waves_path_list)

# ターゲットカテゴリに属するtrack_idのwave_path_list配列でのインデックスを求める
TARGET_CATEGORY = "jazz_blues"
target_category_track_ids = get_tracks_by_category(TARGET_CATEGORY)
# goal_indexの対象となるもの
goal_indexes = get_indexes(target_category_track_ids, track_ids_in_order)

SOURCE_CATEGORY = "classical"

# 1
source_category_track_ids = get_tracks_by_category(SOURCE_CATEGORY)

# 2
# start_indexの対象となるもの
start_indexes = get_indexes(source_category_track_ids, track_ids_in_order)

"""
ある一点のスタート地点（ソースカテゴリ）から
到達しうる全てのゴール地点（ターゲットカテゴリ）までグラフ構造を探索する
"""
results = []
for goal_index in goal_indexes:
    index_weight_list, passed_index = create_dijkstra_list(start_indexes[4], goal_index)
    results.append([index_weight_list, passed_index])

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

# passed_mp3_files = get_passed_mp3_files(passed_index)

# track_categories = get_track_category(passed_mp3_files)

# source_category_nums = get_source_category_nums(track_categories)

# # 1 -> 1.0, 0 -> 0.1に変換する
# normalized_values = normalize(source_category_nums)

# computed_index_weight_list = compute_path_weight(index_weight_list, normalized_values)

# ==============================================================================================================


# def run_algorithm_with_similarity_and_source_category_num(index_weight_list, passed_index):
#     track_ids = run_dijkstra(index_weight_list, passed_index)

# def run_algorithm_with_similarity(index_weight_list, passed_index):
#     track_ids = run_dijkstra(index_weight_list, passed_index)






    # # ノードの数
    # NODE_NUM = len(index_weight_list)

    # # 未探索のノード
    # unsearched_nodes = list(range(NODE_NUM))
    # # ノードごとの距離のリスト　(スタート地点から各ノードまでの距離)
    # distances_from_start = [math.inf] * NODE_NUM
    # previous_nodes = [-1] * NODE_NUM  # 最短経路でそのノードのひとつ前に到達するノードのリスト
    # distances_from_start[0] = 0  # 初期のノードの距離は0とする

    # """
    # 未探索ノードのうち,　そのノードまでの距離が最小のノードのindexを返す関数
    # """
    # def get_target_index(min_distance: float, distances_from_start: List[int], unsearched_nodes: List[int]) -> int:
    #     start = 0 # 検索をスタートする位置
    #     while True:
    #         index = distances_from_start.index(min_distance, start) # 最小の距離のノードのインデックス
    #         """
    #         まだ探索していないノードの対象のインデックスがある場合は，
    #         """
    #         found = index in unsearched_nodes
    #         if found:
    #             return index
    #         else:
    #             start = index + 1


    # """
    # 未探索のノードのうち,　距離が最も短いものを見つける
    # 返り値として,　最小の距離の値を返す.
    # """
    # def get_min_distance(distances_from_start, unsearched_nodes):
    #     min_distance = math.inf  # 最小の距離を保持する変数. 初期値はmath.inf
    #     for node_index in unsearched_nodes:
    #         # より短い距離のエッジがあった場合更新する.
    #         distance = distances_from_start[node_index]
    #         if min_distance > distance:
    #             min_distance = distance
    #     return min_distance


    # while(len(unsearched_nodes) != 0):  # 未探索ノードがなくなるまで繰り返す
    #     min_distance = get_min_distance(distances_from_start, unsearched_nodes)
    #     target_index = get_target_index(min_distance, distances_from_start, unsearched_nodes)  # 未探索ノードのうちで最小のindex番号を取得
    #     unsearched_nodes.remove(target_index)  # ここで探索するので未探索リストから除去
    #     edges_from_target_node = index_weight_list[target_index]  # ターゲットになるノードからのびるエッジのリスト
    #     for index, route_dis in enumerate(edges_from_target_node):
    #         if route_dis != 0: # 経路のコストは通過済みの経路となるため考慮しない．
    #             if distances_from_start[index] > (distances_from_start[target_index] + route_dis):
    #                 # 過去に設定されたdistanceよりも小さい場合はdistanceを更新
    #                 distances_from_start[index] = distances_from_start[target_index] + route_dis
    #                 # 　ひとつ前に到達するノードのリストも更新
    #                 previous_nodes[index] = target_index


    # routes = []
    # print("-----経路-----")
    # previous_node = NODE_NUM - 1
    # while previous_node != -1:
    #     if previous_node != 0:
    #         print(str(previous_node + 1) + " <- ", end='')
    #         routes.append(previous_node + 1)
    #     else:
    #         print(str(previous_node + 1))
    #         routes.append(previous_node + 1)
    #     previous_node = previous_nodes[previous_node]

    # print("-----距離-----")
    # print(distances_from_start[NODE_NUM - 1])
    # routes.reverse()
    # print(routes)

    # def get_recommended_track_ids(routes, passed_index):
    #     indexes = []
    #     for i in routes:
    #         index = passed_index[i-1]
    #         indexes.append(index)
    #     waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
    #     waves_path_list = waves_path_npy.tolist()
    #     pathes = []
    #     track_ids = []
    #     for index in indexes:
    #         path = waves_path_list[index]
    #         splited_path = path.split("/")[3]
    #         track_id = splited_path.split(".")[0]
    #         pathes.append(path)
    #         track_ids.append(track_id)
    #     return track_ids

    # track_ids = get_recommended_track_ids(routes, passed_index)
    # print(track_ids)


"""
任意のスタート地点一点から到達する可能性のあるターゲットカテゴリに属するノードまでの経路を計算する
"""

def get_all_recommended_routes(results, param):
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
            recommended_track_ids = run_dijkstra(index_weight_list, passed_index)
            print("類似度のみ:",recommended_track_ids)
        else:
            # 各ノードがいくつのソースカテゴリに属しているのかを調べる
            source_category_nums = get_source_category_nums(categories)
            normalized_values = normalize(source_category_nums)
            computed_index_weight_list = compute_path_weight(index_weight_list, normalized_values, 1)

            # ダイクストラアルゴリズムを実行する
            recommended_track_ids = run_dijkstra(index_weight_list, passed_index)
            print("x:",recommended_track_ids)
            recommended_track_ids = run_dijkstra(computed_index_weight_list, passed_index)
            print("y:",recommended_track_ids)
            print("========================================================================")

get_all_recommended_routes(results, 0.5)
