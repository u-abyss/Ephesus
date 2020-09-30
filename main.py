import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
from module.category import categorize_movies, categorize_movies_completely
from module.color import get_color, get_color_by_user_categories
from module.favorite import get_user_favorite_categories

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

user_review_numbers = []
max_review_number = 0
max_review_number_user = 0

# 各ユーザが見た映画の本数を出す
for i in range(1, 944):
    user_review_number = u_data_org[u_data_org['user_id'] == i]
    if len(user_review_number) > max_review_number:
        max_review_number = len(user_review_number)
        max_review_number_user = i
    user_review_numbers.append(len(user_review_number))
# 各ユーザが何本の映画に評価をつけたかに関するタプル型の配列 [(user_id-1, 見た映画の本数)]
print(sorted(enumerate(user_review_numbers), key=lambda x:x[1], reverse=True))

# 対象とするユーザが見た映画のidを配列に追加
def get_movieIds(userId):
    target_user_reviews = u_data_org[u_data_org['user_id'] == userId]
    user_watched_movies = []
    for i in target_user_reviews.item_id:
        user_watched_movies.append(i)
    return target_user_reviews
    # print(type((movie_description_org[movie_description_org['movie_id'].isin(user_watched_movies)]).sum()['action']))
get_movieIds(654)

user_favorite_categories = get_user_favorite_categories(movie_description_org, get_movieIds(404))
top5_categories = user_favorite_categories[user_favorite_categories != 0].index[:5]
top3_categories = user_favorite_categories[user_favorite_categories != 0].index[:3]
worst_category = user_favorite_categories[user_favorite_categories != 0].index[-2]

combined_categories = np.append(top3_categories.values, worst_category)
print(combined_categories)
print(movie_description_org[combined_categories])

combined_6_category = np.append(top5_categories.values, worst_category)

def get_movie_labels():
    label = 0
    movie_labels = []
    for row in (movie_description_org[combined_6_category]).itertuples():
        # 嫌いなカテゴリーのみの映画
        if row[0] == 0 and row[1] == 0 and row[2] == 0 and row[3] == 0 and row[4] == 0 and row[5] == 1:
            label = 0
        elif (row[0] == 1 or row[1]== 1 or row[2] == 1 or row[3] == 0 or row[4] == 0) and row[5]== 0:
            label = 2
        elif (row[0] == 1 or row[1]== 1 or row[2] == 1 or row[3] == 0 or row[4] == 0) and row[5]== 1:
            label = 100
        else:
            label = 000
        movie_labels.append(label)
    return movie_labels
print(get_movie_labels())

# def get_movie_labels():
#     label = 0
#     movie_labels = []
#     for row in (movie_description_org[combined_categories]).itertuples():
#         # 嫌いなカテゴリーのみの映画
#         if row[0] == 0 and row[1] == 0 and row[2] == 0 and row[3] == 1:
#             label = 0
#         elif (row[0] == 1 or row[1]== 1 or row[2] == 1) and row[3]== 0:
#             label = 2
#         elif (row[0] == 1 or row[1]== 1 or row[2] == 1) and row[3]== 1:
#             label = 100
#         else:
#             label = 000
#         movie_labels.append(label)
#     return movie_labels
# print(get_movie_labels())

def get_color_by_label(node, array):
    label = array[node-1]
    if label == 0:
        return 'grey'
    elif label == 2:
        return 'red'
    elif label == 100:
        return 'yellow'
    else:
        return 'white'

movie_dict = {}
all_categories = []

movie_dict = categorize_movies(movie_description_org)

#アイテム同士の類似度を計算するために学習データをitem_id✖️user_idの行列に変換する
items = u_data_org.sort_values('item_id').item_id.unique()
users = u_data_org.user_id.unique()
# 各アイテムのユーザごとの評価の配列
shape = (u_data_org.max().loc['item_id'], u_data_org.max().loc['user_id'])
rating_matrix = np.zeros(shape)
for i in u_data_org.index:
    row = u_data_org.loc[i]
    rating_matrix[row['item_id'] -1 , row['user_id'] - 1] = row['rating']

# コサイン類似度によるアイテム同士の類似度の配列
similarity_matrix = 1 - pairwise_distances(rating_matrix, metric='cosine')
np.fill_diagonal(similarity_matrix, 0) # 対角線上の要素を0に上書きする

# 各ノードから派生するノードの配列
similar_movie_two_dimension = [] # 各ノードが持つノードを列挙した二次元配列
similar_movies = []
criteria_value = 0.4
for idx, i in enumerate(similarity_matrix):
    similar_movies = []
    for index, review_point in enumerate(i):
        if review_point >= criteria_value:
            similar_movies.append(index+1)
    similar_movies.insert(0, idx+1)
    similar_movie_two_dimension.append(similar_movies)

# 各ノードが何本の映画とつながっているかを求める [(item_id, つながっているノードの数)]
similar_movie_two_dimension_lengths = []
for row in similar_movie_two_dimension:
    similar_movie_two_dimension_lengths.append(len(row))
# print(sorted(enumerate(similar_movie_two_dimension_lengths), key=lambda x:x[1], reverse=True))

# delete nodes that dot't have edge
delete_nodes = []
for i in range(len(similar_movie_two_dimension)):
    if len(similar_movie_two_dimension[i]) == 1:
        delete_nodes.append(i+1)

def show_graph():
    color_map = []
    G = nx.Graph() # 無向グラフ
    for reviews in similar_movie_two_dimension:
        nx.add_star(G, reviews)
    for node in range(1, 1683):
        # 各ノードのカテゴリーに応じてカラーコードを取得する
        # color_map.append(get_color(node, movie_dict))
        color_map.append(get_color_by_label(node, get_movie_labels()))
        # color_map.append(get_color_by_user_categories(node, movie_dict, top5_categories, worst_category))
    # for i in user_watched_movies:
    #     color_map[i] = 'red'
    for i in delete_nodes:
        G.remove_node(i)

    # reverse=True to prevent offset of index
    for i in sorted(delete_nodes, reverse=True):
        color_map.pop(i)
    nx.draw_networkx(G, node_color=color_map, node_size= 200, font_size=4, width=0.2, style='dotted')
    plt.show()

show_graph()