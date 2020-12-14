from bs4 import BeautifulSoup
import numpy as np
import urllib.request, urllib.error

from txt2df import artist_data_df

# アーティスト名とdbpediaのurlを配列に格納
def get_name_and_url():
    name_and_url_list = []
    for row in artist_data_df.itertuples(name=None):
        name_and_url = list(row[2:4])
        name_and_url_list.append(name_and_url)
    return name_and_url_list

# name_and_url_list = get_name_and_url()


def get_artist_category(urls):
    name_and_categories = []
    for u in urls:
        try:
            lst = []
            artist_name = u[0]
            url = u[1]
            html = urllib.request.urlopen(url)
            soup = BeautifulSoup(html, "html.parser")
            elems = soup.find_all(rel="dbo:genre")
            if elems == []:
                print('空だよ')
            else:
                categories = []
                for elem in elems:
                    text = elem.text
                    category = text.replace("dbr:", "")
                    categories.append(category)
                lst.append(artist_name)
                lst.append(categories)
                print(lst)
                name_and_categories.append(lst)
        except:
            pass
    return name_and_categories

# print(get_artist_category(name_and_url_list))
# name_and_categories = get_artist_category(name_and_url_list)

# np.save('../data/np_artist_name_category', name_and_categories)
print(np.load('../data/np_artist_name_category.npy', allow_pickle=True))
