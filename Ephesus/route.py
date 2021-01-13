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
        previous_index = idx
        target_indexes = []
        index_weight = []
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

    print("passed_index:", passed_index)
    print("")
    print("next_target_indexes", next_target_indexes)
    print("=============================================")
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
index_weight_list = [0]


for index, weight in enumerate(movie_similarity_list[START_INDEX]):
    if index == START_INDEX:
        index_weight_list.append([0,0])
    elif weight < 1.5:
        index_weight_list.append([index,weight])
        next_target_index.append(index)

print("next_target_index:", next_target_index)
print("")
#TODO: 残りのノードの数分の0を配列の末尾に追加
print("index_weight_list:", index_weight_list)
print("")
print("=============================================")

# next_target_index = append_list(next_target_index)

next_target_indexes = get_route(next_target_index)

# next2_targets = []
# for idx in next_target_index: # 49, 120, 180
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     # 探索対象のノードのインデックスを各配列の先頭に追加
#     index_weight.append(idx)
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             #TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             next_target_indexes.append(index)
#     next2_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)

# print("next2_targets", next2_targets)
# print("")
# print("index_weight_list")
# # for row in index_weight_list:
# #     print(row)
# #     print("")
# print("=============================================")

# next3_targets = []



# targets = append_list(next2_targets)

# print("targets:", targets)
# for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             # TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             if index not in targets:
#                 next_target_indexes.append(index)
#     next3_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)
# print("passed_index:", passed_index)
# print("")
# # 空のリストを削除

# next3_targets = remove_empty_list(next3_targets)
# print("next3_targets", next3_targets)
# print("")

# targets = append_list(next3_targets)

# next4_targets = []
# for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             # TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             if index not in targets:
#                 next_target_indexes.append(index)
#     next4_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)
# print("passed_index:", passed_index)
# print("")

# next4_targets = remove_empty_list(next4_targets)

# targets = append_list(next4_targets)

# next5_targets = []
# for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             # TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             if index not in targets:
#                 next_target_indexes.append(index)
#     next5_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)
# print("passed_index:", passed_index)
# print("")

# next5_targets = remove_empty_list(next5_targets)
# targets = append_list(next5_targets)

# next6_targets = []
# for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             # TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             if index not in targets:
#                 next_target_indexes.append(index)
#     next6_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)
# print("passed_index:", passed_index)
# print("")
# print("next6_targets", next6_targets)
# print("=============================================")

# next6_targets = remove_empty_list(next6_targets)
# targets = append_list(next6_targets)

# next7_targets = []
# for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#     previous_index = idx
#     next_target_indexes = []
#     index_weight = []
#     for index, weight in enumerate(movie_similarity_list[idx]):
#         if index == previous_index:
#             weight = 0
#             index_weight.append([index, weight])
#         elif index in passed_index:
#             # TODO: 既存の配列に追加する処理の関数を記述
#             weight = 0
#             index_weight.append([index, weight])
#         elif weight < 1.5:
#             index_weight.append([index, weight])
#             if index not in targets:
#                 next_target_indexes.append(index)
#     next7_targets.append(next_target_indexes)
#     index_weight_list.append(index_weight)
#     passed_index.append(idx)
# print("passed_index:", passed_index)
# print("")
# print("next7_targets", next7_targets)
# print("=============================================")

# next7_targets = remove_empty_list(next7_targets)
# targets = append_list(next7_targets)

# def get_route(targets):
#     next_target_indexes = []
#     for idx in targets: # [97, 99, 120, 126, 171, 173, 180, 203, 209, 221],
#         previous_index = idx
#         target_indexes = []
#         index_weight = []
#         for index, weight in enumerate(movie_similarity_list[idx]):
#             if index == previous_index:
#                 weight = 0
#                 index_weight.append([index, weight])
#             elif index in passed_index:
#                 # TODO: 既存の配列に追加する処理の関数を記述
#                 weight = 0
#                 index_weight.append([index, weight])
#             elif weight < 1.5:
#                 index_weight.append([index, weight])
#                 if index not in targets:
#                     target_indexes.append(index)
#         next_target_indexes.append(target_indexes)
#         index_weight_list.append(index_weight)
#         passed_index.append(idx)

#     print("passed_index:", passed_index)
#     print("")
#     print("next_target_indexes", next_target_indexes)
#     print("=============================================")
#     return next_target_indexes

# next_target_indexes = get_route(targets)
# next_target_indexes = remove_empty_list(next_target_indexes)
# targets = append_list(next_target_indexes)

# next_target_indexes = get_route(targets)
# next_target_indexes = remove_empty_list(next_target_indexes)
# print(next_target_indexes)

# if len(next_target_indexes) == 0:
#     print("ture")





