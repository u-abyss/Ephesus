import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

file_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_1.mp3"
file2_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_2.mp3"
file3_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_3.mp3"
wave_file = "../data/0341 copy.wav"

x , sr = librosa.load(file3_name, sr=44100)
plt.figure(figsize=(14, 5))
librosa.display.waveplot(x, sr=sr)
# plt.show()
chromagram = librosa.feature.chroma_stft(x, sr=sr)
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', cmap='coolwarm')
plt.show()