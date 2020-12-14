import pandas as pd
import numpy as np
import json

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

json_path = "../music_data/spotify_data/data/mpd.slice.0-999.json"

data = json.load(open(json_path))

df = pd.DataFrame(data['playlists'])

drop_1_df = df[df['num_followers'] != 1]

tracks_10_df = drop_1_df[drop_1_df['num_tracks'] == 50]
print(tracks_10_df)

test_df = tracks_10_df[tracks_10_df['num_edits'] == 10]

test_tracks = test_df['tracks']
# print(test_tracks)

# あるプレイリストのアーティストの配列
listened_artist_names = []

for i in test_tracks:
    for j in i:
        artist_name = j["artist_name"]
        listened_artist_names.append(artist_name)


for artist_name in listened_artist_names:
    lowerd_artist_name = artist_name.lower()
    for i in artist_categories:
        if lowerd_artist_name == i[0]:
            print(i[0])
            print(i[1])
            print('------------------')