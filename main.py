import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.metrics.pairwise import pairwise_distances
from tqdm import tqdm

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
#アイテム同士の類似度を計算するために学習データをitem_id✖️user_idの行列に変換する
items = u_data_org.sort_values('item_id').item_id.unique()
users = u_data_org.user_id.unique()
# 各アイテムのユーザごとの評価の配列る
shape = (u_data_org.max().loc['user_id'], u_data_org.max().loc['item_id'])
rating_matrix = np.zeros(shape)
for i in u_data_org.index:
    row = u_data_org.loc[i]
    rating_matrix[row['user_id'] -1 , row['item_id'] - 1] = row['rating']

# userがアイテムを評価したがどうかがわかる{0, 1}の行列を作成
is_rated_matrix = rating_matrix.copy()
is_rated_matrix[is_rated_matrix != 0] = 1

# コサイン類似度によるアイテム同士の類似度の配列
similarity_matrix = 1 - pairwise_distances(rating_matrix, metric='cosine')
np.fill_diagonal(similarity_matrix, 0) # 対角線上の要素を0に上書きする

criteria_value = 0.4

rows = []
for i in similarity_matrix:
    delete_indexes = []
    rows.append(i)

for row in rows:
    row = row[~(row < criteria_value)]
    print(row)


    for j in range(len(i)):
        review = i[j]
        if review < criteria_value:
            delete_indexes.append(j)
    np.delete(i, delete_indexes, axis=None)
print(similarity_matrix)

# G = nx.DiGraph() # 有向グラフ

# # nx.add_path(G, [3, 5, 4, 1, 0, 2, 7, 8, 9, 6])
# # nx.add_path(G, [3, 0, 6, 4, 2, 7, 1, 9, 8, 5])
# nx.add_star(G, [1,2,3,4,5])
# nx.add_star(G, [2,3,4, 5])
# nx.draw_networkx(G)
# plt.show()