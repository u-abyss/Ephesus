import pandas as pd

category_names = [
    'movie_id', 'movie_title', 'release_date', 'video_release_date', 'imdb_url', 'unknown', 'action', 'adventure',
    'animation', 'children', 'comedy', 'crime', 'documentary', 'drama', 'fantasy', 'film_noir', 'horror', 'musical',
    'mystery', 'romance', 'sci_fi', 'thriller', 'war', 'western'
]

def get_user_category_preference(movie_description_org, target_user_reviews):
    total_result = pd.Series(index=category_names)
    for i in range(1, 6):
        item_ids = []
        # print(tmp)
        reviews_by_evaluation= target_user_reviews[target_user_reviews["rating"] == i]
        for item_id in reviews_by_evaluation.item_id:
            item_ids.append(item_id)
        # weights depended on movie review point
        if i == 1:
            multiple = 0.5
        elif i == 2:
            multiple = 0.75
        elif i == 3:
            multiple = 1
        elif i == 4:
            multiple = 1.5
        else:
            multiple = 2
        result = movie_description_org[movie_description_org["movie_id"].isin(item_ids)].sum() * multiple
        # print(result)
        if i == 1:
            total_result = result
        else:
            total_result = total_result + result
    # remove "movie_id" and "unknown"
    total_result.drop(labels=["movie_id", "unknown"], inplace=True)
    return total_result.sort_values(ascending=False)