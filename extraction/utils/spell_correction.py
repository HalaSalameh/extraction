#!/home/adamryman/bin/venv3/bin/python3
"""Takes a phrase as input and Googles it.
If Google thinks the phrase should be different, print Google's phrase to standard out,
otherwise print the input phrase to standard out"""

import sys, os
import requests
from bs4 import BeautifulSoup


def get_google_spelling(phrase):
    """Return how google would spell the phrase"""
    page = get_page(phrase)

    spell_tag = get_spell_tag(page)

    # If the spell tag does not exist or if the text is empty then the input is
    # spelled correctly as far as Google is concerned so we output the input
    if spell_tag is None or spell_tag.text == "":
        return phrase
    else:
        return spell_tag.text


def get_spell_tag(page):
    """Get out the tag that has the Google spelling or is empty"""
    # print(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')
    # print(soup)
    # print(soup)

    spell_tag = soup.find('a', {'class': 'gL9Hy'})
    # print(spell_tag)
    if not spell_tag:
        spell_tag = soup.find('div', {'id': 'scc', 'class': 'BmP5tf'})
        if spell_tag:
            spell_tag = spell_tag.find('b')

    return spell_tag


def get_page(search):
    """Get Google html page that has Google spelling and/or same spelling"""
    headers = {
        "User-Agent":
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0",
    }

    proxies = {
        "http": "http://213.244.124.19:3128",
        "https": "http://213.244.124.19:3128",
    }

    # print("weheeeeeee")
    # print(os.environ.get('http_proxy'))

    # print(get_google_spelling("truffen"))
    # url = 'http://google.com/search?h1=en&q=' + search + "&meta=&gws_rd=ssl"
    url = 'http://google.com/search?h1=en&q=' + search

    page = requests.get(url)

    # print(url)
    return page


# print(get_google_spelling('hemophobea'))

