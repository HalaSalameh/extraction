import requests
import os
import re
from bs4 import BeautifulSoup


def get_class_from_composition(composition):
    base_url = "https://www.drugbank.ca/unearth/q"
    params = {
        'searcher': 'drugs',
        'query': composition
    }
    try:
        page = requests.get(base_url, params=params)
        soup = BeautifulSoup(page.content, 'html.parser')
        therapeutic_Text = None
        therapeutic_list = []
        therapeutic_lis = soup.find('dt', string='AHFS Codes').find_next_sibling('dd').find('ul').findAll('li')
        if therapeutic_lis == None:
            return False, None
        for li in therapeutic_lis:
            therapeutic_list += li.get_text().split('—')[-1].strip().split(' and ')
        therapeutic_list = list(set(therapeutic_list))
        return True, therapeutic_list
    except:
        return False, None

