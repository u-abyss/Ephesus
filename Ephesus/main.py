import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
import statistics
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
from category import get_categorized_movies_by_user_preference, get_user_review_movieIds, get_categorized_movies_by_selected_category, get_all_user_review_numbers
from preference import get_user_category_preference
from color import get_color_by_user_reference, get_color_by_selected_category
from datasets import all_reviews_df, movie_description_df
from similarity import compute_movie_similarity

"""
指定したユーザのお気にりのカテゴリトップN件を取得する関数
取得するお気に入りのカテゴリの件数とユーザのuser_idを入力する
"""

top5_categories = get_user_category_preference(
    movie_description_df, all_reviews_df, 5, 884)
print(top5_categories)

movie_similarity = np.load('../data/movie_similarity.npy')

get_all_user_review_numbers(all_reviews_df)

"""
連結リストを求める関数
連結リスト : どのノードがどのノードと連結しているかを表すデータ構造
返り値 : 連結リスト

ex
[[1, 3, 6, 7], [5, 6, 7, 10] ... [1682, 1682]]
各配列のindex:0のmovie_idの映画と連結しているmovie_idをそれ以降に格納.
連結している映画がない時は,　そのmovie_idが２つ並ぶ.
"""

def get_linked_list():
    linkded_list = []  # 各ノードが持つノードを列挙した二次元配列
    similarity_criterion = 1 / 0.65
    for idx, i in enumerate(movie_similarity):
        similar_movies = []
        for index, similarity_value in enumerate(i):
            if similarity_value <= similarity_criterion:
                similar_movies.append(index+1)  # movie_idをappendしていく
        similar_movies.insert(0, idx+1)  # 各配列の先頭に対象の映画のmovie_idを挿入する.
        linkded_list.append(similar_movies)
    return linkded_list


linkded_list = get_linked_list()

"""
次数(頂点ごとの辺の数)を求める関数
"""
def get_degree_valency():
    degree_valencies = []
    for row in linkded_list:
        degree_valencies.append(len(row))
    return sorted(enumerate(degree_valencies), key=lambda x: x[1], reverse=True)

"""
対象ユーザの視聴状況とお気に入りのカテゴリに応じて,　ノードにラベルをつける関数
"""
def get_node_color(categorized_movies, categorized_movies_by_selected_category):
    color_map = []
    MAX_MOVIE_ID = 1683
    for node in range(1, MAX_MOVIE_ID):
        label = categorized_movies[node - 1]
        if label == 'watch_fave' or label == 'watch_not_fave':
            color_map.append(get_color_by_user_reference(node, categorized_movies))
        else:
            label = categorized_movies_by_selected_category[node-1]
            color_map.append(get_color_by_selected_category(label))
    return color_map


"""
重要度の低い映画を削除する関数.
つながりのある映画がない映画を重要度の低い映画とする.
"""
def get_unused_nodes():
    unused_nodes = []
    MAX_MOVIE_ID = 1682
    for i in range(1, MAX_MOVIE_ID):
        if len(possess_nodes[i-1]) == 2:
            unused_nodes.append(i)
    return unused_nodes

def show_graph():
    G = nx.Graph()
    categorized_movies = get_categorized_movies_by_user_preference(movie_description_df, top5_categories, all_reviews_df, 884)
    categorized_movies_by_selected_category = get_categorized_movies_by_selected_category('documentary', all_reviews_df, movie_description_df, 884)
    for node in possess_nodes:
        nx.add_star(G, node)
    color_map = get_node_color(categorized_movies, categorized_movies_by_selected_category)
    unused_nodes = get_unused_nodes()
    for i in unused_nodes:
        G.remove_node(i)
    for i in sorted(unused_nodes, reverse=True):  # reverse=True to prevent offset of index
        color_map.pop(i)
    nx.draw_networkx(G, node_color=color_map, node_size=200, font_size=4, width=0.2, style='dotted')
    plt.show()

"""
重り付きのネットワーク図を描画するための配列を求める関数

返り値 : ノード間の重さについてのタプル型の要素を格納した配列を格納した二次元配列
        ネットワーク図を描画するに当たって,　用いるmovie_idの配列
"""

def get_edge_weight():
    weighted_edge_list = [] # 2次元配列
    used_node_indexes = []
    for index_y, row in enumerate(movie_similarity):
        weight_tuple_list = []
        for index_x, similarity in enumerate(row):
            if index_x >= index_y + 1: # 各行に対して,　全ての列要素について調べると被りが出てしまうため,　各行において比較対象となる列の要素は,　その行数以上の列とする
                if similarity <= 1 / 0.7:
                    weighted_egde_tuple = (index_y+1, index_x+1, similarity) # (node, node, weight)
                    weight_tuple_list.append(weighted_egde_tuple)
                    used_node_indexes.append(index_y)
                    used_node_indexes.append(index_x)
        if weight_tuple_list != []:
            weighted_edge_list.append(weight_tuple_list)
    unique_used_node_indexes = list(set(used_node_indexes))
    orderd_unique_used_node_indexes = sorted(unique_used_node_indexes)
    return weighted_edge_list, orderd_unique_used_node_indexes

def nx_dijkstra():
    START_NODE_NUMBER = 226
    GOAL_NODE_NUMBER = 405
    categorized_movies = get_categorized_movies_by_user_preference(movie_description_df, top5_categories, all_reviews_df, 884)
    categorized_movies_by_selected_category = get_categorized_movies_by_selected_category('documentary', all_reviews_df, movie_description_df, 884)
    weighted_egde_list, orderd_unique_used_node_indexes = get_edge_weight()

    color_map = get_node_color(categorized_movies, categorized_movies_by_selected_category)

    G = nx.Graph()
    for tuple_list in weighted_egde_list:
        G.add_weighted_edges_from(tuple_list)
    print(nx.dijkstra_path(G, START_NODE_NUMBER, GOAL_NODE_NUMBER, weight='weight'))
    # print(G[784][438]['weight'])

    new_color_map = []
    for idx in orderd_unique_used_node_indexes:
        label = color_map[idx]
        new_color_map.append(label)

    nx.draw_networkx(G, node_color=new_color_map, node_size=200, font_size=4, width=0.2, style='dotted')
    plt.show()

nx_dijkstra()