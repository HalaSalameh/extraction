import re
import time

try:
    from googlesearch import search
except ImportError:
    print("No module named 'google' found")


def get_drug_class_from_drugs_site(sent):
    headers = {'User-agent': 'your bot 0.1'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    wiki = '"drugs.com/drug-class"'
    query = sent + " " + wiki
    titles = []

    search_res = search(query, tld="co.in", num=10, stop=10, pause=10, user_agent=headers['User-Agent'])
    time.sleep(5)
    for url in search_res:
        # print(url)
        if 'www.drugs.com/drug-class/' in url:
            # print(url)
            splits = url.split('//www.drugs.com/drug-class/')
            title = re.sub(".html", "", splits[1])
            title = re.sub('-', " ", title)
            titles.append(title)
    return titles


def get_drug_class_from_google(sent):
    wiki = 'medical word for'
    query = sent + " " + wiki
    search_res = search(query, tld="co.in", num=10, stop=10, pause=10)
    titles = []
    for url in search_res:
        if "https://en.wikipedia.org/wiki/" in url:
            titles.append(url.split("wiki/")[1])
        if "https://www.merriam-webster.com/dictionary/" in url:
            titles.append(url.split("dictionary/")[1])
    return titles


def get_drug_class_from_google_final(sent):
    wiki = 'as mechanism of action'
    query = sent + " " + wiki
    search_res = search(query, tld="co.in", num=10, stop=10, pause=10)
    titles = []
    for url in search_res:
        if "https://en.wikipedia.org/wiki/" in url:
            titles.append(url.split("wiki/")[1])
        if "https://www.sciencedirect.com/topics/neuroscience/" in url:
            titles.append(url.split("neuroscience/")[1])
    return titles
