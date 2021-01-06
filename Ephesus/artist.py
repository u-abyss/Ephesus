import collections
import numpy as np
from txt2df import similarity_df, artist_data_df
from show_network import show_graph
from npy2arr import good_playlists_artists, good_playlists

# from music_category import good_playlist_artists

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

all_connected_playlists_idxs = [
    3,
    5,
    7,
    22,
    34,
    37,
    38,
    40,
    55,
    63,
    64,
    68,
    69,
    70,
    71,
    72,
    82,
    85,
    86,
    88,
    94,
    95,
    101,
    127,
    132,
    133,
    139,
    143,
    146,
    155,
    160,
    161,
    168,
    178,
    181,
    184,
    190,
    193,
    199,
    200,
    212,
    213,
    218,
    225,
    226,
    229,
    236,
    240,
    249,
    255,
    264,
    272,
    278,
    279,
    281,
    284,
    290,
    293,
    301,
    304,
    313,
    315,
    318,
    319,
    320,
    322,
    328,
    336,
    338,
    343,
    348,
    365,
    367,
    370,
    372,
    373,
    374,
    377,
    380,
    384,
    386
]

# for i in all_connected_playlists_idxs:
#     artist_ids = get_artist_id_from_name(good_playlist_artists[i])
#     used_arr = get_used_similar_artists_arr(artist_ids)
#     show_graph(used_arr)

def get_categories(playlist):
    all_categories = []
    for category in playlist:
        all_categories.extend(category)
    c = collections.Counter(all_categories)
    print(c)

for i in all_connected_playlists_idxs:
    if len(good_playlists[i]) > 5:
        print(i)
        print(good_playlists[i])
        print(len(good_playlists[i]))
        print(get_categories(good_playlists[i]))
        print("================================")

def get_unique_categories():
    all_categories = []
    for i in all_connected_playlists_idxs:
        for categories in good_playlists[i]:
            all_categories.extend(categories)
    unique_categories = list(set(all_categories))
    final_arr = []
    for category in unique_categories:
        replaced_category = category.replace("_", ' ')
        final_arr.append(replaced_category)
    print(len(final_arr))
    print(len(unique_categories))
    return final_arr

# unique_categories = get_unique_categories()
# print(unique_categories)

# お気に入りのカテゴリ上位k件
def get_category_count():
    for i in all_connected_playlists_idxs:
        all_categories = []
        for categories in good_playlists[i]:
            all_categories.extend(categories)
        c = collections.Counter(all_categories)
        print(c)
        print("===========")

# get_category_count()


# print(len(good_playlists))
# print(len(good_playlists_artists))
