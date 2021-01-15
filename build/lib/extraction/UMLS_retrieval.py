from __future__ import print_function
# from UMLS_authentication import *
import requests
import json
import argparse
from googletrans import Translator

from extraction.UMLS_authentication import Authentication

translator = Translator()
apikey = "fccde92f-19ad-43b1-8f8c-7e7f544395d2"
uri = "https://uts-ws.nlm.nih.gov"
version = "current"
content_endpoint = "/rest/search/"+ version
def get_code(string):


    global apikey,uri,content_endpoint
    translation = translator.translate(string, src='ar')
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    ticket = AuthClient.getst(tgt)
    query = {'string': translation.text, 'ticket': ticket, 'pageNumber': 1}
    try:
        r = requests.get(uri + content_endpoint, params=query)
    except Exception as e:
        return [],False
    r.encoding = 'utf-8'
    items = json.loads(r.text)
    jsonData = items["result"]
    results = []
    i = 0
    for result in jsonData["results"]:
        if i==4:
            return results,True

        if jsonData["results"][0]["ui"] == "NONE":
            return [],False

        try:
            i +=1
            results.append((result["ui"],result['name']))
        except:
            return results,True

    if len(results) > 0:
        return results,True
    else:
        return [],False
