import mysql.connector as mydb
import numpy as np

# from txt2df import artist_data_df
# artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)
# print(artist_categories)

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

conn = mydb.connect(
    host="localhost",
    port="3306",
    user="root",
    password="Okyu8-0449",
    database="spotify_playlist",
)

conn.ping(reconnect=True)

# DB操作のカーソル
cur = conn.cursor()

# 対象とするプレイリストのidを取得
cur.execute("SELECT id FROM playlist WHERE num_followers >= 1000;")

rows = cur.fetchall()
playlist_ids = [item[0] for item in rows]

print(playlist_ids)

test_id = 881739

def fetch_track_ids():
    cur.execute("SELECT track_id FROM playlist_track_relation WHERE playlist_id = '%s'" % test_id)
    rows = cur.fetchall()
    track_ids = [item[0] for item in rows]
    return track_ids

track_ids = fetch_track_ids()

def fetch_album_ids(track_ids):
    placeholders = ', '.join(['%s']*len(track_ids))
    query = "SELECT album_id FROM track WHERE id IN ({})".format(placeholders)
    cur.execute(query, tuple(track_ids))
    rows = cur.fetchall()
    album_ids = [item[0] for item in rows]
    return album_ids

album_ids = fetch_album_ids(track_ids)


def fetch_artist_names(album_ids):
    placeholders = ', '.join(['%s']*len(album_ids))
    query = "SELECT name FROM album WHERE id IN ({})".format(placeholders)
    cur.execute(query, tuple(album_ids))
    rows = cur.fetchall()
    artist_names = [item[0] for item in rows]
    return artist_names

artists_names = fetch_artist_names(album_ids)
print(artists_names)

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

categories = []
for row in artist_categories:
    if row[0] in artists_names:
        categories.append(row[1])

print(categories)

# categories = map(lambda row: row[0] in artists_names, artist_categories)
# print(categories)

# for i in categories:
#     print(i)



