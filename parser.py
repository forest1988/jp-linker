#-*- coding : utf-8 -*-

#--- use SQLite
import sqlite3

from bs4 import BeautifulSoup
import re
import six

class word_url:
    def __init__(self, word, url):
        self.word = keyword
        self.url = url

#--- GET target words from SQL, and set as a word
#--- use SQLite
dbpath="/Users/shadetree/workspace/django_test/mysite/db.sqlite3"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()
cur.execute("SELECT * FROM polls_keyword;")

user_word_urls = []

keyword_urls = []
for item in cur.fetchall():
    keyword = item[1]
    url = item[2]
    keyword_urls.append(word_url(keyword, "<a href=" + url+ " jplinker=True>" + keyword + "</a>"))


keyword_urls.sort(key=lambda s: len(s.keyword), reverse=True)


target_html = open('./sample/sample.html', mode='r')

soup = BeautifulSoup(target_html, "lxml")

'''
for i, descendant in enumerate(soup.descendants):
    print(i, descendant)
    #print(descendant.string)

for string in soup.stripped_strings:
    print(repr(string))

#tag_p = soup.p
#tag_p.a.decompose()

#print(tag_p)

# print(soup.find("a").extract())
#print("soup", soup.find_all(text=True, recursive=False))
'''
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

'''
print(soup.find_all(attrs={"jplinker": "Done"}))

strings = soup.find_all('font', size='-1')
for string in strings:
    # 本当はもっと再帰的にやらないとダメ
    if soup.find(attrs={"jplinker": "Done"}) !=None:
        soup.find(attrs={"jplinker": "Done"}).unwrap()
    print(string)

'''







target_string="カイコガ触覚葉に関する研究＠無脊椎動物プラットフォーム"

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