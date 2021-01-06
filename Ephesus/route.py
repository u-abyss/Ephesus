"""
提案アルゴリズムを適応させるための配列を作成するモジュール
"""

from artist import used_arr
from show_network import show_graph

print(used_arr)

# def get_first_index_eles(arrs):
#     first_index_arr = []
#     for arr in arrs:
#         first_index_arr.append(arr[0])
#     return first_index_arr

# first_index_eles = get_first_index_eles(used_arr)

final_used_arr = []

num = 0

for similar_arr in used_arr:
    ARR_LEN = len(used_arr)
    remove_eles = []
    rest_arr = []
    for i in range(num+1, ARR_LEN):
        rest_arr.extend(used_arr[i])
    for idx in range(1, 11):
        ele = similar_arr[idx]
        if ele not in rest_arr:
            remove_eles.append(ele)
    similar_arr = [i for i in similar_arr if i not in remove_eles]
    print(similar_arr)
    final_used_arr.append(similar_arr)
    num += 1
    print("===============")

print(final_used_arr)

show_graph(final_used_arr)



