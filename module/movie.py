# 対象とするユーザが見た映画のidを配列
def get_reviewed_movieIds(userId, u_data_org):
    target_user_reviews = u_data_org[u_data_org['user_id'] == userId]
    user_watched_movies = []
    for i in target_user_reviews.item_id:
        user_watched_movies.append(i)
    return user_watched_movies
    # print(type((movie_description_org[movie_description_org['movie_id'].isin(user_watched_movies)]).sum()['action'])