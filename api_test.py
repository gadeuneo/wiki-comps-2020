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

# request headers
# https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Request_fields
# https://meta.wikimedia.org/wiki/User-Agent_policy
# EX: User-Agent: CoolToolName/0.0 (https://example.org/CoolTool/; CoolTool@example.org) UsedBaseLibrary/0.0
# Generic format: <client name>/<version> (<contact information>) <library/framework name>/<version> [<library name>/<version> ...]
headers = {
    'User-Agent': 'CarletonComps2020/0.1 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14'
}


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

# Can either be the url itself or use the requests package to separate params
# in a dictionary. Preferred is requests package parameter as dictionary.

# returns errors; -- see below for comments
query = "format=json&action=query&titles=Batman&prop=revisions&rvprop=content"
params = {
    "action": "query",
    "prop": "revisions",
    "titles": "Batman",
    "rvprop": "timestamp|user|comment|content",
    "rvslots": "*",
    "format": "json"
}


result = rq.get(baseEng+query, headers=headers).json()
r = rq.get(url=baseEng, params=params, headers=headers).json()

printJsonTree(result)
printJsonTree(r)
printJsonTree(badr)

# Note that there should be no warnings or errors in the JSON tree if the query
# was sucessful. However, if they appear in the leftmost column, use the below
# code to help read the error messages and resolve them.

def printQueryErrors(requestObject):
    warn = False
    error = False
    try:
        warnings = requestObject['warnings']
        warn = True
        print("WARNINGS FROM API! READ MESSAGE TO RESOLVE!")
        print("*"*80)
        for key in warnings.keys():
            print("KEY: " + str(key) + "\n")
            for id in requestObject['warnings'][key].keys():
                print(requestObject['warnings'][key][id])
            print("")
    except:
        pass

    try:
        errors = requestObject['errors']
        error = True
        print("ERRORS FROM API! READ MESSAGE TO RESOLVE!")
        print("*"*80)
        for key in errors.keys():
            print("KEY: " + str(key) + "\n")
            print("KEY: " + str(key) + "\n")
            for id in requestObject['errors'][key].keys():
                print(requestObject['errors'][key][id])
            print("")
    except:
        pass

    if (warn and error):
        print("*"*80)
        print("WARNINGS AND ERRORS IN QUERY! READ MESSAGE TO RESOLVE!")
    elif (warn and not error):
        print("*"*80)
        print("WARNINGS IN QUERY! READ MESSAGE TO RESOLVE!")
    elif (not warn and error):
        print("*"*80)
        print("ERRORS IN QUERY! READ MESSAGE TO RESOLVE!")
    else:
        print("*"*80)
        print("QUERY SUCESSFUL!")

printQueryErrors(result)
printQueryErrors(r)