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
        # print(categories)
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