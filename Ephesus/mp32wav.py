import os
from pydub import AudioSegment

# mp3_path1 = "../data/ismir04_genre/audio/development/artist_1_album_1_track_1.mp3"
# mp3_path2 = "../data/ismir04_genre/audio/development/artist_1_album_1_track_2.mp3"


# sound = AudioSegment.from_mp3(mp3_path2)
# sound.export("wave2.wav", format="wav")

genres = ["pop", "metal", "world", "electronic", "classical", "rock", "punk", "jazz"]

path = "../data/ismir04_genre/audio/training/"

files = os.listdir(path)
print(files)