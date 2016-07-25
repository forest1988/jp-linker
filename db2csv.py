#-*- coding : utf-8 -*-

"""
db2csv.py
---
Read database data and save to csv.
"""

import re
import argparse
import six
import codecs

import data_io
from data_io import word_url

# --- get default setting from 'settings.py'
from settings import default_set

def read_argument():
    parser = argparse.ArgumentParser(description='Read keywords from database and write it to csv.')
    parser.add_argument('--databasesystem', '-dbs', default=default_set['DATABASESYSTEM'],
                        help='Set database system')
    parser.add_argument('--database', '-db', default=default_set['DATABASE'],
                        help='Set database')
    parser.add_argument('--csv', default='./sample/test.csv',
                        help='output csv file')
    args = parser.parse_args()

    print('# DATABASE SYSTEM: {}'.format(args.databasesystem))
    print('# DATABASE: {}'.format(args.database))
    print('# CSV: {}'.format(args.csv))

    print('')
    return args


def database_to_csv(dbcursor, table):
    cur = dbcursor

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
            keyword_urls.append(word_url(keyword, "<a href=" + url + " jplinker=True>" + keyword + "</a>"))


if __name__=='__main__':
    args = read_argument()

    cur = data_io.set_dbcursor(args.databasesystem, args.database)
    keyword_urls = data_io.fetch_keyword(cur, args.database)
    target_paths = data_io.fetch_html(cur, args.database)

    # for debug
    target_paths = ['./sample/sample.html', './sample/test.html']

