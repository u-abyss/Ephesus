import glob
import pandas as pd
import numpy as np

# =========================================================================================================================================

# categories = ["classical", "electronic", "jazz_blues", "metal_punk", "rock_pop", "world"]

audio_metadata_df = pd.read_csv('../../ismir04_genre/metadata/development/tracklist.csv', names=('category', 'artist_id', 'album_id', 'track_id', 'track_number', 'file_path'))

category_and_file_path_df = audio_metadata_df.loc[:,['category','file_path']]

def get_tracks_by_category(source_category):
    rows = category_and_file_path_df.query('category == @source_category')
    df_tracks = rows.loc[:, ["file_path"]]
    tracks_list = df_tracks.values.tolist()
    # 2次元リストを1次元リストに変換
    tracks_list = sum(tracks_list, [])
    tracks_list = remove_mp3_extension(tracks_list)
    return tracks_list

def remove_mp3_extension(arr):
    track_ids = []
    for file_name in arr:
        track_id = file_name.split(".")[0]
        track_ids.append(track_id)
    return track_ids


track_ids = get_tracks_by_category("metal_punk")
print(track_ids)

track_ids_in_order_npy = np.load("../../ismir04_genre/track_ids_in_order.npy")
track_ids_in_order_list = track_ids_in_order_npy.tolist()

recommended_track_indexes = []
for track_id in track_ids:
    index = track_ids_in_order_list.index(track_id)
    recommended_track_indexes.append(index)

print(recommended_track_indexes)