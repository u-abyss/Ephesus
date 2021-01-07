from os import path
from pydub import AudioSegment
import sys
from ffprobe import FFProbe

# sys.path.append('/path/to/ffmpeg')

file_name = "../data/ismir04_genre/audio/development/artist_1_album_1_track_1.mp3"

sound = AudioSegment.from_mp3(file_name)
sound.export("file.wav", format="wave")
