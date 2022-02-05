#!/usr/bin/env python3

import requests, ssl, sys, csv, re, datetime
from operator import itemgetter
from bs4 import BeautifulSoup
from read_file import read_keywords
from read_file import read_url
from report import generate_report
from datetime import date
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import PageBreak


# Pass in the urls and keywords
# Iterate through the urls
# Get <a> tags on each page
# Iterate through the keywords
# Get <a> tags containing the keywords
# Get the href and the text of the <a> tags
# Add the resulted href and text to a dict
# Add the dict to a list
# Add the list to link_list which contains lists of the urls found on each page

def get_links(url_list, keywords_list):
    print("Getting links ...")
    # an empty list holding the lists containing dicts
    link_dict_list = []
    # an empty list which will hold the href, so later we can check whether the href is unique
    new_url_list = []
    for url in url_list:
#    an empty list containing dicts
        dict_list = []
        #send get request
        response = requests.get(url)
#        if response.status_code == 404:
#            print("Can't reach {}".format(url))
        new_url_list.append(url)
        #parse html page
        html_page = BeautifulSoup(response.text, "html.parser")
        # get all <a> tags from the website
        all_links = html_page.findAll("a")
        for link in all_links:
        # an empty dict with the current university name, text of the links and href of the links as keys
            dict = {"university": "", "text": "", "link": ""}
            for keyword in keywords_list:
                if keyword in str(link).lower():
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
                        text = link.get_text().replace("\n", "")
                        dict["university"] = url
                        if len(text) > 0:
                            dict["text"] = text.strip()
                        else:
                            dict["text"] = "#Couldn't find text for this link"
                        dict["link"] = href.strip()
                        dict_list.append(dict)
        link_dict_list.append(dict_list)
#        for href in new_url_list:
#            print(href)
    print("Got links")
    return link_dict_list

# get sublinks text and href with the kyewords of specialties
# save the data into a list of lists containing dicts with university, text, link, subtext and sublink as the keys
#def get_sublinks(keywords_list, link_dict_list):
#    print("Getting sublinks ...")
#    # an empty list holding the lists containing dicts
#    sublinks_info = []
#    href_list = []
#    for dict_list in link_dict_list:
#
#        sublinks_dict_list = []
#        for dict in dict_list:
#            link = dict["link"]
#            sublink_dict = dict
#            #send get request
#            response = requests.get(link)
##            if not response.ok:
##                raise Exception("GET failed with status code {}\n with {} ".format(response.status_code, link))
#            #parse html page
#            html_page = BeautifulSoup(response.text, "html.parser")
#            # get all <a> tags from the website
#            all_sublinks = html_page.findAll("a")
#            for sublink in all_sublinks:
##                sublinks_dict_list.append(dict)
#                for keyword in keywords_list[1]:
#                    if keyword in str(sublink).lower():
#                        href = str(sublink.get('href'))
#                        sublink_text = sublink.get_text()
#                        if href.endswith("/"):
#                            href = href[:-1]
##                            print(href)
#                        if "http" not in href or href.startswith("/") or href.startswith("#"):
#                            pass
#                        else:
#                            if href not in href_list:
##                                print(href)
#                                href_list.append(href)
#                                sublink_dict["sublink_text"] = sublink_text
#                                sublink_dict["sublink"] = href
#                                sublinks_dict_list.append(sublink_dict)
##        print(sublinks_dict_list)
#        sublinks_info.append(sublinks_dict_list)
##    print(sublinks_info)
#    print("Got sublinks")
##    print(href_list)
#    return sublinks_info

def write_txt(keywords_list, link_dict_list, report_txt):
    print("Writing txt...")
    d = date.today()
    today = d.strftime("%B %d, %Y")
    keywords_string = ""
    for keyword in keywords_list:
        keyword = "'{}' ".format(keyword)
        keywords_string += keyword
    f = open(report_txt, "w")
    
    title = "{} universities searched with the keywords: {}\nGenerated on {}\n\n".format(len(link_dict_list), keywords_string, today)
    f.write(title)
    for link_list in link_dict_list:
        f.write("\n--------------------------------\n\n")
        f.write("University: {}\n".format(link_list[0]["university"]))
        f.write("{} results: \n".format(len(link_list)))
        link_list_sorted = sorted(link_list, key=itemgetter('text'))
        for dict in link_list_sorted:
            f.write("{}:  {}\n".format(dict["text"], dict["link"]))
    f.close()
    print("TXT written")
    return report_txt

def generate_report_info(keywords_list, link_dict_list):
    styles = getSampleStyleSheet()    
    report_info = ""
    content = ""
    d = date.today()
    today = d.strftime("%B %d, %Y")
    keywords_string = ""
    for keyword in keywords_list:
        keyword = "'{}' ".format(keyword)
        keywords_string += keyword
    report_info += "<a name='content'/>Generated on {}".format(today)
    report_info += "<br/><br/>"
    report_info += "{} universities searched with the keywords: {}".format(len(link_dict_list), keywords_string)
    report_info += "<br/><br/>"
    
    report_info += "<b>Content</b>"
    report_info += "<br/><br/>"
    
    for link_list in link_dict_list:
        number = str(link_dict_list.index(link_list) + 1)
        content += "{}. {} <a href='#{}' color='green'><i>See result</i></a>".format(number, link_list[0]["university"], link_list[0]["university"])
        content += "<br/>"
    report_info += content
    
    report_info += "--------------------------------"
    for link_list in link_dict_list:
        report_info += "<br/><br/>"
        report_info += "<a name='{}'/><b>University: {}</b>".format(link_list[0]["university"], link_list[0]["university"])
        report_info += "<br/>"
        report_info += "{} results: ".format(len(link_list))
        report_info += "<br/><br/>"
        link_list_sorted = sorted(link_list, key=itemgetter('text'))
        for dict in link_list_sorted:
            report_info += "{}:  <font color='blue'><u>{}</u></font>".format(dict["text"], dict["link"])
            report_info += "<br/>"
        report_info += "<br/>"
        report_info += "<a href='#content'><font color='green'>Back</font></a>"
        report_info += "<br/><br/>"
        report_info += "--------------------------------"
        report_info += "<br/><br/>"
    return report_info

if __name__ == "__main__":
    file_keywords = "keywords.txt"
    file_url = "school_links.txt"
    report_txt = "Websites info.txt"
    attachment = "Websites report.pdf"
    title = "Universities Report"
    
    keywords_list = read_keywords(file_keywords)
    url_list = read_url(file_url)
    link_dict_list = get_links(url_list, keywords_list)

    write_txt(keywords_list, link_dict_list, report_txt)
    
    paragraph = generate_report_info(keywords_list, link_dict_list)
    generate_report(attachment, title, paragraph)
    
    print("Done")

