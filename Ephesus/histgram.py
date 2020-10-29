import matplotlib.pyplot as plt
from category import get_all_user_review_numbers
from datasets import all_reviews_df
from main import movies_similarities


def show_histgram(arr, x):
    plt.hist(arr, bins=x)
    plt.show()


# show_histgram(get_all_user_review_numbers(all_reviews_df), 90)


def get_similar_movie_numbers():
    total_row = []
    for row in movies_similarities:
        total_row.extend(row)
    return total_row


similar_movie_numbers = get_similar_movie_numbers()

show_histgram(similar_movie_numbers, 50)
