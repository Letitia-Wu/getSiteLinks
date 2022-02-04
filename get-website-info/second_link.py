#!/usr/bin/env python3

url = "https://www.duke.edu"
link = "https://studentassistance.duke.edu"
keyword = "accounting"

import requests, ssl, sys, csv, re, datetime
from bs4 import BeautifulSoup

#send get request
response = requests.get(link)
if response.status_code == 404:
    print("Can't reach {}".format(url))
#parse html page
html_page = BeautifulSoup(response.text, "html.parser")
# get all <a> tags from the website
all_links = html_page.findAll("a")
for link in all_links:
    if keyword in str(link):
        href = str(link.get('href'))
        print(href)
