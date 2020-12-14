import pandas as pd

from show_network import show_graph


similarity_df = pd.read_table('../music_data/artist_similarity.txt')
artist_data_df = pd.read_table('../music_data/atrist_data.txt')

print(artist_data_df)

# similar_artists_list = []

# for row in similarity_df.itertuples(name=None):
#     similar_artists = list(row)
#     similar_artists.pop(0)
#     similar_artists_list.append(similar_artists)

# show_graph(similar_artists_list)