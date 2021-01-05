import numpy as np
from txt2df import similarity_df, artist_data_df

def get_similar_artists_arr():
    similar_artists_arr = []
    for row in similarity_df.itertuples(name=None):
        artists = []
        # 類似するアーティスト上位10名のリスト
        similar_artists = row[2].split()
        # リストの先頭に対象となるアーティストのidを追加
        similar_artists.insert(0, row[1])
        similar_artists_arr.append(similar_artists)
    return similar_artists_arr

# similar_artists_arr = get_similar_artists_arr()

# print(similar_artists_arr)

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)
print(artist_categories)

# def get_node_fave_categories_num(artist_categories, user_fave_categories):


