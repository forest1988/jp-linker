#-*- coding : utf-8 -*-

"""
data_io.py
---
Data input output.
"""


import sys
import six
import codecs

# --- definition of 'word_url' class
class word_url:
    def __init__(self, word, url):
        self.word = word
        self.url = url

# --- import settings from settings.py
import settings


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
    print('fetching keywords...')
    keyword_urls = []
    cur = dbcursor
    table = settings.DATABASES[database]['TABLES']['KEYWORD']['NAME']
    columns = settings.DATABASES[database]['TABLES']['KEYWORD']['COLUMNS']

    query = "SELECT DISTINCT "+columns[0]+" AS keyword, "+columns[1]+" AS url from "+table+" WHERE "+columns[2]+"=1 ;"
    try:
        cur.execute(query)
    except BaseException:
        print('ERROR! The TABLE name of keywords is not correctly set.')
        print(sys.exc_info()[1])
        keyword_urls = []
        return keyword_urls

    print('---Keywords and urls---')
    for item in cur.fetchall():
        keyword = item[0]
        url = item[1]
        print("{0:<20s} : {1}".format(item[0], item[1]))
        keyword_urls.append(word_url(keyword, "<a href=" + url + " jplinker=True>" + keyword + "</a>"))

    keyword_urls.sort(key=lambda s: len(s.word), reverse=True)
    print('----------')

    return keyword_urls


def fetch_target(dbcursor, database):
    print('fetching targets...')
    cur = dbcursor
    target_paths = []
    cur = dbcursor
    table = settings.DATABASES[database]['TABLES']['TARGET']['NAME']
    columns = settings.DATABASES[database]['TABLES']['TARGET']['COLUMNS']

    query = "SELECT DISTINCT " + columns[0] + " AS path from " + table + " WHERE " + columns[1] + "=1 ;"
    try:
        cur.execute(query)
    except BaseException:
        print('ERROR! The TABLE name of target file path is not correctly set.')
        print(sys.exc_info()[1])
        target_paths = []
        return target_paths

    print('---Target---')
    for item in cur.fetchall():
        print(item[0])
        path = item[0]
        target_paths.append(item[0])
    print('----------')

    return target_paths



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
            print('encoing of ', filepath, '\t: ',correct_encoding)
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