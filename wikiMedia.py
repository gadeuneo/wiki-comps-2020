'''
Example uses of WikiMedia API queries.
James Gardner
'''


def printJsonTree(d, indent=0):
    """Print tree of keys in JSON object.
    
    Prints the different levels of nested keys in a JSON object. When there
    are no more dictionaries to key into, prints objects type and byte-size.

    Input
    -----
    d : dict
    """
    for key,value in d.items():
        print("\t"*indent + str(key),end=" ")
        if isinstance(value, dict):
            print(); printJsonTree(value, indent+1)
        else:
            print(": " + str(type(d[key])).split("'")[1] + " - " + str(len(str(d[key]))))
            
# Example
import requests as rq
data = rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content").json()
printJsonTree(data)

import json
sample = rq.get("https://en.wikipedia.org/w/api.php?format=json&action=query&titles=Batman&prop=revisions&rvprop=content").json()
with open("batman.txt","w", encoding='utf8') as outfile:
    json.dump(sample, outfile)


import re


# re.findall(r"\d{4}\)", re.findall(r"debut.+?\n", lines)[0])[0][:-1]

# \d{4} is matches a digit exactly 4 in length, \D matches non-digit
# . is matches any character EXCEPT newline (\n)
# ? matches the preceding pattern element zero or one time, UNLESS:
    #Modifies the *, +, ? or {M,N}'d regex that comes before to match as few times as possible.
#\n is Matches what the nth marked subexpression matched, where n is a digit from 1 to 9.

# https://stackoverflow.com/questions/809837/python-regex-for-finding-contents-of-mediawiki-markup-links

