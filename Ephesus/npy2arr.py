import pandas as pd
import numpy as np

artist_categories = np.load('../data/np_artist_name_category.npy', allow_pickle=True)

good_playlists_artists = np.load("../data/np_good_playlists_artists.npy", allow_pickle=True)

good_playlists = np.load("../data/np_good_playlists.npy", allow_pickle=True)
