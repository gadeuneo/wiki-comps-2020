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
    "User-Agent": "BotCarletonComps2020/0.8 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
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
    End Bot Login Code
'''


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
            # "rvlimit": 5,
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
        # TODO fix limits
        while (not done):
            revs = S.get(url=url, headers=headers, params=revisions).json()
            if (hasError(revs)):
                print("Query Error! Exiting program!")
                sys.exit(1)
            # printJsonTree(revs)
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
    
    # TODO fix issues with getting pageviews OR find another metric
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
        print("Query Error! Exiting program!")
        sys.exit(1)
    if (int(list(data['query']['pages'].keys())[0]) == -1):
        print("TITLE: {0} NOT FOUND! PLEASE CHECK TITLE SPELLING!".format(title))
        sys.exit(1)
    pageid = list(data['query']['pages'].keys())[0]
    return pageid

def getRedirects(pageid):
    redirects = {
        "action": "query",
        "prop": "redirects",
        "pageids": pageid,
        "format": "json",
        "rdlimit": 500,
        "continue": ""
    }
    done = False
    allReds = []
    while (not done):
        reds = S.get(url=url, headers=headers, params=redirects).json()
        if (hasError(reds)):
            print("Query Error! Exiting program!")
            sys.exit(1)
        redList = reds['query']['pages'][pageid]['redirects']
        for red in redList:
            allReds.append(red)
        
        if ("continue" in reds):
                revisions['continue'] = reds['continue']['continue']
                revisions['rdcontinue'] = reds['continue']['rdcontinue']
        else:
            done = True

    return allReds
        

'''
    End Data Collection Functions
'''

'''
    Begin Data Collection
'''

# Subject to change as script needs

titles = [
    "2019-20 Hong Kong protests",
    "Hong Kong",
    "2019 Hong Kong extradiction bill",
    "Government of Hong Kong",
    "Murder of Poon Hiu-wing",
    "One country, two systems",
    "Demosisto",
    "Hong Kong 1 July marches",
    "Civil Human Rights Front",
    "Hong Kong Human Rights and Democracy Act",
    "Chinese University of Hong Kong conflict",
    "Death of Chow Tsz-lok",
    "Siege of the Hong Kong Polytechnic University",
    "2019 Yuen Long attack",
    "Hong Kong-Mainland China conflict",
    "Storming of the Legislative Council Complex",
    "Hong Kong Way",
    "2019 Prince Edward station attack",
    "Death of Chan Yin-lan",
    "2019 Hong Kong local elections",
    "List of protests in Hong Kong",
    "Police misconduct allegations during the 2019-20 Hong Kong protests",
    "Art of the 2019-20 Hong Kong protests",
    "12 June 2019 Hong Kong protest",
    "Umbrella Movement",
    "Causes of the 2019-20 Hong Kong protests",
    "Tactics and methods surrounding the 2019-20 Hong Kong protests",
    "Carrie Lam",
    "Reactions to the 2019-20 Hong Kong protests",
    "List of early 2019 Hong Kong protests",
    "List of July 2019 Hong Kong protests",
    "List of August 2019 Hong Kong protests",
    "List of September 2019 Hong Kong protests",
    "List of October 2019 Hong Kong protests",
    "List of November 2019 Hong Kong protests",
    "List of December 2019 Hong Kong protests",
    "List of Janurary 2020 Hong Kong protests",
    "Glory to Hong Kong",
    "Lennon Wall (Hong Kong)",
    "HKmap.live",
    "Killing of Luo Changquig"
]

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
# redirects = getRedirects(getPageId(title))
# sys.exit(0)
# Skip pageviews for now...
# views = getPageviews(getPageId(title))

end = time.time()
print("Time Elapsed: " + str(end-start))


# exits program to prevent creating files for now...
sys.exit(0)

path = "data"
if (not os.path.exists(path)):
    os.mkdir(path)

# adds talk pages
for i in range(len(titles)):
    titles.append("Talk:" + titles[i])


####### TESTING UNSTABLE CODE AHEAD!!! #####
data = getRevisions(getPageId(titles[0]), start=startDate, end=endDate)
# redirects = getRedirects(getPageId(titles[0]))
name = titles[0].copy()
name = name.replace(" ", "_")
name = name.replace(".", "(dot)")
name = name.replace(":", "(colon)")
name += ".csv"
if (not os.path.isfile(os.path.join(path, name))):
    dfData = pd.DataFrame(data)
    dfRed = pd.DataFrame(redirects)
    dfData.to_csv(os.path.join(path, "Data" + name))
    # dfRed.to_csv(os.path.join(path, "Redirects" + name))




for title in titles:
    data = getRevisions(getPageId(title), start=startDate, end=endDate)
    redirects = getRedirects(getPageId(title))

    name = title.copy()
    name = name.replace(" ", "_")
    name = name.replace(".", "(dot)")
    name = name.replace(":", "(colon)")
    name += ".csv"
    if (not os.path.isfile(os.path.join(path, name))):
        dfData = pd.DataFrame(data)
        dfRed = pd.DataFrame(redirects)
        dfData.to_csv(os.path.join(path, "Data" + name))
        dfRed.to_csv(os.path.join(path, "Redirects" + name))
    
end = time.time()
print("Time Elapsed: " + str(end-start))

