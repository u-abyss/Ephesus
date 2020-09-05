import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
import random

# color_map = ['#C72F7E','#ff4000','#ff4000','#00bfff','#ff4000','#ff4000','#ff4000']
# G = nx.Graph() # 無向グラフ
# nx.add_star(G, [1, 3,5,7,8])
# nx.add_star(G, [2, 8])
# nx.add_star(G, [3, 5,7])
# nx.add_star(G, [4, 3,8])

u_data_org = pd.read_csv(
    './u.data',
    sep='\t',
    names=['user_id','item_id', 'rating', 'timestamp']
)
# encodingをlatin-1に変更しないとエラーになる
movie_description_org = pd.read_csv(
    './u.item.csv',
    sep='|',
    names=[
        'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
        'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
        'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
    ],
    encoding='latin-1'
)

delete_columns = ['movie_id','movie_title','release_date', 'video_release_date', 'imdb_url']
movie_description_org.drop(delete_columns, axis=1, inplace=True)
movie_categories = [
    'unknown', 'action', 'adventure', 'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
    'film_noir', 'horror', 'musical', 'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]
movie_dict = {}
all_categories = []
def categorize_movies(matrix):
    movie_id = 1
    category_number = 0
    for row in matrix.itertuples():
        categories = []
        for i in range(1, 20):
            if row[i] == 1:
                categories.append(i)
        # print(categories)
        if categories not in all_categories:
            all_categories.append(categories)
            category_number = all_categories.index(categories)
            movie_dict.setdefault(movie_id, category_number)
            movie_id += 1
        else:
            category_number = all_categories.index(categories)
            movie_dict.setdefault(movie_id, category_number)
            movie_id += 1

categorize_movies(movie_description_org)

watched_movies = [10, 50, 100, 300, 900, 901, 1000, 1200, 1478, 1500, 1550, 1600, 1681]

#アイテム同士の類似度を計算するために学習データをitem_id✖️user_idの行列に変換する
items = u_data_org.sort_values('item_id').item_id.unique()
users = u_data_org.user_id.unique()
# 各アイテムのユーザごとの評価の配列る
shape = (u_data_org.max().loc['item_id'], u_data_org.max().loc['user_id'])
rating_matrix = np.zeros(shape)
for i in u_data_org.index:
    row = u_data_org.loc[i]
    rating_matrix[row['item_id'] -1 , row['user_id'] - 1] = row['rating']

# userがアイテムを評価したがどうかがわかる{0, 1}の行列を作成
is_rated_matrix = rating_matrix.copy()
is_rated_matrix[is_rated_matrix != 0] = 1

# コサイン類似度によるアイテム同士の類似度の配列
similarity_matrix = 1 - pairwise_distances(rating_matrix, metric='cosine')
np.fill_diagonal(similarity_matrix, 0) # 対角線上の要素を0に上書きする

similar_movie_matrix = []
similar_movies = []
criteria_value = 0.4
for idx, i in enumerate(similarity_matrix):
    similar_movies = []
    for index, review_point in enumerate(i):
        if review_point >= criteria_value:
            similar_movies.append(index+1)
    similar_movies.insert(0, idx+1)
    similar_movie_matrix.append(similar_movies)

# ランダムにカラーコードを生成する
def generate_random_color_code():
    return '#{:X}{:X}{:X}'.format(*[random.randint(10, 255) for _ in range(3)])

# 映画のカテゴリーの種類数分だけのカラーコードを配列にappendする
colors = []
for i in range(216):
    while True:
        color = generate_random_color_code()
        # カラーコードの文字列の長さが6の場合draw_networkxでエラーが起きる. またカラーコードが被った場合もう一度カラーコードを生成する.
        if color not in colors and len(color) == 7:
            colors.append(color)
            break


def get_color(node):
    category_number = movie_dict[node]
    color = colors[category_number]
    return color

color_map = []
G = nx.Graph() # 無向グラフ
for reviews in similar_movie_matrix:
    nx.add_star(G, reviews)
for node in range(1, 1683):
    # 各ノードのカテゴリーに応じてカラーコードを取得する
    color_map.append(get_color(node))
nx.draw_networkx(G, node_color=color_map, node_size= 200, font_size=4, width=0.2, style='dotted')
plt.show()

