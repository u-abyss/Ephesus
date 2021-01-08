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
# print(chromagram)
# print(chromagram.shape)

# for i in chromagram:
#     print(len(i))


# def get_mfcc(file_path):
#     wave, sr = librosa.load(file_path)
#     mfccs = librosa.feature.mfcc(wave)
#     return mfccs

# mfccs = get_mfcc(file2_name)

# # nu = 0
# # for i in mfccs:
# #     print(nu)
# #     nu += 1
# #     print(len(i))
# #     print(nu)

# print(mfccs.shape)
# print(mfccs[0])
# print("==================")
# print(len(mfccs))

# # ベクトル量子化
# def vq(mfccs, k):
#     """mfccのベクトル集合をk個のクラスタにベクトル量子化"""
#     codebook, destortion = scipy.cluster.vq.kmeans(mfccs, k)
#     codes, dist = scipy.cluster.vq.vq(mfccs, codebook)
#     return codes

# codes = vq(mfccs, 15)
# print(codes)

# def get_signature():
#     mfssc = get_mfcc()
#     codes = vq()

#     # 各クラスタのデータ数，平均ベクトル，共分散行列を求めてシグネチャとする
#     for k in range(15):
#         # クラスタkのフレームのみ抽出
#         frames = np.array([mfccs[i] for i in range(len(mfccs)) if codes[i] == k])

# # if __name__ == "__main__":
# #     if len(sys.argv) != 3:
# #         print(usage: python mfcc_to_signature.py [mfccdir] [sigdir])
# #         sys.exit()

# #     mfccDir = sys.argv[1]
# #     sigDir  = sys.argv[2]

# #     if not os.path.exists(sigDir):
# #         os.mkdir(sigDir)

# #     for file in os.listdir(mfccDir):
# #         if not file.endswith(".mfc"): continue
# #         mfccFile = os.path.join(mfccDir, file)
# #         sigFile = os.path.join(sigDir, file.replace(".mfc", ".sig"))

# #         print(mfccFile, "=>", sigFile)

# #         fout = open(sigFile, "w")

# #         # MFCCをロード
# #         # 各行がフレームのMFCCベクトル
# #         mfcc = loadMFCC(mfccFile, 20)

# #         # MFCCをベクトル量子化してコードを求める
# #         code = vq(mfcc, 16)

# #         # 各クラスタのデータ数、平均ベクトル、
# #         # 共分散行列を求めてシグネチャとする
# #         for k in range(16):
# #             # クラスタkのフレームのみ抽出
# #             frames = np.array([mfcc[i] for i in range(len(mfcc)) if code[i] == k])
# #             # MFCCの各次元の平均をとって平均ベクトルを求める
# #             m = np.apply_along_axis(np.mean, 0, frames)  # 0は縦方向
# #             # MFCCの各次元間での分散・共分散行列を求める
# #             sigma = np.cov(frames.T)
# #             # 重み（各クラスタのデータ数）
# #             w = len(frames)
# #             # このクラスタの特徴量をフラット形式で出力
# #             # 1行が重み1個、平均ベクトル20個、分散・共分散行列400個の計421個の数値列
# #             features = np.hstack((w, m, sigma.flatten()))
# #             features = [str(x) for x in features]
# #             fout.write(" ".join(features) + "\n")
# #         fout.close()