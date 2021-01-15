from urllib.request import urlopen
import re
import json
import html2text
from urllib.parse import quote

web_teb_ignored = ["FeedBack", "Advertise with Us", "Webteb"]


def get_token():
    url = "https://cse.google.com/cse.js?cx=003333014675457179190:wpk8hvbvqse&output=embed"
    try:
        content = urlopen(url).read()
        content = content.decode('utf8')
        content = re.split(r"\(*\)", content)
        token_str = "{"+(content[len(content)-2][3:])
        token_json = json.loads(token_str)
        return token_json['cse_token']
    except Exception as e:
        print(e)
        return False


def get_web_teb_text(query):
    
    global web_teb_ignored
    token = get_token()
    if not token:
        token = "AKaTTZhvC6aRcoFbJpEhyVBA8c-B:1570300990198"
    url = "https://cse.google.com/cse/element/v1?rsz=filtered_cse&num=10&hl=ar&source=gcsc&gss=.com&cselibv" \
          "=c96da2eab22f03d8&cx=003333014675457179190:wpk8hvbvqse&q=" + quote(query)+"" \
          "&safe=off&cse_tok=" + token + "&sort=&exp" \
          "=csqr,cc,4229469&googlehost=www.google.com&callback=google.search.cse.api3482 "

    try:
        content = urlopen(url).read()
    except Exception as e:
        print(e)
        return False, None
    content = content.decode('utf8')
    content_new = content.split("google.search.cse.api3482")[1]
    content_new = content_new[1:len(content_new)-2]
    content_json = json.loads(content_new)
    if 'results' not in  content_json:
        return False, None
    new_url = content_json['results'][0]['unescapedUrl']
    try:
        content = urlopen(new_url).read()
    except Exception as e:
        print(e)
        return False, None
    content = content.decode('utf8')
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images =True
    string = h.handle(content)
    ext = re.sub(r'[^a-z A-Z\n]', '', string)
    ext = ext.split('\n')
    ext =[e.strip() for e in ext if len(e.strip()) > 0 and e.strip() not in web_teb_ignored]

    if len(ext) > 0:

        return True, ext[0:min(len(ext), 3)]

    return False, None

#print(get_web_teb_text("نيكوتين"))
