'''
Compare two pages from IDs using MediaWiki API

James Gardner
'''

import json
import requests as rq


# helper function to visualize json file -- best for small examples

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

# https://www.mediawiki.org/wiki/API:Compare
# Compare two revisions

url = "https://en.wikipedia.org/w/api.php?"
headers = {
    "User-Agent": "CarletonComps2020/0.1 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
    "Connection": "close"
}

original = 936093302
update = 935980605

params = {
    "action": "compare",
    "fromrev": original,
    "torev": update,
    "format": "json"
}

data = rq.get(url=url, headers=headers, params=params).json()

# errors = data['error']
# for key in errors.keys():
#     print("KEY: " + str(key) + "\n")
#     print(data['error'][key])
#     print("")


printJsonTree(data)
print(data['compare']['*'])