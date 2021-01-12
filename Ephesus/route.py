"""
提案アルゴリズムを適応させるための配列を作成するモジュール
"""
import numpy as np

movie_similarity = np.load("../data/movie_similarity.npy")
movie_similarity_list = movie_similarity.tolist()
# print(len(movie_similarity))

row1 = movie_similarity[0]
row2 = movie_similarity[1]

weight_criteria = 1.5
# 推薦のスタートとなる映画のインデックスを引数とする

next_targets = []
for index, weight in enumerate(movie_similarity_list[0]):
    if weight < 1.5:
        next_targets.append(index)

print("next_target", next_targets)

next2_targets = []
for idx in next_targets:
    if idx == 0:
        continue
    print(idx)
    next_targets = []
    for index, weight in enumerate(movie_similarity_list[idx]):
        if weight < 1.5:
            next_targets.append(index)
    next2_targets.append(next_targets)


print("next2_targets", next2_targets)

next3_targets = []
for row in next2_targets:
    next_targets = []
    for idx, weight in enumerate(movie_similarity_list[idx]):
        if weight < 1.5:
            next_targets.append(idx)
    next3_targets.append(next_targets)

print("next3_targets", next3_targets)

next4_targets = []
for row in next3_targets:
    next_targets = []
    for idx, weight in enumerate(movie_similarity_list[idx]):
        if weight < 1.5:
            next_targets.append(idx)
    next4_targets.append(next_targets)

print("next4_targets", next4_targets)

# print(row1)
# print(row2)

# new_similarity_list = []
# for row in movie_similarity_list:
#     weights = []
#     for weight in row:
#         if weight < 1.5:
#             weights.append(weight)
#             print("inf")
#     new_similarity_list.append(weights)

# print(new_similarity_list)


# def get_first_index_eles(arrs):
#     first_index_arr = []
#     for arr in arrs:
#         first_index_arr.append(arr[0])
#     return first_index_arr

# first_index_eles = get_first_index_eles(used_arr)

# final_used_arr = []

# num = 0

# for similar_arr in used_arr:
#     ARR_LEN = len(used_arr)
#     remove_eles = []
#     rest_arr = []
#     for i in range(num+1, ARR_LEN):
#         rest_arr.extend(used_arr[i])
#     for idx in range(1, 11):
#         ele = similar_arr[idx]
#         if ele not in rest_arr:
#             remove_eles.append(ele)
#     similar_arr = [i for i in similar_arr if i not in remove_eles]
#     print(similar_arr)
#     final_used_arr.append(similar_arr)
#     num += 1
#     print("===============")

# print(final_used_arr)

# show_graph(final_used_arr)



