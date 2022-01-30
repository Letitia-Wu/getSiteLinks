#!/usr/bin/env python3

# Read the txt file with keywords
# Save the keywords in a list
def read_keywords(file_keywords):
    print("Reading keywords...")
    keywords_list = []
    with open(file_keywords) as f:
        for line in f:
            keywords_list.append(line.strip())
    print("Got keywords")
    return keywords_list
    
# Read the txt file with urls of the official websites of the shcools
# Save the urls in a list
def read_url(file_url):
    print("Reading urls...")
    url_list = []
    with open(file_url) as f:
        for line in f:
            url_list.append(line.strip())
    print("Got urls")
    return url_list

if __name__ == "__main__":
    file_keywords = "keywords.txt"
    file_url = "school_links.txt"
    
    read_keywords(file_keywords)
    read_url(file_url)
