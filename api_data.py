'''
Gets data of page as html file from start date until creation date.

James Gardner
'''

import requests as rq
import json


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
        errors = requestObject['error']
        error = True
        print("ERRORS FROM API! READ MESSAGE TO RESOLVE!")
        print("*"*80)
        for key in errors.keys():
            print("KEY: " + str(key) + "\n")
            print(requestObject['error'][key])
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

url = "https://en.wikipedia.org/w/api.php?"
headers = {
    "User-Agent": "CarletonComps2020/0.1 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
    "Connection": "close"
}

title = "2019–20_Hong_Kong_protests"

# as of 03:29am January 20, 2020
original = 936645906

# params = {
#     "action": "parse",
#     "page": "2019-20 Hong Kong protests",
#     "format": "json"
# }


# /w/api.php?action=query&format=json&prop=revisions&list=allrevisions
# &rawcontinue=1&revids=936645906&rvprop=ids%7Ctimestamp%7Cflags%7Ccomment%7Cuser&rvslots=*
# &rvlimit=5&rvendid=936645906&arvprop=ids%7Ctimestamp%7Cflags%7Ccomment%7Cuser&arvslots=*&arvlimit=5

# params = {
#     "action": "query",
#     "format": "json",
#     "prop": "revisions",
#     # "list": "allrevisions",
#     "rawcontinue": 1,
#     "titles": "2019–20_Hong_Kong_protests",
#     "rvend": "2020-01-20T14:56:00Z",
#     "rvprop": "timestamp|flags|comment|user|content|ids",
#     "rvslots": "*",
#     "rvlimit": 50,
#     # "rvendid": original,
#     # "arvprop": "ids|timestamp|flags|comment|user|content|ids",
#     # "arvslots": "*"
# }

#action=query
# &prop=revisions
# &titles=Stack%20Overflow
# &rvlimit=1
# &rvprop=content
# &rvdir=newer
# &rvstart=2016-12-20T00:00:00Z


# https://stackoverflow.com/questions/7136343/wikipedia-api-how-to-get-the-number-of-revisions-of-a-page
params = { 'action': 'query',
           'format': 'json',
           'continue': '',
           'titles': title,
           'prop': 'revisions',
           'rvprop': 'ids',
           'rvlimit': 'max'}




# printQueryErrors(data)
# printJsonTree(data)

# print(data['query']['pages']['61008894']['revisions'][0]['revid'])

# print(data['continue']['rvcontinue'])
# print(data['continue']['continue'])

numRev = 0

done = False
while (not done):
    data = rq.get(url=url, params=params, headers=headers).json()

    for id in data['query']['pages']:
        numRev += len(data['query']['pages'][id]['revisions'])

    if ('continue') in data:
        params['continue'] = data['continue']['continue']
        params['rvcontinue'] = data['continue']['rvcontinue']
    else:
        done = True

print("NUMBER OF REVISIONS: " + str(numRev))