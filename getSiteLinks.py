#!/usr/bin/env python3

#modules
from colorama import Back
import requests
from bs4 import BeautifulSoup
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.poolmanager import PoolManager
import ssl

#page url
url = r"https://umich.edu"

#send get request
response = requests.get(url)

#parse html page
html_page = BeautifulSoup(response.text, "html.parser")

#get all  tags
all_urls = html_page.findAll("a")

internal_urls = set()
external_urls = set()

f = open("result.txt", "w")
for link in all_urls:
    href=link.get('href')
    
    if href:
        if r"umich.edu" in href:
        #internal link
            internal_urls.add(href)
        elif href[0]=="#":
        #same page target link
            internal_urls.add("{}{}".format(url, href))
        else:
        #external link
            external_urls.add(href)

#print(Back.MAGENTA  + "Total External URLs: {}\n".format(len(internal_urls)))
#print("Total External URLs: {}\n".format(len(internal_urls)))
#f.write("Total External URLs: {}\n".format(len(internal_urls)))

for url in internal_urls:
#    print(Back.GREEN + "Internal URL {}".format(url))
    f.write("Internal URL {}".format(url))
    f.write("\n")
#    print("Internal URL {}".format(url))
#print(Back.MAGENTA  + "\n\nTotal External URLs: {}\n".format(len(external_urls)))
#print("\n\nTotal External URLs: {}\n".format(len(external_urls)))
#f.write("\n\nTotal External URLs: {}\n".format(len(external_urls)))

for url in external_urls:
#    print(Back.RED + "External URL {}".format(url))
    f.write("External URL {}".format(url))
    f.write("\n")
#    print("External URL {}".format(url))

f.close()
