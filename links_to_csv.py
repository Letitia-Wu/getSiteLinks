#!/usr/bin/env python3

import requests, ssl, sys, csv
from colorama import Back
from bs4 import BeautifulSoup
from reportlab.platypus import SimpleDocTemplate


# Read the txt file with keywords
# Save the keywords in a list
def read_keywords(file_keywords):
    print("Getting keywords...")
    keywords_list = []
    with open(file_keywords) as f:
        for line in f:
            keywords_list.append(line.strip())
    print("Got keywords")
    return keywords_list
    
# Read the file with urls of the official websites of the shcools
# Save the urls in a list
def read_url(file_url):
    print("Getting urls...")
    url_list = []
    with open(file_url) as f:
        for line in f:
            url_list.append(line.strip())
    print("Got urls")
    return url_list

# Pass the list of schools' offical websites, and get the links embedded on each website
# Return a list of dictionaries with "Universities" and "Links" as keys
# and the school official website and extracted links as values
def get_links(url_list, keywords_list):
    print("Getting first layer links...")
    links_dict_list = []
    for url in url_list:
        links_dict = {"Universities": "", "Links": "", "Keywords": ""}
        all_hrefs_str = ""
        keywords_all = ""
        #send get request
        response = requests.get(url)
        #parse html page
        html_page = BeautifulSoup(response.text, "html.parser")
        # get all <a> tags from the website
        all_links = html_page.findAll("a")
        for link in all_links:
            for keyword in keywords_list:
                if keyword in str(link):
                    if keyword not in keywords_all:
                        keywords_all += keyword
                        keywords_all += " "
                    href = str(link.get('href'))
                    if "http" not in href:
                        if href.startswith("/") or href.startswith("#"):
                            href = url + href
                            if href not in all_hrefs_str:
                                all_hrefs_str += href
                                all_hrefs_str += "\n"
                        else:
                            href = url + "/" + href
                            if href not in all_hrefs_str:
                                all_hrefs_str += href
                                all_hrefs_str += "\n"
                    else:
                        if  href not in all_hrefs_str:
                            all_hrefs_str += href
                            all_hrefs_str += "\n"
                else:
                    pass
            links_dict["Keywords"] = keywords_all
            links_dict["Universities"] = url
            links_dict["Links"] = all_hrefs_str
        links_dict_list.append(links_dict)
    print("Got first layer links")
    return links_dict_list
    
def get_second_layer_links(links_dict_list):
    print("Getting second layer links...")
    # get each dict in links_dict_list
    for dict in links_dict_list:
        links_list = []
        all_hrefs_str = ""
        keywords_list = dict["Keywords"].strip().split()
        links_list = dict["Links"].strip().split("\n")
        for link in links_list:
            if link.endswith("/"):
                link = link[:-1]
            #send get request
            response = requests.get(link)
            #parse html page
            html_page = BeautifulSoup(response.text, "html.parser")
            # get all <a> tags from the website
            all_links = html_page.findAll("a")
            all_hrefs_str += link
            all_hrefs_str += "\n"
            for second_layer_link in all_links:
                for keyword in keywords_list:
                    if keyword in second_layer_link:
                        href = str(second_layer_link.get('href'))
                        if "http" not in href:
                            if href.startswith("/") or href.startswith("#"):
                                href = link + href
                                if href not in all_hrefs_str:
                                    all_hrefs_str += href
                                    all_hrefs_str += "\n"
                            else:
                                href = link + "/" + href
                                if href not in all_hrefs_str:
                                    all_hrefs_str += href
                                    all_hrefs_str += "\n"
                                
                        else:
                            if  href not in all_hrefs_str:
                                all_hrefs_str += href
                                all_hrefs_str += "\n"
        dict["Links"] = all_hrefs_str
    print("Got second layer links")
    return links_dict_list

# Write the data created by get_links to a csv file
def write_csv(data, data_csv):
    print("Wrting csv...")
    keys = ["Universities", "Keywords", "Links"]
    with open(data_csv, 'w') as data_csv:
        writer = csv.DictWriter(data_csv, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print("csv written")
    return data_csv
    
def write_txt(data, result_txt):
    print("Writing txt...")
    f = open(result_txt, "w")
    for dict in data:
        string = "Website searched: {}\nKeywords: {}\nLinks: {}".format(dict["Universities"],dict["Keywords"], dict["Links"])
        f.write(string)
        f.write("\n")
    print("txt written")
    print("done")
    return result_txt

if __name__ == "__main__":
    file_keywords = "keywords.txt"
    file_url = "school_links.txt"
    
    url_list = read_url(file_url)
    keywords_list = read_keywords(file_keywords)
    links_dict_list = get_links(url_list, keywords_list)
    data = get_second_layer_links(links_dict_list)
    
    data_csv = "Links from US Universities.csv"
    write_csv(data, data_csv)
    
    result_txt = "Result.txt"
    write_txt(data, result_txt)

