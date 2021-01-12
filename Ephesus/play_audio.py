# from playsound import playsoun
import simpleaudio

wave_path = "../ismir04_genre/wave/artist_100_album_1_track_1.wav"

wav_obj = simpleaudio.WaveObject.from_wave_file(wave_path)
play_obj = wav_obj.play()
play_obj.wait_done()


# playsound(wave_path)