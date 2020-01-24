'''
Gets metadata of wikipage per revision.
Saves in csv format per revision.

James Gardner
'''

import requests as rq
import json
import os
from datetime import datetime as dt
import time

'''
    Begin Helper Functions
'''

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

'''
    Begin Bot Login Code.
'''

url = "https://en.wikipedia.org/w/api.php?"

headers = {
    "User-Agent": "BotCarletonComps2020/0.5 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
    "connection": "keep-alive"
    # "Connection": "close"
}

getToken = {
    "action": "query",
    "meta": "tokens",
    "type": "login",
    "format": "json"
}

credentials = ""
with open("credentials.txt", "r", encoding="utf-8") as f:
    credentials = f.read()

credentials = credentials.split()
username = credentials[0]
password = credentials[1]


S = rq.Session()

botLogin = S.get(url=url, params=getToken).json()

token = botLogin['query']['tokens']['logintoken']

login = {
    "action": "login",
    "lgname": username,
    "lgpassword": password,
    "lgtoken": token,
    "format": "json"
}

botLogin = S.post(url=url, data=login).json()

# printJsonTree(botLogin)

# print(botLogin['login']['result'])

'''
    Begin Data Collection Functions
'''

def getRevisions(title, start=None, end=None):
    if (start == None or end == None):
        revisions = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "timestamp|user|userid|comment|ids|size",
            "rvslots": "*",
            "rvlimit": "max",
            "format": "json",
            "continue": "",
            "maxlag": 5
        }

        revs = S.get(url=url, headers=headers, params=revisions).json()
        # printJsonTree(revs)
        revList = revs['query']['pages']['61008894']['revisions']
        allRevs = {}
        for rev in revList:
            allRevs.update(rev)
        # return dictionary or tuple?
        return allRevs
    else:
        # Fails? does not return revision property???
        revisions = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "rvprop": "timestamp|user|userid|comment|ids|size",
            "rvslots": "*",
            "rvlimit": "5",
            "rvstart": start,
            "rvend": end,
            # "rvcontinue": "",
            "format": "json",
            "continue": "",
            "maxlag": 5
        }

        revs = S.get(url=url, headers=headers, params=revisions).json()
        printJsonTree(revs)
        printQueryErrors(revs)
        revList = revs['query']['pages']['61008894']['revisions']
        allRevs = {}
        for rev in revList:
            allRevs.update(rev)
        # return dictionary or tuple?
        return allRevs

def getPageviews(title):
    pageviews = {
        "action": "query",
        "prop": "pageviews",
        "titles": title,
        "format": "json",
        "pvipmetric": "pageviews",
        "pvipcontinue": "",
        "maxlag": 5
    }

    views = S.get(url=url, headers=headers, params=pageviews).json()
    # printJsonTree(views)
    pageList = views['query']['pages']['61008894']['pageviews']
    allViews = {}
    allViews.update(pageList)
    # dictionary or tuple pairs? Which is better?
    return allViews

def getDeletedRevisions(title, start, end):
    revisions = {
        "action": "query",
        "prop": "deletedrevisions",
        "titles": title,
        "drvprop": "timestamp|user|userid|ids|size",
        "drvslots": "*",
        "drvlimit": "max",
        "format": "json",
        "continue": "",
        "maxlag": 5,
        "drvstart": start,
        "drvend": end
    }

    revs = S.get(url=url, headers=headers, params=revisions).json()
    # printQueryErrors(revs)
    # printJsonTree(revs)
    # print(revs['limits'])
    revList = revs['query']['pages']['61008894']['deletedrevisions']
    allRevs = {}
    for rev in revList:
        allRevs.update(rev)
    # return dictionary or tuple?
    return allRevs




# Will be list of titles? Or page IDs?
title = "2019–20_Hong_Kong_protests"
# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2019-12-31", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2020-01-20", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# Fails to properly grab all data based on date?
rev = getRevisions(title, startDate, endDate)
