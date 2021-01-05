import pandas as pd
import numpy as np
# from show_network import show_graph

similarity_df = pd.read_table('../music_data/artist_similarity.txt')

artist_data_df = pd.read_table('../music_data/atrist_data.txt', names=["artist_id","artist_name", "url"])

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)
