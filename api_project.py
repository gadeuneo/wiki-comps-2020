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
            "rvprop": "timestamp|user|userid|ids|size|comment",
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

# def getDeletedRevisions(pageid, start=None, end=None):
#     if (start == None or end == None):
#         print("Start and End date required!")
#         sys.exit(1)
#     else:
#         revisions = {
#             "action": "query",
#             "prop": "deletedrevisions",
#             # "titles": title,
#             "pageids": pageid,
#             "drvprop": "timestamp|user|userid|ids|size|comment",
#             "drvslots": "*",
#             "drvlimit": "max",
#             "format": "json",
#             "continue": "",
#             "maxlag": 5,
#             "drvstart": start,
#             "drvend": end,
#             "drvdir": "newer",
#             "formatversion": 2,
#             "maxlag": 5
#         }

#         done = False
#         allRevs = []
#         while (not done):
#             revs = S.get(url=url, headers=headers, params=revisions).json()
#             # Permission error????
#             # printQueryErrors(revs)
#             revList = revs['query']['pages'][0]['deletedrevisions']
#             for rev in revList:
#                 allRevs.append(rev)
            
#             if ("continue" in revs):
#                 revisions['continue'] = revs['continue']['continue']
#                 revisions['rvcontinue'] = revs['continue']['rvcontinue']
#             else:
#                 done = True
    
#         return allRevs

def getPageId(title):
    page = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "format": "json"
        }
    
    data = S.get(url=url, headers=headers, params=page).json()
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


master = {
    "revid": [],
    "timestamp": [],
    "user": [],
    "userid": [],
    "size": [],
    "comment": []
}
print(len(protests))

print(protests[0]['revid'])

for d in protests:
    for key in master.keys():
        try:
            master[key].append(d[key])
        except:
            print(d)


# exits program to prevent creating files for now...
sys.exit(0)

try:
    os.mkdir(title)
    path = title
except:
    print("DIRECTORY ALREADY EXISTS!")
    # safety to avoid overwriting existing files
    sys.exit(1)

# with open("test.csv", "w", encoding="utf-8") as f:
#     f.write("revid\n")
#     for id in master['revid']:
#         f.write(str(id)+"\n")

with open(os.path.join(path, title+".csv"), "w", encoding="utf-8") as f:
    f.write("revid, timestamp, user, userid, size, comment\n")
    for i in range(len(master['comment'])):
        f.write(str(master['revid'][i]) + "," + str(master['timestamp'][i]) + "," \
            + str(master['user'][i]) + "," + str(master['userid'][i]) + "," \
                + str(master['size'][i]) + "," + str(master['comment'][i]) + "\n")


with open(os.path.join(path, title+".csv"), "r", encoding="utf-8") as f:
    csv = f.read()

end = time.time()

print("Time Elapsed: " + str(end-start))