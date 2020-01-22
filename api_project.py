'''
Gets metadata of wikipage per revision.
Saves in csv format per revision.

James Gardner
'''

import requests as rq
import json
import os

def printJsonTree(d, indent=0):
    """Print tree of keys in JSON object.
    
    Prints the different levels of nested keys in a JSON object. When there
    are no more dictionaries to key into, prints objects type and byte-size.
    Also iterates through lists of dictionaries.

    Input
    -----
    d : dict
    """
    for key,value in d.items():
        print("\t"*indent + str(key),end=" ")
        if isinstance(value, dict):
            print(); printJsonTree(value, indent+1)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    print(); printJsonTree(item, indent+1)
                else:
                    print(": " + str(type(d[key])).split("'")[1] + " - " + str(len(str(d[key]))))
        else:
            print(": " + str(type(d[key])).split("'")[1] + " - " + str(len(str(d[key]))))

url = "https://en.wikipedia.org/w/api.php?"
headers = {
    "User-Agent": "BotCarletonComps2020/0.5 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
    "Connection": "close"
}
title = "2019–20_Hong_Kong_protests"
# https://stackoverflow.com/questions/7136343/wikipedia-api-how-to-get-the-number-of-revisions-of-a-page
params = { 'action': 'query',
           'format': 'json',
           'continue': '',
           'titles': title,
           'prop': 'revisions',
           'rvprop': 'ids',
           'rvlimit': 'max'}

username = ""
password = ""
credentials = ""

with open("credentials.txt", "r", encoding="utf-8") as f:
    credentials = f.read()

print(credentials)