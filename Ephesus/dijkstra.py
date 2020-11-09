import math
from typing import List, Dict

route_list = [[0, 50, 80, 0, 0], [0, 0, 20, 15, 0], [0, 0, 0, 10, 15], [
    0, 0, 0, 0, 30], [0, 0, 0, 0, 0]]  # 初期のノード間の距離のリスト

NODE_NUM = len(route_list)  # ノードの数

unsearched_nodes = list(range(NODE_NUM))  # 未探索ノード
# ノードごとの距離のリスト　(スタート地点から各ノードまでの距離)
distances_from_start = [math.inf] * NODE_NUM
previous_nodes = [-1] * NODE_NUM  # 最短経路でそのノードのひとつ前に到達するノードのリスト
distances_from_start[0] = 0  # 初期のノードの距離は0とする


"""
未探索ノードのうち,　そのノードまでの距離が最小のノードのindexを返す関数
"""


def get_target_index(min_distance: float, distances_from_start: List[int], unsearched_nodes: List[int]) -> int:
    start = 0
    while True:
        index = distances_from_start.index(min_distance, start)
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
    target_index = get_target_index(
        min_distance, distances_from_start, unsearched_nodes)  # 未探索ノードのうちで最小のindex番号を取得
    unsearched_nodes.remove(target_index)  # ここで探索するので未探索リストから除去
    target_edge = route_list[target_index]  # ターゲットになるノードからのびるエッジのリスト
    for index, route_dis in enumerate(target_edge):
        if route_dis != 0:
            if distances_from_start[index] > (distances_from_start[target_index] + route_dis):
                # 過去に設定されたdistanceよりも小さい場合はdistanceを更新
                distances_from_start[index] = distances_from_start[target_index] + route_dis
                # 　ひとつ前に到達するノードのリストも更新
                previous_nodes[index] = target_index

print("-----経路-----")
previous_node = NODE_NUM - 1
while previous_node != -1:
    if previous_node != 0:
        print(str(previous_node + 1) + " <- ", end='')
    else:
        print(str(previous_node + 1))
    previous_node = previous_nodes[previous_node]

print("-----距離-----")
print(distances_from_start[NODE_NUM - 1])
