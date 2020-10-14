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

def get_user_review_movieIds(all_reviews_df):
    user_review_movieIds = []
    MAX_USER_RANGE = 944
    for i in range(1, MAX_USER_RANGE):
        user_reviews_df = all_reviews_df[all_reviews_df['user_id'] == i]
        user_review_movieIds.append(len(user_reviews_df))
    # 各ユーザが何本の映画に評価をつけたかに関するタプル型の配列 [(user_id-1, 見た映画の本数)]
    # print(sorted(enumerate(user_review_numbers), key=lambda x:x[1], reverse=True))
    return user_review_movieIds

def isUserPreferenceCategory(sum: int) -> bool:
    if sum != 0:
        return True
    else:
        return False

def get_categorized_movies_by_user_preference(movie_description_df, top5_categories, all_reviews_df):
    categorized_movies_by_user_preference = []
    user_reviewed_movieIds: List[int] = get_user_review_movieIds(all_reviews_df)
    categorized_movies_by_user_preference_append = categorized_movies_by_user_preference.append
    for row in (movie_description_df.loc[:, top5_categories]).itertuples():
        sm = sum(row) - row.Index
        # すでに見た映画かどうかの場合分け
        if row.Index + 1 in user_reviewed_movieIds:
            # カテゴリがユーザの好みのカテゴリのリストに入っているかどうかの判定
            if isUserPreferenceCategory(sm) == True:
                categorized_movies_by_user_preference_append('watch_fave')
            else:
                categorized_movies_by_user_preference_append('watch_not_fave')
        else:
            if isUserPreferenceCategory(sm) == True:
                categorized_movies_by_user_preference_append('not_watch_fave')
            else:
                categorized_movies_by_user_preference_append('not_watch_not_fave')
    return categorized_movies_by_user_preference

"""
分野横断先のカテゴリーを一つ決定する
各映画がそのカテゴリーを持っているのかいないのかを判別する
その映画をみたことがあるのかないのかを判別する
"""

def isUserSelectedCategory(label: int) -> bool:
    if label == 1:
        return True
    else:
        return False

def get_categorized_movies_by_selected_category(category: str, all_reviews_df, movie_description_df):
    categorized_movies_by_selected_category = []
    user_review_movieIds = get_user_review_movieIds(all_reviews_df)
    categorized_movies_by_selected_category_append = categorized_movies_by_selected_category.append
    # print(movie_description_df.loc[:, category])
    for index, label in (movie_description_df.loc[:, category]).iteritems():
        # print(label)
        if index + 1 not in user_review_movieIds:
            if isUserSelectedCategory(label) == True:
                categorized_movies_by_selected_category_append('selected_category')
            else:
                categorized_movies_by_selected_category_append('not_selected_category')
        else:
            categorized_movies_by_selected_category_append('watched')
    return categorized_movies_by_selected_category




