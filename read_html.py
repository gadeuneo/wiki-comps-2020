'''
HTML parser for MediaWiki API results.

James Gardner
'''

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import re

with open("Hong_Kong.html", "r", encoding="utf-8") as f:
    page = f.read()

# with open("Hong_Kong.html", "r", encoding="utf-8") as ff:
#     i = 0
#     for line in ff:
#         if i > 5:
#             break
#         else:
#             print(line)
#         i+=1

# HTMLParser is more manual, can make custom classes
# More learning curve, but more flexibility

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        print("Encountered an end tag :", tag)

    def handle_data(self, data):
        print("Encountered some data  :", data)

parser = MyHTMLParser()
# parser.feed(page)

# BeautifulSoup has more documentation and methods for extracting data
# Looks to be more restriced on methods, doensn't look like you can make
# custom ones.

soup = BeautifulSoup(page, 'html.parser')
# print(soup.prettify())
text = soup.get_text()
# print(text)

# Finds all occurances of 'Hong' in text
# print(re.findall("Hong", text))

# Finds all indices of 'Hong Kong' in text
# print([m.start() for m in re.finditer('Hong Kong', text)])

