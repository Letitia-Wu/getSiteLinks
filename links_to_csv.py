#!/usr/bin/env python3
from colorama import Back
import requests
from bs4 import BeautifulSoup
import ssl
import sys
import csv

# Read the file with urls of the official websites of the shcools
# Save the urls in a list
def read_url(file):
    url_list = []
    with open(file) as f:
        for line in f:
            url_list.append(line.strip())
    return url_list

# Pass the list of schools' offical websites, and get the links embedded on each website
# Return a list of dictionaries with the school official website's url as keys, and extracted links as values
def get_links(url_list):
    links_dict_list = []
    for url in url_list:
        #send get request
        response = requests.get(url)
        #parse html page
        html_page = BeautifulSoup(response.text, "html.parser")
        #get all <a> tags from the website
        all_links = html_page.findAll("a")
        for link in all_links:
            links_dict = {}
            href = link.get('href')
            href = str(href)
            if href.startswith("/") or href.startswith("#"):
                pass
            else:
                links_dict[url] = href
                links_dict_list.append(links_dict)
    return links_dict_list


# Write the data created by get_links to a csv file
def write_csv(data, data_csv):
    keys = []
#    print(data)
    for dict in data:
        for key in dict:
            if key not in keys:
                keys.append(key)
    with open(data_csv, 'w') as data_csv:
        writer = csv.DictWriter(data_csv, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    return data_csv

    
if __name__ == "__main__":
    file = "school_links.txt"
    url_list = read_url(file)
    data = get_links(url_list)
    data_csv = "Links from US Universities.csv"
    write_csv(data, data_csv)
    


