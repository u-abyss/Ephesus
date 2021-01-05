import numpy as np
from txt2df import similarity_df, artist_data_df
from music_category import good_playlist_artists

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

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

"""
アーティスト名からアーティストidを取得する関数
"""
def get_artist_id_from_name(playlist):
    artist_ids = []
    for artist_name in playlist:
        row = artist_data_df.query("artist_name == @artist_name")
        artist_id = (row.artist_id).to_string()
        replaced_id = artist_id.replace("    ", '=')
        splited_id = replaced_id.split('=')[1]
        artist_ids.append(splited_id)
    return artist_ids

similar_artists_arr = get_similar_artists_arr()

artist_ids = get_artist_id_from_name(good_playlist_artists[3])
print(artist_ids)

for row in good_playlist_artists[3]:
    print(row)

"""
プレイリストの曲のアーティストidから，グラフ構築に使用する配列を取得する関数
"""
def get_used_similar_artists_arr(artist_ids):
    used_arr = []
    for id in artist_ids:
        for arr in similar_artists_arr:
            if id == arr[0]:
                used_arr.append(arr)
    return used_arr

used_arr = get_used_similar_artists_arr(artist_ids)


# def get_node_fave_categories_num(artist_categories, user_fave_categories):




