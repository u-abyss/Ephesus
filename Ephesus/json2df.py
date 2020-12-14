import pandas as pd
import json

json_path = "../music_data/spotify_data/data/mpd.slice.0-999.json"

# json_open = open(json_path, 'r')

# json_load = json.load(json_open)

# df = pd.read_json(json_load)

data = json.load(open(json_path))
df = pd.DataFrame(data['playlists'])
print(df)