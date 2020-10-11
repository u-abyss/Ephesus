movie_dict = {}
all_categories = []

movie_categories = [
    'unknown', 'action', 'adventure', 'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy',
    'film_noir', 'horror', 'musical', 'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]

def categorize_movies_completely(matrix):
    movie_id = 1
    category_number = 0
    for row in matrix.itertuples():
        categories = []
        for i in range(1, 20):
            if row[i] == 1:
                categories.append(i)
        if categories not in all_categories:
            all_categories.append(categories)
            category_number = all_categories.index(categories)
            movie_dict.setdefault(movie_id, category_number)
            movie_id += 1
        else:
            category_number = all_categories.index(categories)
            movie_dict.setdefault(movie_id, category_number)
            movie_id += 1
    return movie_dict

"""
categorize_movie()
各映画を一つのカテゴリーで分ける
複数のカテゴリーがあるものに一番先頭にあるカテゴリーをその映画のカテゴリーとして定義する
{movieID: 'category'}
"""

def categorize_movie(matrix):
    matrix.drop("movie_id", axis=1, inplace=True)
    movie_id = 1
    for row in matrix.itertuples():
        for i in range(1, 20):
            if row[i] == 1:
                movie_dict.setdefault(movie_id, movie_categories[i-1])
                movie_id += 1
                break
            else:
                continue
    return movie_dict

def get_user_review_movieIds(u_data_org):
    user_review_movieIds = []
    for i in range(1, 944):
        user_reviews_df = u_data_org[u_data_org['user_id'] == i]
        user_review_movieIds.append(len(user_reviews_df))
    # 各ユーザが何本の映画に評価をつけたかに関するタプル型の配列 [(user_id-1, 見た映画の本数)]
    # print(sorted(enumerate(user_review_numbers), key=lambda x:x[1], reverse=True))
    return user_review_movieIds

def get_categorized_movies_by_user_preference(movie_description_org, top5_categories, u_data_org):
    categorized_movies_by_user_preference = []
    for row in (movie_description_org.loc[:, top5_categories]).itertuples():
        user_reviewed_movieIds = get_user_review_movieIds(u_data_org)
        sm = sum(row)
        categorized_movies_by_user_preference_append = categorized_movies_by_user_preference.append
        # すでに見た映画かどうかの場合分け
        if row.Index + 1 in user_reviewed_movieIds:
            # カテゴリがユーザの好みのカテゴリのリストに入っているかどうかの判定
            if sm - row.Index != 0:
                categorized_movies_by_user_preference_append('watch_fave')
            else:
                categorized_movies_by_user_preference_append('watch_not_fave')
        else:
            if sm - row.Index != 0:
                categorized_movies_by_user_preference_append('not_watch_fave')
            else:
                categorized_movies_by_user_preference_append('not_watch_not_fave')
    return categorized_movies_by_user_preference