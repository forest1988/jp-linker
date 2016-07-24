from bs4 import BeautifulSoup as BS
from bs4.element import NavigableString, Comment
import re
import codecs

# html = "<html><body>無脊椎動物プラットフォームは<h1>無脊椎動物のプラットフォームです。</h1>無脊椎動物プラットフォームはいいぞ。</body></html>"
# print(html)
soup = BS(codecs.open("sample/sample.html", 'r', "utf-8"), "html.parser")
# soup = BS(html, "html.parser")
for tag in soup.findAll(True):
#    for text in tag.findAll(text=True):
#        if isinstance(text.string, NavigableString):
#            print(text.parent.name)
#            print(text)
    if tag.name not in ["html", "link", "a", "script", "noscript", "title", "meta"]:
#        if isinstance(tag.string, NavigableString):
#        print("========== " + tag.name + " ==========")
#        print(tag.string)
        for text in tag.findAll(text=True, recursive=False):
            if isinstance(text, NavigableString) and not isinstance(text, Comment):
                repstr = re.sub("カイコガ", '%999%', text.string)
                text.string.replaceWith(repstr)

result = re.sub('%999%', '<a href="https://en.wikipedia.org/wiki/Bombyx_mori">カイコガ</a>', soup.prettify())
print(result)
