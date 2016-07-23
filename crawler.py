# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup as BS
import mechanize
import datetime
import sys
import re
import ast
import mysql.connector
import config

# --- Set Encoding ---
reload(sys)
sys.setdefaultencoding("utf-8")

# --- Connect to mySQL ---
## You should make "config.py" to set database name and so on.
dbcon = mysql.connector.connect(
    database=config.database,
    user=config.user,
    password=config.password,
    host=config.host
)
dbcur = dbcon.cursor()

try:
    dbcur.execute(
        'CREATE TABLE ivbpfdictionary (url VARCHAR(255) UNIQUE, html TEXT, title VARCHAR(255), text TEXT, date DATETIME, authors VARCHAR(255), channels VARCHAR(255));')
    dbcon.commit()
except:
    print "There already is the table!"

# --- Compile Pattern ---
pattern = re.compile('\{.+?\}')

# --- Get Date Time ---
now = datetime.datetime.now()
### With more precision, we should consider a time difference.


# --- Set First URL ---
print "This is the code for Crawling 'TECHCRUNCH'"
url = 'http://techcrunch.com/'

b = mechanize.Browser()
b.open(url)

# --- Click Stream by "mechanize" ---

#
# URL sample : http://techcrunch.com/2015/05/26/tc-cribs-lumositys-brilliant-soma-office/
#              http://techcrunch.com/2015/05/26/workday-falls-5-despite-beating-market-expectations-in-its-fq1/
#
# each page has "Next Story" button.
# sample : <a href="http://techcrunch.com/2015/05/27/mapsense/" class="next-link" data-omni-sm="art_nextstory">
#
# In the top page, - class="river-block" - means the latest news class
#
# var sranalytics = {"version":"0.1.4","pid":"518833fa642b2405ba000008","iframe":"0","title":"Airware Launches Fund To Catalyze The Rest Of The Commercial Drone Equation","url":"http:\/\/techcrunch.com\/2015\/05\/27\/drone-fund\/","date":"2015-05-27 13:01:39","channels":["tc"],"tags":[],"authors":["Josh Constine"]};
#


html = b.response().read()

soup = BS(html)

'''
for link in soup.find_all('li', {"class":"river-block"}):
    print(link.get('data-permalink'))
'''

# try:
# latest_url = soup.find('li', {"class":"river-block"}).get('data-permalink')
# except:
latest_url = soup.find_all('a', {"data-omni-sm": "gbl_river_headline,1"})[0].get('href')
print latest_url

print "Latest News : " + latest_url

tmpurl = latest_url

while True:
    b.open(tmpurl)
    tmphtml = b.response().read()
    soup = BS(tmphtml)

    # --- GET SRANALYTICS ---
    sranalytics = soup.find(text=re.compile("var sranalytics"))
    match = pattern.search(sranalytics)
    d = ast.literal_eval(match.group())
    # print d

    article_datetime = datetime.datetime.strptime(d['date'], '%Y-%m-%d %H:%M:%S')
    # print article_datetime
    # print now - datetime.timedelta(days=7)
    if article_datetime < now - datetime.timedelta(days=7):
        print "One Weeks Ago!"
        break

    # --- URL ---
    print "<URL>"
    print tmpurl

    # --- HTML ---
    # print tmphtml

    # --- TITLE ---
    print "<TITLE>"
    print d['title']

    # --- MAIN TEXT ---
    print "<MAIN TEXT>"
    # <div class="article-entry text">
    main_text_asResultSet = soup.find_all('div', {"class": "article-entry text"})
    main_text_asString = unicode.join(u'\n', map(unicode, main_text_asResultSet))
    tmpsoup = BS(main_text_asString)
    main_text_asResultSet = tmpsoup.find_all('p')
    main_text_asString = unicode.join(u'\n', map(unicode, main_text_asResultSet))
    tmpsoup = BS(main_text_asString)
    # print tmpsoup.get_text()

    # --- DATE TIME ---
    print "<DATE TIME>"
    print d['date']

    # --- AUTHORS ---
    print "<AUTHORS>"
    print d['authors']

    # --- CHANNELS ---
    print "<CHANNELS>"
    print d['channels']

    # --- NEXT ---
    for next_link in soup.find_all('a', {"class": "next-link"}):
        next_url = next_link.get('href')
        print "<NEXT>"
        print next_url

    tmpurl = next_url

    INSERT_EXEC = ("INSERT IGNORE INTO techchrunch "
                   "(url, html, title, text, date, authors, channels) "
                   "VALUES (%s, %s, %s, %s, %s, %s, %s)")
    INPUT_DATA = (
    tmpurl, tmphtml, d['title'], tmpsoup.get_text(), d['date'], ','.join(d['authors']), ','.join(d['channels']))
    dbcur.execute(INSERT_EXEC, INPUT_DATA)
    dbcon.commit()
