
from bs4 import BeautifulSoup as BS
import datetime
import sys
import re
import ast

import six

# --- definition of 'word_url' class
class word_url:
    def __init__(self, word, url):
        self.word = word
        self.url = url

# --- import settings from settings.py
import settings

'''
system = settings.DATABASESYSTEM
database = settings.DATABASES[settings.DATABASE]
'''

def set_dbcursor(system, database):
    database = settings.DATABASES[database]

    if system == 'sqlite':
        import sqlite3
        conn = sqlite3.connect(database['DBPATH'])
        cur = conn.cursor()
    elif system == 'mysql':
        import mysql.connector
        conn = mysql.connector.connect(
            database=database['NAME'],
            user=database['USER'],
            password=database['PASSWORD'],
            host=database['HOST'],
            port=database['PORT']
        )
        cur = conn.cursor()
    else:
        print('DataBase Type is not correctly set!')

    return cur


def fetch_keyword(dbcursor, database):
    #--- Get keywords and corresponding urls from Database

    cur = dbcursor

    table = settings.DATABASES[database]['TABLES']['KEYWORD']

    cur.execute("SELECT * FROM " + table + ";")

    keyword_urls = []

    print(cur.fetchall())

    '''
    for item in cur.fetchall():

        keyword = item[1]
        url = item[2]
        if item[3] != 0:
            keyword_urls.append(word_url(keyword, "<a href=" + url+ " jplinker=True>" + keyword + "</a>"))


    keyword_urls.sort(key=lambda s: len(s.word), reverse=True)


    target_html=codecs.open("sample/sample.html", 'r', "utf-8")

    '''

    return keyword_urls

def fetch_html(dbcursor, database):
    # TODO
    cur = dbcursor

    table = settings.DATABASES[database]['TABLES']['HTML']

    try:
        cur.execute("SELECT * FROM " + table + ";")
    except BaseException:
        print('ERROR! The TABLE name of target file path is not correctly set.')
        print('\t Please check "settings.py"')

    pass


def test_set():
    # --- test mode ---
    keyword_urls = []
    target_path = './sample/sample.html'
    keyword_urls.append(word_url('触角葉',
                                 ('<a href='
                                  '"https://invbrain.neuroinf.jp/modules/xwords/entry.php?entryID=47&categoryID=1"'
                                  ' jplinker=True>触角葉</a>')))
    return (keyword_urls, target_path)