'''
Wikipedia MediaWiki API User Docs

In depth breakdown of using the MediaWiki API with explanations of examples
that progress in complexity.

Probably over the top documentation, but will try to leave nothing unexplained.

James Gardner
'''

# allows Python to make web requests
import requests as rq
# allows Python to read JSON files (similar to a dictionary)
import json
# allows Python to use regular expressions to search results
import re

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

# base URLs for the MediaWiki and English Wiki -- not sure on difference yet
baseMed = "https://www.mediawiki.org/w/api.php?"
baseEng = "https://en.wikipedia.org/w/api.php?"

# will be using baseEng for now

'''
sample query -- returns contents of Batman Wiki article
Breakdown:
format=json -- returns json format
action=query -- perform a query
titles=Batman -- a list of titles to work on; separate with '|'
prop=revisions -- which properties to get; in this case the revision information
rvprop=content -- what revision property to get; in this case the content
rvslots=* -- which pieces of content to get; * denotes all content
'''
query = "format=json&action=query&titles=Batman&prop=revisions&rvprop=content&rvslots=*"

params = {
    "action": "query",
    "prop": "revisions",
    "titles": "Batman",
    "rvprop": "timestamp|user|comment|content",
    "rvslots": "*",
    "format": "json"
}

result = rq.get(baseEng+query).json()

r = rq.get(url=baseEng, params=params).json()

printJsonTree(result)
printJsonTree(r)


# print(result['warnings']['main'])
# print(result['warnings']['revisions'])