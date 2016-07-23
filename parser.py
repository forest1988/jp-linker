#-*- coding : utf-8 -*-

from bs4 import BeautifulSoup
import re

class keyword_url:
    def __init__(self, keyword, url):
        self.keyword = keyword
        self.url = url

# TODO : GET target words from SQL, and set as a word


# --- test set> ---
keyword_urls = []
keywords = ["無脊椎", "脊椎", "無脊椎動物プラットフォーム", "プラットフォーム", "1023", "11"]
for urlid, keyword in enumerate(keywords):
    keyword_urls.append(keyword_url(keyword, "<a href=http://>" +str(keyword) + "<a>"))
    keyword_urls.append(keyword_url(">" + keyword + "</a>", None))

keyword_urls.sort(key = lambda s: len(s.keyword), reverse=True)
# --- <test set ---

target_html = '無脊椎動物プラットフォームは無脊椎動物のプラットフォームです。<a href="hogehoge">無脊椎動物プラットフォーム</a>はいいぞ。'

soup = BeautifulSoup(target_html, "lxml")


# print(soup.find("a").extract())
# print("soup", soup.find_all(text=True, recursive=False))

'''
original_string = soup.p.contents[:]

print(original_string)
'''

'''
for tag in soup.find_all(True, recursive=False):
    if tag.name != "a":
        if hasattr(tag, "text"):
            tag.string = "hogehoge"
            print(tag.name)
            print(tag.text)
        else:
            print("None")

print(soup)
print("Hello!")
'''

target_string = target_html
print(target_string)

for i, tmp_keyword_url in enumerate(keyword_urls):
    pattern = re.compile(tmp_keyword_url.keyword)
    target_string = re.sub(pattern, "%" + str(i) + "%", target_string)

print(target_string)

for urlid, tmp_keyword_url in enumerate(keyword_urls):
    pattern = re.compile("%" + str(urlid) + "%")
    if tmp_keyword_url.url != None:
        target_string = re.sub(pattern, tmp_keyword_url.url, target_string)
    else:
        target_string = re.sub(pattern, tmp_keyword_url.keyword, target_string)

print(target_string)
