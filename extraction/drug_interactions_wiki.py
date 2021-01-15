# -*- coding: utf-8 -*-

import requests

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")

def check_if_chemical(word):

    wiki = "ويكيبيديا"
    query = word + " " + wiki
    url = ""
    try:
        for j in search(query, tld="co.in", num=1, stop=1, pause=2):
            url = j
        try:
        
            response = requests.get(url)
            if "بوب كيم" in response.text or "PubChem" in response.text or "ChEBI" in response.text or "ATC" in response.text:
                return True
        except Exception as e:
            return False
    except:

        return False
    return False

