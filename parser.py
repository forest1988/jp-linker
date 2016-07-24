#-*- coding : utf-8 -*-

#--- use SQLite
import sqlite3

from bs4 import BeautifulSoup
import re
import codecs
import six


class word_url:
    def __init__(self, word, url):
        self.word = word
        self.url = url

#--- GET target words from SQL, and set as a word
#--- use SQLite
dbpath="/Users/shadetree/workspace/django_test/mysite/db.sqlite3"
conn = sqlite3.connect(dbpath)
cur = conn.cursor()
cur.execute("SELECT * FROM polls_keyword;")

keyword_urls = []

for item in cur.fetchall():
    keyword = item[1]
    url = item[2]
    if item[3] != 0:
        keyword_urls.append(word_url(keyword, "<a href=" + url+ " jplinker=True>" + keyword + "</a>"))


keyword_urls.sort(key=lambda s: len(s.word), reverse=True)


target_html=codecs.open("sample/sample.html", 'r', "utf-8")

# soup = BeautifulSoup(target_html, "lxml")


def preprocess(target, offset):
    #--- refresh the output of last time
    tmp = target
    pattern = re.compile("<(.*?)jplinker=True>(.*?)<(.*?)>")
    tmp = re.sub(pattern, '\\2', tmp)

    user_words = []

    #--- user tags
    pattern = re.compile("<a href=(.*?)>(.*?)</a>")
    iter = re.finditer(pattern, tmp)
    for user_word_id, match in enumerate(iter):
        user_word_id = user_word_id + offset
        user_words.append(match.group(0))
        tmp = re.sub(match.group(0), "%" + str(user_word_id) + "%", tmp)

    preprocessed = tmp
    return (preprocessed, user_words)




def process(target, keyword_urls, user_words):
    tmp = target
    for key_id, keyword_url in enumerate(keyword_urls):
        pattern = re.compile(keyword_url.word)
        tmp = re.sub(pattern, "%" + str(key_id) + "%", tmp)

    for key_id, keyword_url in enumerate(keyword_urls):
        pattern = re.compile("%" + str(key_id) + "%")
        if keyword_url.url != None:
            tmp = re.sub(pattern, keyword_url.url, tmp)
        else:
            tmp = re.sub(pattern, keyword_url.word, tmp)

    for user_word_id, user_word in enumerate(user_words):
        user_word_id = user_word_id + len(keyword_urls)
        tmp = re.sub("%" + str(user_word_id) + "%", user_word, tmp)
        print(tmp)

    processed = tmp
    return processed

def test_keywords(keyword_urls):
    target_string='カイコガ<a href="http://hogehoge.text" jplinker=True>触角葉のこのような構造</a>は，脊椎動物の<a href="hoge">第一次嗅覚中枢</a>である嗅球と類似'
    print("target : ", target_string)
    offset = len(keyword_urls)

    (preprocessed_string, user_words) = preprocess(target_string, offset)
    processed_string = process(preprocessed_string, keyword_urls, user_words)
    print(processed_string)

    target_string='カイコガ<a href="hogehoge" jplinker=True>触角葉</a>に関する<a href="aaa">研究</a>＠無脊椎動物プラットフォーム'
    print("target : ", target_string)
    (preprocessed_string, user_words) = preprocess(target_string, offset)
    processed_string = process(preprocessed_string, keyword_urls, user_words)
    print(processed_string)


if __name__=='__main__':
    target_string=target_html.read()
    offset = len(keyword_urls)

    (preprocessed_string, user_words) = preprocess(target_string, offset)
    processed_string = process(preprocessed_string, keyword_urls, user_words)
    print(processed_string)

    f = open('./sample/test.html', 'w')
    f.write(processed_string)
    f.close()

