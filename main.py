import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import random
import statistics
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm
from module.category import categorize_movie, categorize_movies_completely, get_categorized_movies_by_user_preference, get_user_review_movieIds, get_categorized_movies_by_selected_category
from module.preference import get_user_category_preference
from module.color import get_color_by_user_reference, get_color, get_color_by_selected_category
from utils.showhistgram import show_histgram

# ユーザ数943人
# 映画数1682

all_reviews_df = pd.read_csv(
    './data/u.data',
    sep='\t',
    names=['user_id','item_id', 'rating', 'timestamp']
)
category_names = [
    'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]

movie_categories = ['unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western']
# encodingをlatin-1に変更しないとエラーになる
movie_description_df = pd.read_csv(
    './data/u.item.csv',
    sep='|',
    names=category_names,
    encoding='latin-1'
)

delete_columns = ['movie_title','release_date', 'video_release_date', 'imdb_url']
movie_description_df.drop(delete_columns, axis=1, inplace=True)

"""
各ユーザのレビュー数のヒストグラムを表示する
"""
# show_histgram(get_user_review_movieIds(), bin=40)

top5_categories = get_user_category_preference(movie_description_df, all_reviews_df, 5, 247)
print(top5_categories)
# worst_category = get_user_category_preference(movie_description_df, all_reviews_df, -1, 247)

"""
各映画同士のコサイン類似度を求める関数.
映画数✖️映画数の行列を返す.
1行は映画
ベクトルの中身はその映画と,　他の全ての映画とのコサイン類似度の値.
"""
def computeMovieSimilarity(all_reviews_df):
    items = all_reviews_df.sort_values('item_id').item_id.unique()#アイテム同士の類似度を計算するために学習データをitem_id✖️user_idの行列に変換する
    users = all_reviews_df.user_id.unique()
    shape = (all_reviews_df.max().loc['item_id'], all_reviews_df.max().loc['user_id'])
    user_rating_matrix = np.zeros(shape) # 全ての要素が0で初期化された映画数✖️ユーザ数の行列を定義
    for i in all_reviews_df.index:
        row = all_reviews_df.loc[i]
        user_rating_matrix[row['item_id'] -1 , row['user_id'] - 1] = row['rating']
    movies_similarities = 1 - pairwise_distances(user_rating_matrix, metric='cosine') # コサイン類似度によるアイテム同士の類似度の配列
    np.fill_diagonal(movies_similarities, 0) # 対角線上の要素を0に上書きする
    return movies_similarities

movies_similarities = computeMovieSimilarity(all_reviews_df)

# movie_category_dict = categorize_movie(movie_description_df)
"""
各映画のその他の映画とのコサイン類似度のヒストグラムを表示
"""
# total_row = []
# for row in similarity_matrix:
#     total_row.extend(row)
# show_histgram(total_row, 50)

# 各ノードから派生するノード数の配列
"""
各ノードが他のどのノードとつながっているかを調べる関数
ノード : 映画
枝 : 映画と映画の間に関連性がある場合,　枝が張られる.
"""
similar_movie_two_dimension = [] # 各ノードが持つノードを列挙した二次元配列
similarity_criterion = 0.4
for idx, i in enumerate(movies_similarities):
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
    unused_nodes = []
    for i in range(len(similar_movie_two_dimension)):
        if len(similar_movie_two_dimension[i]) == 1:
            unused_nodes.append(i+1)
    return unused_nodes

def show_graph():
    color_map = []
    G = nx.Graph()
    categorized_movies = get_categorized_movies_by_user_preference(movie_description_df, top5_categories, all_reviews_df)
    categorized_movies_by_selected_category = get_categorized_movies_by_selected_category('adventure', all_reviews_df, movie_description_df)
    print(len(categorized_movies_by_selected_category))
    for reviews in similar_movie_two_dimension:
        nx.add_star(G, reviews)
    for node in range(1, 1683):
        # 各ノードのカテゴリーに応じてカラーコードを取得する
        # color_map.append(get_color(node, movie_category_dict))
        label = categorized_movies[node-1]
        if label == 'watch_fave' or label == 'watch_not_fave':
            color_map.append(get_color_by_user_reference(node, categorized_movies))
        else:
            label = categorized_movies_by_selected_category[node-1]
            color_map.append(get_color_by_selected_category(label))
    unused_nodes = get_unused_nodes()
    for i in unused_nodes:
        G.remove_node(i)
    for i in sorted(unused_nodes, reverse=True): # reverse=True to prevent offset of index
        color_map.pop(i)
    nx.draw_networkx(G, node_color=color_map, node_size= 200, font_size=4, width=0.2, style='dotted')
    plt.show()

show_graph()