import pandas as pd
import numpy as np

# similarity_df = pd.read_table('../music_data/artist_similarity.txt')

# artist_data_df = pd.read_table('../music_data/atrist_data.txt', names=["artist_id","artist_name", "url"])

# artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

# test = np.load("../ismir04_genre/eval_list.npy")
# # print(len(test))

# # x1 = np.load("../ismir04_genre/similarities/artist_122_album_1_track_3.npy")
# # x2 = np.load("../ismir04_genre/similarities/artist_100_album_1_track_2.npy")
# # x3 = np.load("../ismir04_genre/similarities/artist_100_album_1_track_3.npy")
# # print(x1)
# # print(x2)
# # print(x3)

# elm_num = 3

# np.random.seed(0)
# a = np.random.rand(elm_num)
# b = np.random.rand(elm_num)

# print(type(a))
# print(a)
# print(a.shape)

# a = np.arange(3)
# print(a)
# b = np.arange(3)

# result = a @ b
# print(result)
# print(type(result))

# x = np.load("../ismir04_genre/npy/reverse/artist_106_album_2_track_3.npy")
# y = np.load("../ismir04_genre/similarities/artist_26_album_1_track_2.npy")
# print(y)
import glob

num = 0
files = glob.glob("../ismir04_genre/similarities/*")
for file in files:
    print(file)
    print(num)
    num += 1
