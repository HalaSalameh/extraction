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
def check(identifier,categories):


    global apikey,uri,version
    AuthClient = Authentication(apikey)
    tgt = AuthClient.gettgt()
    ticket = AuthClient.getst(tgt)
    content_endpoint = "/rest/content/" + str(version) + "/CUI/" + str(identifier)
    query = {'ticket': ticket, 'pageNumber': 1}
    try:
        r = requests.get(uri + content_endpoint, params=query)
    except Exception as e:
        print(e)
        return False
    r.encoding = 'utf-8'
    items = json.loads(r.text)
    jsonData = items["result"]
    try:
        arr = jsonData["semanticTypes"]
        if arr[0]['name'] in categories:
            return True
        else:
            return False
    except Exception as e:
        return "UN"
