"""
提案アルゴリズムを適応させるための配列を作成するモジュール
"""
import math
import numpy as np
from typing import List, Dict

# 推薦のスタートとなる音声のインデックスを引数とする
START_INDEX = 700
MAX_SIMILARITY = 1.3
MIN_SIMILARITY = 1.0

audio_similarty = np.load("../../ismir04_genre/final_similarity_matrix.npy")
audio_similarty_list = audio_similarty.tolist()

def reverse_similarity_value(arr):
    reversed_similarities_list = []
    for row in arr:
        new_row = []
        for value in row:
            if value == 0:
                continue
            reversed_value = 1 / value
            new_row.append(reversed_value)
        reversed_similarities_list.append(new_row)
    return reversed_similarities_list

audio_similarty_list = reverse_similarity_value(audio_similarty_list)

def append_list(prev_list):
    new_list = []
    for row in prev_list:
        for idx in row:
            new_list.append(idx)
    return new_list

def remove_empty_list(prev_list):
    new_list = [x for x in prev_list if x != []]
    return new_list

passed_index = [START_INDEX]

def get_first_next_target_indexes(start_index):
    next_target_index = []
    index_weight_list = []
    index_weight = [0]
    for index, weight in enumerate(audio_similarty_list[start_index]):
        if index == START_INDEX:
            continue
        elif MIN_SIMILARITY < weight < MAX_SIMILARITY:
            index_weight.append(weight)
            next_target_index.append(index)
    index_weight_list.append(index_weight)
    return next_target_index, index_weight_list

def get_route(targets, index_weight_list):
    index_weight_list = index_weight_list
    next_target_indexes = []
    first_search_indexes = []
    num = 1
    for idx in targets:
        if num > 20000:
            return index_weight_list
        if idx in passed_index:
            continue
        target_indexes = []
        passed_index_len = len(passed_index)
        index_weight = [0] * passed_index_len
        # インデックスがidxのノードから伸びるノードのインデックスの配列を求める.[fulfilling_condition_indexes]
        fulfilling_condition_indexes = []
        for index, weight in enumerate(audio_similarty_list[idx]):
            # if weight < weight_criteria:
            if MIN_SIMILARITY < weight < MAX_SIMILARITY:
                fulfilling_condition_indexes.append(index)

        # すでに調査済みのノードに対して枝が張られているものを，除外する．
        for index in passed_index:
            if index in fulfilling_condition_indexes:
                fulfilling_condition_indexes.remove(index)
        # 現在のidxを除外する.
        if idx in fulfilling_condition_indexes:
            fulfilling_condition_indexes.remove(idx)

        # targetsの中で，まだ探索していないものを調べる
        for index in targets:
            if index in passed_index:
                continue
            if index in fulfilling_condition_indexes:
                index_weight.append(audio_similarty_list[idx][index])
                fulfilling_condition_indexes.remove(index)
            else:
                # 現在探索しているノード自身との類似度のため，0を代入する
                index_weight.append(0)
        # 先に調べるべきノードのインデックスを調べる.next_target_indexesの中の要素
        for index in first_search_indexes:
            if index in fulfilling_condition_indexes:
                index_weight.append(audio_similarty_list[idx][index])
                fulfilling_condition_indexes.remove(index)
            else:
                index_weight.append(0)

        first_search_indexes.extend(fulfilling_condition_indexes)
        for index in fulfilling_condition_indexes:
            index_weight.append(audio_similarty_list[idx][index])
            target_indexes.append(index)
        next_target_indexes.append(target_indexes)
        index_weight_list.append(index_weight)
        passed_index.append(idx)
        num += 1

    next_target_indexes = remove_empty_list(next_target_indexes)
    next_target_indexes = append_list(next_target_indexes)
    if len(next_target_indexes) == 0:
        return index_weight_list
    else:
        return get_route(next_target_indexes, index_weight_list)

def add_or_remove_eles_in_list(weight_list):
    length = len(weight_list)
    NODE_NUM = len(passed_index)
    index_weight_list = []
    for row in weight_list:
        row_num = len(row)
        if row_num == NODE_NUM:
            index_weight_list.append(row)
        elif row_num < NODE_NUM:
            needed_zero_num = NODE_NUM - row_num
            add_zero_arr = [0] * needed_zero_num
            row.extend(add_zero_arr)
            index_weight_list.append(row)
        else:
            unused_node_num = row_num - NODE_NUM
            del(row[-unused_node_num:])
            index_weight_list.append(row)
    return index_weight_list

next_target_index, index_weight_list = get_first_next_target_indexes(START_INDEX)

index_weight_list = get_route(next_target_index, index_weight_list)

# 提案アルゴリズムに適応可能な配列（index_weight_list）
index_weight_list = add_or_remove_eles_in_list(index_weight_list)

# ========================================================================================================

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

# print("-----経路-----")
# previous_node = NODE_NUM - 1
# while previous_node != -1:
#     if previous_node != 0:
#         print(str(previous_node + 1) + " <- ", end='')
#     else:
#         print(str(previous_node + 1))
#     previous_node = previous_nodes[previous_node]

# print("-----距離-----")
# print(distances_from_start[NODE_NUM - 1])
