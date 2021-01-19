import math
from typing import List, Dict

"""
route_listの[0,0]がスタートノード
            [n, n]がゴールノード
"""

route_list = [
    [0, 0.8, 0.6, 0, 0, 0, 0, 0, 0],
    [0, 0, 0.5, 0.4, 0, 0, 0, 0, 0],
    [0, 0, 0, 0.9, 0.2, 0.7, 0, 0, 0],
    [0, 0, 0, 0, 0.8, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0.5, 0.4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0.9, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0.8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0.6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
]  # 初期のノード間の距離のリスト

# 各ノードが持つユーザのお気に入りのカテゴリの数
# fave_categories_nums = [1, 0, 3, 2, 2]

"""
min-maxスケーリングにより，正規化を行う
l(normalization) = l(i) - s(最大値) / s(最大値) - 0(最小値)
s = 3
"""
def normalize(fave_categories_nums):
    normalized_values = []
    for fave_num in fave_categories_nums:
        l = (fave_num - 0) / 1
        print(l)
        if l == 0:
            l = 0.1
        normalized_values.append(l)
    return normalized_values

# normalized_values = normalize(fave_categories_nums)
# print(normalized_values)

"""
好きなカテゴリーの数が0の時は，掛けない
"""

def compute_path_weight(route_list, normalized_values):
    final_route_list = []
    for row in route_list:
        new_row = []
        for index, similarity in enumerate(row):
            final_path_weight = similarity * normalized_values[index]
            if final_path_weight != 0:
                final_path_weight = 1 / final_path_weight
            new_row.append(final_path_weight)
        final_route_list.append(new_row)
    return final_route_list

# print(compute_path_weight(route_list, normalized_values))

# final_route_list = compute_path_weight(route_list, normalized_values)


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

# print(previous_nodes)

