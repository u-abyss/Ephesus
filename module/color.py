import random

# 映画のジャンルに応じて,　ノードに色付けをする
def get_color(node, dict):
    category = dict[node]
    if category == 'unknown':
        return 'grey'
    elif category == 'action':
        return 'mediumvioletred'
    elif category == 'adventure':
        return 'green'
    elif category == 'animation':
        return 'yellow'
    elif category == 'children':
        return 'orange'
    elif category == 'comedy':
        return 'gold'
    elif category == 'crime':
        return 'purple'
    elif category == 'documentary':
        return 'brown'
    elif category == 'drama':
        return 'lightyellow'
    elif category == 'fantasy':
        return 'pink'
    elif category == 'film_noir':
        return 'aqua'
    elif category == 'horror':
        return 'black'
    elif category == 'musical':
        return 'tomato'
    elif category == 'mystery':
        return 'navy'
    elif category == 'romance':
        return 'magenta'
    elif category == 'sci_fi':
        return 'darkgreen'
    elif category == 'thriller':
        return 'darkslategray'
    elif category == 'war':
        return 'darkred'
    else:
        return 'chocolate'

# ランダムにカラーコードを生成する
def generate_random_color_code():
    return '#{:X}{:X}{:X}'.format(*[random.randint(10, 255) for _ in range(3)])

# 映画のカテゴリーの種類数分だけのカラーコードを配列にappendする
colors = []
def get_colors():
    for i in range(216):
        while True:
            color = generate_random_color_code()
            # カラーコードの文字列の長さが6の場合draw_networkxでエラーが起きる. またカラーコードが被った場合もう一度カラーコードを生成する.
            if color not in colors and len(color) == 7:
                colors.append(color)
                break
    return colors

def get_random_color(node, dict):
    category_number = dict[node]
    color = colors[category_number]
    return color

def get_color_by_user_reference(node, array):
    label = array[node-1]
    if label == 'watch_fave':
        return 'deeppink'
    elif label == 'watch_not_fave':
        return 'lightpink'
    elif label == 'not_watch_fave':
        return 'blue'
    else:
        return 'lightblue'

def get_color_by_selected_category(label):
    if label == "selected_category":
        return "black"
    else:
        return "gray"

