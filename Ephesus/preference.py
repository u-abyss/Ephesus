import pandas as pd
from movie import get_reviewed_movieIds

category_names = [
    'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]

def get_user_category_preference(movie_description_df, all_reviews_df, n, user_id):
    reviewd_movieIds = get_reviewed_movieIds(user_id, all_reviews_df)
    sum_reviews = movie_description_df[movie_description_df["movie_id"].isin(reviewd_movieIds)].sum()
    print(sum_reviews)
    sum_reviews.drop(labels=["movie_id", "unknown"], inplace=True)
    if n > 0:
        return sum_reviews.sort_values(ascending=False).index[:n]
    else:
        return sum_reviews.sort_values(ascending=False).index[n]