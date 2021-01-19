"""
提案アルゴリズムを適応させるための配列を作成するモジュール
"""
import math
import numpy as np
from typing import List, Dict

# 推薦のスタートとなる音声のインデックスを引数とする
MAX_SIMILARITY = 1.8
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
# print(audio_similarty_list[0])

def append_list(prev_list):
    new_list = []
    for row in prev_list:
        for idx in row:
            new_list.append(idx)
    return new_list

def remove_empty_list(prev_list):
    new_list = [x for x in prev_list if x != []]
    return new_list

# passed_index = [START_INDEX]

def get_first_next_target_indexes(start_index, passed_index):
    next_target_index = []
    index_weight_list = []
    index_weight = [0]
    for index, weight in enumerate(audio_similarty_list[start_index]):
        if index == start_index:
            continue
        elif MIN_SIMILARITY < weight < MAX_SIMILARITY:
            index_weight.append(weight)
            next_target_index.append(index)
    index_weight_list.append(index_weight)
    return next_target_index, index_weight_list, passed_index

def get_route(targets, index_weight_list, passed_index):
    index_weight_list = index_weight_list
    next_target_indexes = []
    first_search_indexes = []
    num = 1
    for idx in targets:
        if num > 20:
            return index_weight_list, passed_index
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
        return index_weight_list, passed_index
    else:
        return get_route(next_target_indexes, index_weight_list, passed_index)

def add_or_remove_eles_in_list(weight_list, passed_index):
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

def create_dijkstra_list(start_index):
    passed_index = [start_index]
    next_target_index, index_weight_list, passed_index = get_first_next_target_indexes(start_index, passed_index)
    index_weight_list, passed_index = get_route(next_target_index, index_weight_list, passed_index)
    # 提案アルゴリズムに適応可能な配列（index_weight_list）
    index_weight_list = add_or_remove_eles_in_list(index_weight_list, passed_index)
    return index_weight_list, passed_index

# index_weight_list = create_dijkstra_list(START_INDEX)