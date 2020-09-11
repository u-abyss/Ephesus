import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
import random

# ユーザ数943人
# 映画数1682

u_data_org = pd.read_csv(
    './data/u.data',
    sep='\t',
    names=['user_id','item_id', 'rating', 'timestamp']
)

# encodingをlatin-1に変更しないとエラーになる
movie_description_org = pd.read_csv(
    './data/u.item.csv',
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
target_user_reviews = u_data_org[u_data_org['user_id'] == 727]
user_watched_movies = []
for i in target_user_reviews.item_id:
    user_watched_movies.append(i)
# print(user_watched_movies)


movie_dict = {}
all_categories = []

def categorize_movies_completely(matrix):
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

def categorize_movies(matrix):
    movie_id = 1
    for row in matrix.itertuples():
        for i in range(1, 20):
            if row[i] == 1:
                movie_dict.setdefault(movie_id, movie_categories[i-1])
                movie_id += 1
                break
            else:
                continue
categorize_movies(movie_description_org)

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
print(sorted(enumerate(similar_movie_two_dimension_lengths), key=lambda x:x[1], reverse=True))

# ランダムにカラーコードを生成する
def generate_random_color_code():
    return '#{:X}{:X}{:X}'.format(*[random.randint(10, 255) for _ in range(3)])

# 映画のカテゴリーの種類数分だけのカラーコードを配列にappendする
colors = []
def get_colors():
    for i in range(216):
        while True:
            color = generate_random_color_code()
            # カラーコードの文字列の長さが6の場合draw_networkxでエラーが起きる. またカラーコードが被った場合もう一度カラーコードを生成する.
            if color not in colors and len(color) == 7:
                colors.append(color)
                break

def get_random_color(node):
    category_number = movie_dict[node]
    color = colors[category_number]
    return color

# 映画のジャンルに応じて,　ノードに色付けをする
def get_color(node):
    category = movie_dict[node]
    if category == 'unknown':
        return 'grey'
    elif category == 'action':
        return 'mediumvioletred'
    elif category == 'adventure':
        return 'green'
    elif category == 'animation':
        return 'yellow'
    elif category == 'children':
        return 'orange'
    elif category == 'comedy':
        return 'gold'
    elif category == 'crime':
        return 'purple'
    elif category == 'documentary':
        return 'brown'
    elif category == 'drama':
        return 'lightyellow'
    elif category == 'fantasy':
        return 'pink'
    elif category == 'film_noir':
        return 'aqua'
    elif category == 'horror':
        return 'black'
    elif category == 'musical':
        return 'tomato'
    elif category == 'mystery':
        return 'navy'
    elif category == 'romance':
        return 'magenta'
    elif category == 'sci_fi':
        return 'darkgreen'
    elif category == 'thriller':
        return 'darkslategray'
    elif category == 'war':
        return 'darkred'
    else:
        return 'chocolate'

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
        color_map.append(get_color(node))
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