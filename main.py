import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
from module.category import categorize_movie, categorize_movies_completely
from module.color import get_color, get_color_by_user_categories
from module.preference import get_user_category_preference
from module.movie import get_movieIds

# ユーザ数943人
# 映画数1682

u_data_org = pd.read_csv(
    './data/u.data',
    sep='\t',
    names=['user_id','item_id', 'rating', 'timestamp']
)
category_names = [
    'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]
# encodingをlatin-1に変更しないとエラーになる
movie_description_org = pd.read_csv(
    './data/u.item.csv',
    sep='|',
    names=category_names,
    encoding='latin-1'
)

delete_columns = ['movie_title','release_date', 'video_release_date', 'imdb_url']
movie_description_org.drop(delete_columns, axis=1, inplace=True)

# 各ユーザが見た評価した映画の本数を出す
user_review_numbers = []
for i in range(1, 944):
    user_reviews_df = u_data_org[u_data_org['user_id'] == i]
    user_review_numbers.append(len(user_reviews_df))
# 各ユーザが何本の映画に評価をつけたかに関するタプル型の配列 [(user_id-1, 見た映画の本数)]
print(sorted(enumerate(user_review_numbers), key=lambda x:x[1], reverse=True))

"""
get_movieIds(userId, u_date_org)
対象のユーザが評価した映画のidの配列を返す関数
"""
user_preference_categories =  get_user_category_preference(movie_description_org, get_movieIds(12, u_data_org))
top5_categories = user_preference_categories[user_preference_categories != 0].index[:5]
top3_categories = user_preference_categories[user_preference_categories != 0].index[:3]
worst_category = user_preference_categories[user_preference_categories != 0].index[-2]

combined_categories = np.append(top3_categories.values, worst_category)
combined_6_category = np.append(top5_categories.values, worst_category)

def get_movie_labels():
    label = 0
    movie_labels = []
    for row in (movie_description_org[combined_6_category]).itertuples():
        # 嫌いなカテゴリーのみの映画
        if row[1] == 0 and row[2] == 0 and row[3] == 0 and row[4] == 0 and row[5] == 0 and row[6] == 1:
            label = 'dislike'
        elif (row[1] == 1 or row[2]== 1 or row[3] == 1 or row[4] == 1 or row[5] == 1) and row[6]== 0:
            label = 'like'
        elif (row[1] == 1 or row[2]== 1 or row[3] == 1 or row[4] == 1 or row[5] == 1) and row[6]== 1:
            label = 'both'
        else:
            label = 'none'
        movie_labels.append(label)
    return movie_labels
# print(get_movie_labels())

# def get_movie_labels():
#     label = 0
#     movie_labels = []
#     for row in (movie_description_org[combined_categories]).itertuples():
#         # 嫌いなカテゴリーのみの映画
#         if row[1] == 0 and row[2] == 0 and row[3] == 0 and row[4] == 1:
#             label = 'dislike'
#             # print(row)
#         elif (row[1] == 1 or row[2]== 1 or row[3] == 1) and row[4]== 0:
#             label = 'like'
#         elif (row[1] == 1 or row[2]== 1 or row[3] == 1) and row[4]== 1:
#             label = 'both'
#         else:
#             label = 'none'
#         movie_labels.append(label)
#     return movie_labels
# print(get_movie_labels())


def get_color_by_label(node, array):
    label = array[node-1]
    if label == 'dislike':
        return 'blue'
    elif label == 'like':
        return 'red'
    elif label == 'both':
        return 'yellow'
    else:
        return 'white'
"""
categorize_movie()
各映画を一つのカテゴリーで分ける
複数のカテゴリーがあるものに一番先頭にあるカテゴリーをその映画のカテゴリーとして定義する
{movieID: 'category'}
"""
movie_category_dict = {}
movie_category_dict = categorize_movie(movie_description_org)

#アイテム同士の類似度を計算するために学習データをitem_id✖️user_idの行列に変換する
items = u_data_org.sort_values('item_id').item_id.unique()
users = u_data_org.user_id.unique()
shape = (u_data_org.max().loc['item_id'], u_data_org.max().loc['user_id'])
# 全ての要素が0で初期化された映画数✖️ユーザ数の行列を定義
user_rating_matrix = np.zeros(shape)
for i in u_data_org.index:
    row = u_data_org.loc[i]
    user_rating_matrix[row['item_id'] -1 , row['user_id'] - 1] = row['rating']

# コサイン類似度によるアイテム同士の類似度の配列
similarity_matrix = 1-pairwise_distances(user_rating_matrix, metric='cosine')
np.fill_diagonal(similarity_matrix, 0) # 対角線上の要素を0に上書きする

# def get_mean(matrix):
#     totals = []
#     for i in matrix:
#         for j in i:
#             if j != 0:
#                 totals.append(j)
#     total_sum = sum(totals)
#     mean = total_sum / 1413721
#     return mean
# reshape_similarity_matrix = similarity_matrix.flatten()

# 各ノードから派生するノード数の配列
similar_movie_two_dimension = [] # 各ノードが持つノードを列挙した二次元配列
similarity_criterion = 0.4
for idx, i in enumerate(similarity_matrix):
    similar_movies = []
    for index, review_point in enumerate(i):
        if review_point >= similarity_criterion:
            similar_movies.append(index+1)
    similar_movies.insert(0, idx+1)
    similar_movie_two_dimension.append(similar_movies)

# 各ノードが何本の映画とつながっているかを求める [(item_id, つながっているノードの数)]
similar_movie_two_dimension_lengths = []
for row in similar_movie_two_dimension:
    similar_movie_two_dimension_lengths.append(len(row))
# print(sorted(enumerate(similar_movie_two_dimension_lengths), key=lambda x:x[1], reverse=True))

# delete nodes that dot't have any edges
def get_unused_nodes():
    delete_nodes = []
    for i in range(len(similar_movie_two_dimension)):
        if len(similar_movie_two_dimension[i]) == 1:
            delete_nodes.append(i+1)
    return delete_nodes

def show_graph():
    color_map = []
    G = nx.Graph()
    for reviews in similar_movie_two_dimension:
        nx.add_star(G, reviews)
    for node in range(1, 1683):
        # 各ノードのカテゴリーに応じてカラーコードを取得する
        # color_map.append(get_color(node, movie_category_dict))
        color_map.append(get_color_by_label(node, get_movie_labels()))
        # color_map.append(get_color_by_user_categories(node, movie_category_dict, top5_categories, worst_category))
    unused_nodes = get_unused_nodes()
    for i in unused_nodes:
        G.remove_node(i)
    for i in sorted(unused_nodes, reverse=True): # reverse=True to prevent offset of index
        color_map.pop(i)
    nx.draw_networkx(G, node_color=color_map, node_size= 200, font_size=4, width=0.2, style='dotted')
    plt.show()

show_graph()