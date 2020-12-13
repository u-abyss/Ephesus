from bs4 import BeautifulSoup
import urllib.request, urllib.error

url = "http://dbpedia.org/page/Ornella_Vanoni"

html = urllib.request.urlopen(url)

soup = BeautifulSoup(html, "html.parser")

elems = soup.find_all(rel="dbo:genre")

for elem in elems:
    text = elem.text
    category = text.replace("dbr:", "")
    print(category)
