import request
from bs4 import BeautifulSoup
import re

urlName = "http://dbpedia.org/page/"
target_url = request.get(urlName)
soup = BeautifulSoup(target_url.content, "html.parser")

