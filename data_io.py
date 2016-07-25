#-*- coding : utf-8 -*-

"""
data_io.py
---
Data input output.
"""


from bs4 import BeautifulSoup as BS
import datetime
import sys
import re
import ast

import six
import codecs

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

    # TODO : with 'as' command, we can use table's own attribute.
    cur.execute("SELECT * FROM " + table + ";")



    keyword_urls = []

    # print(cur.fetchall())

    # TODO
    print('---Keywords and urls---')
    for item in cur.fetchall():
        print(item)
        keyword = item[1]
        url = item[2]
        if item[3] != 0:
            keyword_urls.append(word_url(keyword, "<a href=" + url+ " jplinker=True>" + keyword + "</a>"))


    keyword_urls.sort(key=lambda s: len(s.word), reverse=True)



    # <- TODO

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


# --- CSV MODE ---
def read_csv(keyword_list_path, target_list_path):
    import csv
    keyword_urls = []
    target_paths = []

    test_codecs = ['utf_8', 'euc_jp', 'euc_jis_2004', 'euc_jisx0213',
                   'shift_jis', 'shift_jis_2004', 'shift_jisx0213',
                   'iso2022jp', 'iso2022_jp_1', 'iso2022_jp_2', 'iso2022_jp_3',
                   'iso2022_jp_ext', 'latin_1', 'ascii']

    for i, filepath in enumerate((keyword_list_path, target_list_path)):
        for encoding in test_codecs:
            try:
                with codecs.open(filepath, 'r', encoding) as csvfile:
                    reader = csv.reader(csvfile, delimiter=",", quotechar='"')
                    for row in reader:
                        # loop for encoding check
                        pass
                correct_encoding = encoding
                break
            except UnicodeDecodeError:
                pass

        with codecs.open(filepath, 'r', correct_encoding) as csvfile:
            print('encoing: ', correct_encoding)
            reader = csv.reader(csvfile, delimiter=",", quotechar='"')

            if i == 0:
                for row in reader:
                    keyword = row[0]
                    url = row[1]
                    if row[2] != 0:
                        keyword_urls.append(word_url(keyword, "<a href=" + url + " jplinker=True>" + keyword + "</a>"))
            elif i == 1:
                for row in reader:
                    url = row[0]
                    if row[1] != 0:
                        target_paths.append(url)


    return (keyword_urls, target_paths)


# --- TEST MODE ---
def test_set():
    # --- test mode ---
    keyword_urls = []
    target_paths = ['./sample/sample.html']
    keyword_urls.append(word_url('触角葉',
                                 ('<a href='
                                  '"https://invbrain.neuroinf.jp/modules/xwords/entry.php?entryID=47&categoryID=1"'
                                  ' jplinker=True>触角葉</a>')))
    return (keyword_urls, target_paths)