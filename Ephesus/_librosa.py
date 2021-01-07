import librosa
import librosa.display
import matplotlib.pyplot as plt

file_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_1.mp3"
file2_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_2.mp3"
wave_file = "../data/0341 copy.wav"

wave, sr = librosa.load(file2_name, sr = 44100)
mfccs = librosa.feature.mfcc(wave, sr = sr)

print(mfccs.shape)

