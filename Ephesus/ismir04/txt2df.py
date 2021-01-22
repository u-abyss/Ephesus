import pandas as pd
import numpy as np

# similarity_df = pd.read_table('../music_data/artist_similarity.txt')

# artist_data_df = pd.read_table('../music_data/atrist_data.txt', names=["artist_id","artist_name", "url"])

# artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

# test = np.load("../ismir04_genre/eval_list.npy")

# npy = np.load("../../ismir04_genre/waves_path_list.npy")
# lst = npy.tolist()

# track1 = lst[386]
# track2 = lst[490]
# track3 = lst[345]
# print(track1)
# print(track2)
# print(track3)


# test = np.load('../../ismir04_genre/final_similarity_matrix.npy')
# print(test)

test = np.load("../../ismir04_genre/result/world_jazz.npy", allow_pickle=True)
x = test.tolist()
print(len(x))
print(x[0][2])


# waves_path_npy = np.load("../../ismir04_genre/waves_path_list.npy")
# waves_path_list = waves_path_npy.tolist()
# def get_track_ids_in_order(path_lists):
#     track_ids = []
#     for path in waves_path_list:
#         splited_path = path.split("/")[3]
#         track_id = splited_path.split(".")[0]
#         mp3_name = track_id + ".mp3"
#         track_ids.append(mp3_name)
#     return track_ids

# track_ids = get_track_ids_in_order(waves_path_list)
# # print(track_ids)

# audio_metadata_df = pd.read_csv('../../ismir04_genre/metadata/development/tracklist.csv', names=('category', 'artist_id', 'album_id', 'track_id', 'track_number', 'file_path'))

# category_and_file_path_df = audio_metadata_df.loc[:,['category','file_path']]

# # print(category_and_file_path_df)

# categoris = []

# for mp3_name in track_ids:
#     row = category_and_file_path_df.query("file_path == @mp3_name")
#     category = row.category.tolist()
#     # print(category)
#     categoris.extend(category)

# # print(len(categoris))

# x = np.load("../../ismir04_genre/categories.npy")
# print(x.tolist())