import numpy as np
import pandas as pd

# from sklearn.metrics.pairwise import pairwise_distance
from datasets import all_reviews_df
from sklearn.metrics import pairwise_distances


def compute_movie_similarity() -> np.ndarray:
    # アイテム同士の類似度を計算するためにデータをitem_id✖️user_idの行列に変換する
    items = all_reviews_df.sort_values('item_id').item_id.unique()
    users = all_reviews_df.user_id.unique()
    shape = (all_reviews_df.max().loc['item_id'],
             all_reviews_df.max().loc['user_id'])
    user_rating_matrix = np.zeros(shape)  # 全ての要素が0で初期化された映画数✖️ユーザ数の行列を定義
    for i in all_reviews_df.index:
        row = all_reviews_df.loc[i]
        user_rating_matrix[row['item_id'] - 1,
                           row['user_id'] - 1] = row['rating']
    # コサイン類似度によるアイテム同士の類似度の配列
    movies_similarities = 1 - \
        pairwise_distances(user_rating_matrix, metric='cosine')
    np.fill_diagonal(movies_similarities, 0)  # 対角線上の要素を0に上書きする
    return movies_similarities


def save_as_binary(f):
    np.save('../data/movie_similarity', f)
