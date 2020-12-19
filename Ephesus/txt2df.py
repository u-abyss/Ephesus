import pandas as pd
import numpy as np

from show_network import show_graph


similarity_df = pd.read_table('../music_data/artist_similarity.txt')
artist_data_df = pd.read_table('../music_data/atrist_data.txt')

# print(similarity_df)
print(artist_data_df.iloc[:, 1])


artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

# print(artist_categories)

# similar_artists_list = []

# for row in similarity_df.itertuples(name=None):
#     similar_artists = list(row)
#     similar_artists.pop(0)
#     similar_artists_list.append(similar_artists)

# show_graph(similar_artists_list)