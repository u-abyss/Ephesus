import shutil
import os
import pandas as pd
from pydub import AudioSegment

def move_files(category_name):
    base_path = "../data/ismir04_genre/audio/training/" + category_name + "/"
    files = os.listdir(base_path)

    for file in files:
        if file == ".DS_Store":
            continue
        path = base_path + file + "/"
        genres = os.listdir(path)
        for genre in genres:
            if genre == ".DS_Store":
                continue
            used_path = file + "/" + genre
            path2 = path + genre
            audios = os.listdir(path2)
            for audio in audios:
                if audio == ".DS_Store":
                    continue
                new_path = path2 + "/" + audio
                print(new_path)
                shutil.move(new_path, '../data/ismir04_genre/audio/' + category_name + "/")


PATH_LIST = "../ismir04_genre/metadata/development/tracklist.csv"

df = pd.read_csv(PATH_LIST, names=('class','artist_id','album_id','track_id','track_number','file_path'))
file_pathes = df["file_path"].tolist()

def mp3_to_wav(path_list):
    for path in path_list:
        track_name = path.split(".mp3")[0]
        mp3_path = "../ismir04_genre/audio/development/" + path
        sound = AudioSegment.from_mp3(mp3_path)
        time = sound.duration_seconds
        if time > 90:
            sound = sound[:90000]
            sound.export(f'../ismir04_genre/waves/{track_name}.wav', format="wav")
        else:
            sound.export(f'../ismir04_genre/waves/{track_name}.wav', format="wav")

mp3_to_wav(file_pathes)

print(file_pathes)

sound = AudioSegment.from_file("../ismir04_genre/audio/development/artist_2_album_1_track_3.mp3", format="mp3")
time = sound.duration_seconds
print(type(time))
print("再生時間:", time)

# sound1 = sound[:45000]
# time = sound1.duration_seconds
# print(time)

# sound1.export("test.mp3", format="mp3")