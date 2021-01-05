import numpy as np

from sqlconfig import sql_config



sql_config.ping(reconnect=True)

# DB操作のカーソル
cur = sql_config.cursor()

# 対象とするプレイリストのidを取得
cur.execute("SELECT id FROM playlist WHERE num_followers >= 1000;")

rows = cur.fetchall()
playlist_ids = [item[0] for item in rows]

"""
プレイリスト内の曲のtrack_idを取得する関数
"""
def fetch_track_ids(playlist_id):
    cur.execute("SELECT track_id FROM playlist_track_relation WHERE playlist_id = '%s'" % playlist_id)
    rows = cur.fetchall()
    track_ids = [item[0] for item in rows]
    return track_ids

"""
track_idから，その曲が含まれるアルバムのalbum_idを取得する関数
"""
def fetch_album_ids(track_ids):
    placeholders = ', '.join(['%s']*len(track_ids))
    query = "SELECT album_id FROM track WHERE id IN ({})".format(placeholders)
    cur.execute(query, tuple(track_ids))
    rows = cur.fetchall()
    album_ids = [item[0] for item in rows]
    return album_ids

"""
album_idからそのアルバムのアーティスト名を取得する関数
"""
def fetch_artist_names(album_ids):
    placeholders = ', '.join(['%s']*len(album_ids))
    query = "SELECT name FROM album WHERE id IN ({})".format(placeholders)
    cur.execute(query, tuple(album_ids))
    rows = cur.fetchall()
    artist_names = [item[0] for item in rows]
    return artist_names

"""
アーティスト名の配列から，各アーティストが属するカテゴリの配列を取得する関数
"""

def get_artist_categories(lowered_artist_names):
    artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)
    categories = []
    artists = []
    for row in artist_categories:
        if row[0] in lowered_artist_names:
            categories.append(row[1])
            artists.append(row[0])
    return categories, artists

"""
検証実験に使用できそうなプレイリストを返す関数
今のところ，アーティスト名からカテゴリを取得できるものを返してる．
"""
def find_good_playlist(playlist_ids):
    good_playlists = []
    good_playlist_artists = []
    for playlist_id in playlist_ids:
        track_ids = fetch_track_ids(playlist_id)
        album_ids = fetch_album_ids(track_ids)
        artist_names = fetch_artist_names(album_ids)
        # 大文字小文字を区別せずに，配列に含まれているかどうかをチェックするため，artist_namesの要素を全て小文字に変換する
        lowered_artist_names = list(map(lambda name: name.lower(), artist_names))
        artist_categories, artists = get_artist_categories(lowered_artist_names)
        if len(artist_categories) != 0:
            if len(artist_categories) >= 4:
                good_playlists.append(artist_categories)
                good_playlist_artists.append(artists)
    return good_playlists, good_playlist_artists


# 実験に使えそうなプレイリストに対応したアーティスト名の配列とそのアーティストのカテゴリの配列を返す
#TODO: カテゴリを算出できるアーティストのみを返す
good_playlists, good_playlist_artists = find_good_playlist(playlist_ids)

print(good_playlist_artists)
# print(len(good_playlist_artists))
print("================")
print(good_playlists)

