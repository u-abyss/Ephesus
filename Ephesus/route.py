"""
提案アルゴリズムを適応させるための配列を作成するモジュール
"""
import numpy as np

movie_similarity = np.load("../data/movie_similarity.npy")
movie_similarity_list = movie_similarity.tolist()

def append_list(prev_list):
    new_list = []
    for row in prev_list:
        for idx in row:
            new_list.append(idx)
    return new_list

def remove_empty_list(prev_list):
    new_list = [x for x in prev_list if x != []]
    return new_list

def get_route(targets):
    next_target_indexes = []
    for idx in targets:
        if idx in passed_index:
            continue
        previous_index = idx
        target_indexes = []
        index_weight = [idx]
        for index, weight in enumerate(movie_similarity_list[idx]):
            if index == previous_index:
                weight = 0
                index_weight.append([index, weight])
            elif index in passed_index:
                # TODO: 既存の配列に追加する処理の関数を記述
                weight = 0
                index_weight.append([index, weight])
            elif weight < 1.5:
                index_weight.append([index, weight])
                if index not in targets:
                    target_indexes.append(index)
        next_target_indexes.append(target_indexes)
        index_weight_list.append(index_weight)
        passed_index.append(idx)
    next_target_indexes = remove_empty_list(next_target_indexes)
    next_target_indexes = append_list(next_target_indexes)
    if len(next_target_indexes) == 0:
        print("finish")
    else:
        return get_route(next_target_indexes)

weight_criteria = 1.5
# 推薦のスタートとなる映画のインデックスを引数とする
START_INDEX = 0

passed_index = [START_INDEX]
next_target_index = []
index_weight_list = []

print(movie_similarity_list[0])
index_weight = [0]
for index, weight in enumerate(movie_similarity_list[START_INDEX]):
    if index == START_INDEX:
        weight = 0
        index_weight.append([index, weight])
    elif weight < 1.5:
        index_weight.append([index, weight])
        next_target_index.append(index)
index_weight_list.append(index_weight)
print(index_weight_list)
print("next_target_index:", next_target_index)
print("")
#TODO: 残りのノードの数分の0を配列の末尾に追加
print("index_weight_list:", index_weight_list)
print("")
print("=============================================")

next_target_indexes = get_route(next_target_index)
for row in index_weight_list:
    print(row)
    print("")

print(len(index_weight_list))
print(index_weight_list[2])
print(len(passed_index))

print("")
print(passed_index)
