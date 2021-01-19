import math
import numpy as np
import pandas as pd
from typing import List, Dict

from category import get_tracks_by_category
from dijkstra import normalize, compute_path_weight
from route import create_dijkstra_list
from similarity import get_track_ids_in_order


"""
1. ソースカテゴリの入力
2. 1.のカテゴリに属するtrack_idのwave_path_list配列でのインデックスを求める
3. それぞれについて提案アルゴリズムに適応できるように配列を生成する
4. それぞれについて提案アルゴリズムを適応させる
"""

source_category = "world"

# 1
track_ids = get_tracks_by_category("metal_punk")

# 2
# 基準となるファイルパスの順番
waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
waves_path_list = waves_path_npy.tolist()

# get only track_id
track_ids_in_order = get_track_ids_in_order(waves_path_list)

# start_indexの対象となるもの

def get_start_indexes(track_ids):
    start_indexes = []
    for track_id in track_ids:
        index = track_ids_in_order.index(track_id)
        start_indexes.append(index)
    return start_indexes

start_indexes = get_start_indexes(track_ids)

# 3
index_weight_list, passed_index = create_dijkstra_list(start_indexes[4])
# print("passed:", passed_index)

def get_track_mp3_names(passed_index):
    passed_track_mp3_names = []
    for index in passed_index:
        path = waves_path_list[index]
        splited_path = path.split("/")[3]
        track_id = splited_path.split(".")[0]
        mp3_name = track_id + ".mp3"
        passed_track_mp3_names.append(mp3_name)
    return passed_track_mp3_names

passed_track_mp3_names = get_track_mp3_names(passed_index)

print(passed_track_mp3_names)

audio_metadata_df = pd.read_csv('../../ismir04_genre/metadata/development/tracklist.csv', names=('category', 'artist_id', 'album_id', 'track_id', 'track_number', 'file_path'))
category_and_file_path_df = audio_metadata_df.loc[:,['category','file_path']]

def get_track_category(mp3_files):
    categories = []
    for mp3_file in mp3_files:
        row = category_and_file_path_df.query('file_path == @mp3_file')
        category = (row.category).to_list()
        categories.append(category[0])
    return categories

categories = get_track_category(passed_track_mp3_names)

def get_source_category_nums(categories):
    source_category_nums = []
    for category in categories:
        if category == source_category:
            source_category_nums.append(1)
        else:
            source_category_nums.append(0)
    return source_category_nums

source_category_nums = get_source_category_nums(categories)
print(source_category_nums)

"""
1 -> 1.0
0 -> 0.1
"""

normalized_values = normalize(source_category_nums)
print(normalized_values)

index_weight_list = compute_path_weight(index_weight_list, normalized_values)


# ノードの数
NODE_NUM = len(index_weight_list)

# 未探索のノード
unsearched_nodes = list(range(NODE_NUM))
# ノードごとの距離のリスト　(スタート地点から各ノードまでの距離)
distances_from_start = [math.inf] * NODE_NUM
previous_nodes = [-1] * NODE_NUM  # 最短経路でそのノードのひとつ前に到達するノードのリスト
distances_from_start[0] = 0  # 初期のノードの距離は0とする

"""
未探索ノードのうち,　そのノードまでの距離が最小のノードのindexを返す関数
"""
def get_target_index(min_distance: float, distances_from_start: List[int], unsearched_nodes: List[int]) -> int:
    start = 0 # 検索をスタートする位置
    while True:
        index = distances_from_start.index(min_distance, start) # 最小の距離のノードのインデックス
        """
        まだ探索していないノードの対象のインデックスがある場合は，
        """
        found = index in unsearched_nodes
        if found:
            return index
        else:
            start = index + 1


"""
未探索のノードのうち,　距離が最も短いものを見つける
返り値として,　最小の距離の値を返す.
"""
def get_min_distance(distances_from_start, unsearched_nodes):
    min_distance = math.inf  # 最小の距離を保持する変数. 初期値はmath.inf
    for node_index in unsearched_nodes:
        # より短い距離のエッジがあった場合更新する.
        distance = distances_from_start[node_index]
        if min_distance > distance:
            min_distance = distance
    return min_distance


while(len(unsearched_nodes) != 0):  # 未探索ノードがなくなるまで繰り返す
    min_distance = get_min_distance(distances_from_start, unsearched_nodes)
    target_index = get_target_index(min_distance, distances_from_start, unsearched_nodes)  # 未探索ノードのうちで最小のindex番号を取得
    unsearched_nodes.remove(target_index)  # ここで探索するので未探索リストから除去
    edges_from_target_node = index_weight_list[target_index]  # ターゲットになるノードからのびるエッジのリスト
    for index, route_dis in enumerate(edges_from_target_node):
        if route_dis != 0: # 経路のコストは通過済みの経路となるため考慮しない．
            if distances_from_start[index] > (distances_from_start[target_index] + route_dis):
                # 過去に設定されたdistanceよりも小さい場合はdistanceを更新
                distances_from_start[index] = distances_from_start[target_index] + route_dis
                # 　ひとつ前に到達するノードのリストも更新
                previous_nodes[index] = target_index


routes = []
print("-----経路-----")
previous_node = NODE_NUM - 1
while previous_node != -1:
    if previous_node != 0:
        print(str(previous_node + 1) + " <- ", end='')
        routes.append(previous_node + 1)
    else:
        print(str(previous_node + 1))
        routes.append(previous_node + 1)
    previous_node = previous_nodes[previous_node]

print("-----距離-----")
print(distances_from_start[NODE_NUM - 1])
routes.reverse()
print(routes)

def get_recommended_track_ids(routes, passed_index):
    indexes = []
    for i in routes:
        index = passed_index[i-1]
        indexes.append(index)
    waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
    waves_path_list = waves_path_npy.tolist()
    pathes = []
    track_ids = []
    for index in indexes:
        path = waves_path_list[index]
        splited_path = path.split("/")[3]
        track_id = splited_path.split(".")[0]
        pathes.append(path)
        track_ids.append(track_id)
    return track_ids

track_ids = get_recommended_track_ids(routes, passed_index)
print(track_ids)
