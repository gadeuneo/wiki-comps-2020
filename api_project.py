'''
Gets metadata of wikipage per revision.
Saves in csv format per revision.

James Gardner
'''

import requests as rq
import json
import os
import sys
from datetime import datetime as dt
import time
import pandas as pd

start = time.time()

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

def hasError(requestObject):
    warn = False
    error = False
    try:
        warnings = requestObject['warnings']
        warn = True
    except:
        pass

    try:
        errors = requestObject['error']
        error = True
    except:
        pass

    if (warn or error):
        return True
    else:
        return False
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

def getRevisions(pageid, start=None, end=None):
    if (start == None or end == None):
        print("ERROR, need start and end date!")
        sys.exit(1)
    else:
        revisions = {
            "action": "query",
            "prop": "revisions",
            # "titles": title,
            "pageids": pageid,
            "rvprop": "timestamp|user|userid|ids|size",
            "rvslots": "*",
            "rvlimit": "max",
            "rvstart": start,
            "rvend": end,
            "rvdir": "newer",
            # "rvcontinue": "",
            "format": "json",
            "continue": "",
            "formatversion": 2,
            "maxlag": 5
        }
        done = False
        allRevs = []
        while (not done):
            revs = S.get(url=url, headers=headers, params=revisions).json()
            # pageid = list(revs['query']['pages'].keys())[0]
            # revList = revs['query']['pages'][pageid]['revisions']
            revList = revs['query']['pages'][0]['revisions']
            for rev in revList:
                allRevs.append(rev)
            
            if ("continue" in revs):
                revisions['continue'] = revs['continue']['continue']
                revisions['rvcontinue'] = revs['continue']['rvcontinue']
            else:
                done = True

        return allRevs

def getPageviews(pageid):
    pageviews = {
        "action": "query",
        "prop": "pageviews",
        # "titles": title,
        "pageids": pageid,
        "format": "json",
        "pvipmetric": "pageviews",
        "pvipcontinue": "",
        "maxlag": 5
    }
    
    done = False
    views = S.get(url=url, headers=headers, params=pageviews).json()
    printJsonTree(views)
    pageList = views['query']['pages'][pageid]['pageviews']
    allViews = {}
    allViews.update(pageList)
    return allViews

def getPageId(title):
    page = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "format": "json"
        }
    
    data = S.get(url=url, headers=headers, params=page).json()
    if (hasError(data)):
        print("TITLE NOT FOUND! PLEASE CHECK TITLE SPELLING!")
        sys.exit(1)
    pageid = list(data['query']['pages'].keys())[0]
    return pageid


# Subject to change as script needs
title = "2019–20 Hong Kong protests"
# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2019-06-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# returns list of dictionaries
protests = getRevisions(getPageId(title), start=startDate, end=endDate)

# print(len(protests))

# handle userhidden ....
'''
IGNORE CODE BELOW!!!!
'''

# https://www.geeksforgeeks.org/create-a-pandas-dataframe-from-list-of-dicts/
# https://stackoverflow.com/questions/34183004/how-to-write-a-dictionary-to-excel-in-python

# THIS WORKS!!!!
# df = pd.DataFrame(protests)
# df.to_csv("test.csv")

master = {
    "revid": [],
    "timestamp": [],
    "user": [],
    "userid": [],
    "size": []
}


for d in protests:
    try:
        master['revid'].append(d['revid'])
        master['timestamp'].append(d['timestamp'])
        master['user'].append(d['user'])
        master['userid'].append(d['userid'])
        master['size'].append(d['size'])
    except:
        print(d)
    # for key in master.keys():
    #     try:
    #         master[key].append(d[key])
    #     except:
    #         print(d)


# Should be same size; if not there's missing data that should have
# printed from the try-except block above.
# print(len(master['revid']))
# print(len(master['timestamp']))
# print(len(master['user']))
# print(len(master['userid']))
# print(len(master['size']))
# print(len(master['comment']))

'''
END CODE TO IGNORE!!!
'''


# exits program to prevent creating files for now...
sys.exit(0)

path = "data"
if (not os.path.exists(path)):
    os.mkdir(path)

title = title.replace(" ", "_")
title += ".csv"

if (os.path.isfile(os.path.join(path, title))):
    print("ERROR! FILE ALREADY EXISTS! ABORTING ACTION TO PREVENT \
        FILE OVERWRITE!")
    sys.exit(1)

with open(os.path.join(path, title), "w", encoding="utf-8") as f:
    f.write("revid, timestamp, user, userid, size\n")
    for i in range(len(master['user'])):
        f.write(str(master['revid'][i]) + "," + str(master['timestamp'][i]) + "," \
            + str(master['user'][i]).replace(",", "") + "," + str(master['userid'][i]) + "," \
                + str(master['size'][i]) + "\n") 

# with open(os.path.join(path, title+".csv"), "r", encoding="utf-8") as f:
#     csv = f.read()

end = time.time()

print("Time Elapsed: " + str(end-start))