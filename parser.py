#-*- coding : utf-8 -*-

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

keyword_urls.sort(key = lambda s: len(s.keyword), reverse=True)
# --- <test set ---

target_string = "無脊椎動物プラットフォームは無脊椎動物のプラットフォームです。無脊椎動物プラットフォームはいいぞ。"
print(target_string)

for i, tmp_keyword_url in enumerate(keyword_urls):
    pattern = re.compile(tmp_keyword_url.keyword)
    target_string = re.sub(pattern, "%" + str(i) + "%", target_string)

print(target_string)

for urlid, tmp_keyword_url in enumerate(keyword_urls):
    pattern = re.compile("%" + str(urlid) + "%")
    target_string = re.sub(pattern, tmp_keyword_url.url,target_string)

print(target_string)
