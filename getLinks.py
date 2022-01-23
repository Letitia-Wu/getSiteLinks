#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

urls = 'https://catalog.gatech.edu/coursesaz/'
grab = requests.get(urls)
soup = BeautifulSoup(grab.text, 'html.parser')

# opening a file in write mode
f = open("test1.txt", "w")
# traverse paragraphs from soup
for link in soup.find_all("a"):
    data = link.get('href')
    if data == None:
        pass
    else:
        f.write(data)
        f.write("\n")

f.close()




