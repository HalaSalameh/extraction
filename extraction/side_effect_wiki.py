# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import json
import wikipedia


try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def check_words(word):

    wiki ="ويكيبيديا"
    query = word+ " "+ wiki
    url=""
    title=""
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        url=j
    try:
        response = requests.get(url)
    except Exception as e:
        return False,None

    soup=BeautifulSoup(response.text, features='xml')
    categories=[]

    for link in soup.find_all('a', href=re.compile(r"/wiki/")):
        for links in link:
            categories.append(link.get('title'))
    for car in categories:
        if car != "بوابة:طب":
            continue
        else :
            title = soup.select("#firstHeading")[0].text
            return True, title
    return False, None

