#!/usr/bin/env python3

import requests, ssl, sys, csv
from bs4 import BeautifulSoup
# Get the lists of urls and keywords from read_file.py
from read_file import read_keywords
from read_file import read_url

# Turn url_list into a list of lists
def create_url_lists(url_list):
    url_lists = []
    for url in url_list:
        turn_url_into_list = []
        turn_url_into_list.append(url)
        url_lists.append(turn_url_into_list)
    return url_lists

# Pass in the urls and keywords
# Iterate through the urls
# Get <a> tags on each page
# Iterate through the keywords
# Get <a> tags containing the keywords
# Get the href of the <a> tags
# Add the resulted href to a list
# Add the list to link_list which contains lists of the urls found on each page
def get_links(url_lists, keywords_list):
    print("Getting urls ...")
    # a list of lists of urls found on each page
    link_lists = []
    for url_list in url_lists:
        new_url_list = []
        for url in url_list:
            #send get request
            response = requests.get(url)
            if response.status_code == 404:
                print("Can't reach {}".format(url))
            new_url_list.append(url)
            #parse html page
            html_page = BeautifulSoup(response.text, "html.parser")
            # get all <a> tags from the website
            all_links = html_page.findAll("a")
            for link in all_links:
                for keyword in keywords_list:
                    if keyword in str(link):
                        href = str(link.get('href'))
                        if href.endswith("/"):
                            href = href[:-1]
                        if "http" not in href:
                            if href.startswith("/") or href.startswith("#"):
                                href = url + href
                            else:
                                href = url + "/" + href
                        if href not in new_url_list:
                            new_url_list.append(href)
        link_lists.append(new_url_list)
    print("Got urls")
    return link_lists

if __name__ == "__main__":
    file_keywords = "keywords.txt"
    file_url = "school_links.txt"
    
    keywords_list = read_keywords(file_keywords)
    url_list = read_url(file_url)
    url_lists = create_url_lists(url_list)

    print(get_links(url_lists, keywords_list))

