#-*- coding : utf-8 -*-

"""
linker.py
---
Core of jp-linker.py
"""

import sys
import re
import argparse
import six
import codecs

import data_io
from data_io import word_url

# --- get default setting from 'settings.py'
from settings import default_set

def read_argument():
    parser = argparse.ArgumentParser(description='Make links of keywords in html.')
    parser.add_argument('--databasesystem', '-dbs', default=default_set['DATABASESYSTEM'],
                        help='Set database system')
    parser.add_argument('--database', '-db', default=default_set['DATABASE'],
                        help='Set database')
    parser.add_argument('--csv', nargs=2,
                        help='Use .csv instead of Database. To use this option, you should set two file paths.')
    parser.add_argument('--test', action='store_true', default=False,
                        help='Run this program in test mode')
    args = parser.parse_args()

    if args.test:
        print('---TEST MODE---')
        return args

    if args.csv != None:
        print('---CSV MODE---')
        print('# CSV KEYWORD LIST : {}'.format(args.csv[0]))
        print('# CSV TARGET LIST  : {}'.format(args.csv[1]))
        return args

    print('# DATABASE SYSTEM: {}'.format(args.databasesystem))
    print('# DATABASE: {}'.format(args.database))


    print('')
    return args


def preprocess(target, offset):
    #--- refresh the output of last time
    tmp = target
    pattern = re.compile("<(.*?)jplinker=True>(.*?)<(.*?)>")
    tmp = re.sub(pattern, '\\2', tmp)

    user_words = []

    #--- user tags
    pattern = re.compile("<a (.*?)href=(.*?)>(.*?)</a>")
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

    processed = tmp
    return processed


if __name__=='__main__':
    # --- Read Arguments from command line.
    args = read_argument()

    # --- Get data from database (or CSV).
    if args.test:
         (keyword_urls, target_paths) = data_io.test_set()

    elif args.csv != None:
        # --- CSV mode ---
        (keyword_urls, target_paths) = data_io.read_csv(args.csv[0], args.csv[1])

    else:
        # --- normal mode ---
        cur = data_io.set_dbcursor(args.databasesystem, args.database)
        keyword_urls = data_io.fetch_keyword(cur, args.database)
        target_paths = data_io.fetch_target(cur, args.database)


    if len(keyword_urls) == 0 :
        print('ERROR! There is no keywords!')
        sys.exit(-1)

    if len(target_paths) == 0 :
        print('ERROR! There is no targets!')
        sys.exit(-1)


    for target_path in target_paths:
        target_html = codecs.open(target_path, 'r', "utf-8")
        # do process in for loop.
        target_string=target_html.read()
        offset = len(keyword_urls)

        (preprocessed_string, user_words) = preprocess(target_string, offset)
        processed_string = process(preprocessed_string, keyword_urls, user_words)

        print(target_path, 'is processed.')

        f = open((target_path + '.processed'), 'w')
        f.write(processed_string)
        f.close()
