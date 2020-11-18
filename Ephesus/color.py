def get_color_by_user_reference(node, array):
    label = array[node-1]
    if label == 'watch_fave':
        return 'deeppink'
    elif label == 'watch_not_fave':
        return 'lightpink'
    elif label == 'not_watch_fave':
        return 'lightblue'
    elif label == 'not_watch_not_fave':
        return 'whitesmoke'
    elif label =='not_watch':
        return 'whitesmoke'
    else:
        return 'lightblue'

def get_color_by_selected_category(label):
    if label == "selected_category":
        return "gold"
    else:
        return "whitesmoke"
