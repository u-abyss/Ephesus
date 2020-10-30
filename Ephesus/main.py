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

"""
各映画同士のコサイン類似度を求める関数.
映画数✖️映画数の行列を返す.
1行は映画
ベクトルの中身はその映画と,　他の全ての映画とのコサイン類似度の値.
"""

movie_similarity = np.load('../data/movie_similarity.npy')


"""
TODO
    - タプルのリストを作成する（始点,　終点,　重み）
    - 重みをsimilarityの逆数とする
    - 重みつきのネットワーク図を作成
"""
# weighted_egde_list = []
# movies_similarities = compute_movie_similarity(all_reviews_df)
# for index, row in enumerate(movies_similarities):
#     tuple_list = []
#     for _index, similarity in enumerate(row):
#         if _index >= index + 1:
#             if similarity >= 0.7:
#                 weighted_egde_tuple = (index+1, _index+1, similarity)
#                 tuple_list.append(weighted_egde_tuple)
#     weighted_egde_list.append(tuple_list)

# # print(weighted_egde_list)
# G = nx.Graph()
# for tuple_list in weighted_egde_list:
#     G.add_weighted_edges_from(tuple_list)
# print(nx.dijkstra_path(G, 28, 226, weight='weight'))
# print(G[28][423]['weight'])
# nx.draw_networkx(G, node_size=200,
#                  font_size=4, width=0.2, style='dotted')
# plt.show()


get_all_user_review_numbers(all_reviews_df)

# 各ノードから派生するノード数の配列
"""
各ノードが他のどのノードとつながっているかを調べる関数
ノード　: 映画
枝     : 映画と映画の間に関連性がある場合,　枝が張られる.
"""


def get_each_possess_nodes():
    possessNodes = []  # 各ノードが持つノードを列挙した二次元配列
    similarity_criterion = 0.65
    for idx, i in enumerate(movie_similarity):
        similar_movies = []
        for index, similarity_value in enumerate(i):
            if similarity_value >= similarity_criterion:
                similar_movies.append(index+1)  # movie_idをappendしていく
        similar_movies.insert(0, idx+1)  # 各配列の先頭に対象の映画のmovie_idを挿入する.
        possessNodes.append(similar_movies)
    return possessNodes


possess_nodes = get_each_possess_nodes()

"""
各映画が何本の映画とつながっているかを求める関数 [(movie_id, つながっているノードの数)]
"""


def get_each_possess_nodes_number():
    possessNodesLengths = []
    for row in possess_nodes:
        possessNodesLengths.append(len(row))
    return sorted(enumerate(possessNodesLengths), key=lambda x: x[1], reverse=True)


"""
重要度の低い映画を削除する関数.
つながりのある映画がない映画を重要度の低い映画とする.
"""


def get_unused_nodes():
    unused_nodes = []
    MAX_MOVIE_ID = 1682
    for i in range(1, MAX_MOVIE_ID):
        if len(possess_nodes[i-1]) == 1:
            unused_nodes.append(i)
    return unused_nodes


def show_graph():
    color_map = []
    G = nx.Graph()
    categorized_movies = get_categorized_movies_by_user_preference(
        movie_description_df, top5_categories, all_reviews_df, 884)
    categorized_movies_by_selected_category = get_categorized_movies_by_selected_category(
        'documentary', all_reviews_df, movie_description_df, 884)
    for node in possess_nodes:
        nx.add_star(G, node)
    MAX_MOVIE_ID = 1683
    for node in range(1, MAX_MOVIE_ID):
        """
        見たことあるないで分ける+指定したカテゴリを含む映画で色分け
        """
        label = categorized_movies[node-1]
        if label == 'watch_fave' or label == 'watch_not_fave':
            color_map.append(get_color_by_user_reference(
                node, categorized_movies))
        else:
            label = categorized_movies_by_selected_category[node-1]
            color_map.append(get_color_by_selected_category(label))

    unused_nodes = get_unused_nodes()
    for i in unused_nodes:
        G.remove_node(i)
    for i in sorted(unused_nodes, reverse=True):  # reverse=True to prevent offset of index
        color_map.pop(i)
    nx.draw_networkx(G, node_color=color_map, node_size=200,
                     font_size=4, width=0.2, style='dotted')
    plt.show()


show_graph()
