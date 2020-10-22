import pandas as pd

all_reviews_df = pd.read_csv(
    '../data/u.data',
    sep='\t',
    names=['user_id','item_id', 'rating', 'timestamp']
)

category_names = [
    'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]

movie_description_df = pd.read_csv(
    '../data/u.item.csv',
    sep='|',
    names=category_names,
    encoding='latin-1'
)

delete_columns = ['movie_title','release_date', 'video_release_date', 'imdb_url']
movie_description_df.drop(delete_columns, axis=1, inplace=True)