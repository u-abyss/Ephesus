import glob
import pandas as pd
import numpy as np

# audio_metadata_df = pd.read_csv('../ismir04_genre/metadata/development/tracklist.csv', names=('category', 'artist_id', 'album_id', 'track_id', 'track_number', 'file_path'))

# category_and_file_path_df = audio_metadata_df.loc[:,['category','file_path']]

# world_df = category_and_file_path_df.query('category == "world"')
# print(world_df)
# print(type(world_df))

# similaritiesディレクトリの全ファイルを取得する
def get_all_files_path_in_similarites_directory():
    similarities_list = []
    file_pathes = glob.glob("../ismir04_genre/similarities/*")
    return file_pathes

audio_similarities_npy = np.load("../ismir04_genre/audio_similarities.npy")

audio_similarities_list = audio_similarities_npy.tolist()

SIMILARITES_NUM = len(audio_similarities_list)

waves_path_npy = np.load("../ismir04_genre/waves_path_list.npy")

# 基準となるファイルパスの順番
waves_path_list = waves_path_npy.tolist()

def get_track_ids_in_order(path_lists):
    track_ids = []
    for path in waves_path_list:
        splited_path = path.split("/")[3]
        track_id = splited_path.split(".")[0]
        track_ids.append(track_id)
    return track_ids

track_ids = get_track_ids_in_order(waves_path_list)

sorted_path_npy = []

for track_id in track_ids:
    path = "../ismir04_genre/similarities/" + track_id + ".npy"
    sorted_path_npy.append(path)

def create_similarity_matrix():
    audio_similarity_matrix = []
    for path in sorted_path_npy:
        similarity_list = np.load(path)
        audio_similarity_matrix.append(similarity_list)
    return audio_similarity_matrix

similarity_matrix = np.load("../ismir04_genre/similarity_matrix.npy")
print(similarity_matrix.tolist())


# =========================================================================================================================================

# movie_dict = {}
# all_categories = []

# movie_categories = [
#     'unknown', 'action', 'adventure', 'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
#     'film_noir', 'horror', 'musical', 'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
# ]


# """
# categorize_movie()
# 各映画を一つのカテゴリーで分ける
# 複数のカテゴリーがあるものに一番先頭にあるカテゴリーをその映画のカテゴリーとして定義する
# {movieID: 'category'}
# """

# def get_user_review_movieIds(all_reviews_df, user_id):
#     user_review_movieIds = (
#         all_reviews_df[all_reviews_df['user_id'] == user_id + 1]['item_id']).tolist()
#     return user_review_movieIds


# def get_all_user_review_numbers(all_reviews_df):
#     all_user_review_numbers = []
#     # count = 0
#     MAX_USER_RANGE = 944
#     for i in range(1, MAX_USER_RANGE):
#         user_reviews_df = all_reviews_df[all_reviews_df['user_id'] == i]
#         # print(user_reviews_df)
#         # if len(user_reviews_df) not in all_user_review_numbers:
#         #     count += 1
#         all_user_review_numbers.append(len(user_reviews_df))
#     # 各ユーザが何本の映画に評価をつけたかに関するタプル型の配列 [(user_id-1, 見た映画の本数)]
#     print(sorted(enumerate(all_user_review_numbers), key=lambda x:x[1], reverse=True))
#     return all_user_review_numbers


# def isUserPreferenceCategory(sum: int) -> bool:
#     if sum != 0:
#         return True
#     else:
#         return False


# """
# 各映画を４つに分ける
# 「見たことのある映画かつ好きなカテゴリーを含む」
# 「見たことのある映画かつ好きなカテゴリーを含まない」
# 「見たことない映画かつ好きなカテゴリーを含む」
# 「見たことない映画かつ好きなカテゴリーを含まない」
# """


# def get_categorized_movies_by_user_preference(movie_description_df, top5_categories, all_reviews_df, user_id):
#     categorized_movies_by_user_preference = []
#     user_reviewed_movieIds = get_user_review_movieIds(all_reviews_df, user_id)
#     categorized_movies_by_user_preference_append = categorized_movies_by_user_preference.append
#     for row in (movie_description_df.loc[:, top5_categories]).itertuples():
#         sm = sum(row) - row.Index
#         # すでに見た映画かどうかの場合分け
#         if row.Index + 1 in user_reviewed_movieIds:
#             # カテゴリがユーザの好みのカテゴリのリストに入っているかどうかの判定
#             if isUserPreferenceCategory(sm) == True:
#                 categorized_movies_by_user_preference_append('watch_fave')
#             else:
#                 categorized_movies_by_user_preference_append('watch_not_fave')
#         else:
#             categorized_movies_by_user_preference_append('not_watch')
#             # if isUserPreferenceCategory(sm) == True:
#             #     categorized_movies_by_user_preference_append('not_watch_fave')
#             # else:
#             #     categorized_movies_by_user_preference_append('not_watch_not_fave')
#     return categorized_movies_by_user_preference


# """
# 分野横断先のカテゴリーを一つ決定する
# 各映画がそのカテゴリーを持っているのかいないのかを判別する
# その映画をみたことがあるのかないのかを判別する
# """


# def isUserSelectedCategory(label: int) -> bool:
#     if label == 1:
#         return True
#     else:
#         return False


# def get_categorized_movies_by_selected_category(category: str, all_reviews_df, movie_description_df, user_id):
#     categorized_movies_by_selected_category = []
#     user_review_movieIds = get_user_review_movieIds(all_reviews_df, user_id)
#     categorized_movies_by_selected_category_append = categorized_movies_by_selected_category.append
#     for index, label in (movie_description_df.loc[:, category]).iteritems():
#         if index + 1 not in user_review_movieIds:  # 未視聴の映画
#             if isUserSelectedCategory(label) == True:
#                 categorized_movies_by_selected_category_append(
#                     'selected_category')
#             else:
#                 categorized_movies_by_selected_category_append(
#                     'not_selected_category')
#         else:
#             categorized_movies_by_selected_category_append('watched')
#     return categorized_movies_by_selected_category
