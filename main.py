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

from static_helpers import *

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
def login(S, url, headers):
    url = url
    headers = headers
    getToken = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }

    username, password = get_credentials()

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

def getRevisions(S, url, headers, pageid, start=None, end=None):
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

def getPageviews(S, url, headers, pageid):
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
    # printJsonTree(views)
    pageList = views['query']['pages'][pageid]['pageviews']
    allViews = {}
    allViews.update(pageList)
    return allViews

def getPageId(S, url, headers, title):
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

def getRedirects(S, url, headers, pageid):
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
                redirects['continue'] = reds['continue']['continue']
                redirects['rdcontinue'] = reds['continue']['rdcontinue']
        else:
            done = True

    return allReds

def getCreationDate(S, url, headers, pageid):
    creation = {
        "action": "query",
        "prop": "revisions",
        "pageids": pageid,
        "rvprop": "timestamp",
        # "rvslots": "*",
        "rvlimit": 1,
        # "rvlimit": 5,
        "rvdir": "newer",
        "format": "json",
        "formatversion": 2,
    }
    create = S.get(url=url, headers=headers, params=creation).json()
    if (hasError(create)):
        print("Query Error! Exiting program!")
        sys.exit(1)
    timestamp = create['query']['pages'][0]['revisions'][0]['timestamp']
    return timestamp

def getPageviewsHack(S, url, headers, df):
    ids = df['pageid'].tolist()
    altTitles = df['title'].tolist()
    index = 0
    allViews = dict()
    for pageid in ids:
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
        allViews[altTitles[index]] = dict()
        while (not done):
            views = S.get(url=url, headers=headers, params=pageviews).json()
            # printJsonTree(views)
            pageList = views['query']['pages'][str(pageid)]['pageviews']
            allViews[altTitles[index]].update(pageList)
            # pvipcontinue param doesn't show up at all
            if ("continue" in views):
                views['continue'] = views['continue']['continue']
                views['pvipcontinue'] = views['continue']['pvipcontinue']
            else:
                done = True
        index += 1

    return allViews

'''
    End Data Collection Functions
'''

'''
    Begin Data Collection
'''
def main():

    url = "https://en.wikipedia.org/w/api.php?"

    headers = {
        "User-Agent": "BotCarletonComps2020/0.8 (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) Python/3.6.9 Requests/2.18.14",
        "connection": "keep-alive"
        # "Connection": "close"
    }
    S = rq.Session()

    login(S, url, headers)
    endLogin = time.time()
    print("Login took {0} seconds".format(str(endLogin-start)))

    # To change included titles, go to titles.txt
    titles = get_titles()

    # Convert date to Unix Timestamp
    startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
    endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
    today = int(time.mktime(dt.today().timetuple()))
    # Assertions for proper date args
    assert(startDate <= endDate)
    assert(endDate <= today)

    # Skip pageviews for now...
    # views = getPageviews(getPageId(title))

    # exits program to prevent creating files for now...
    # sys.exit(0)

    # Create is going to be deprecated
    directories = ["10years", "creation"]

    create_directories(directories)

    titles = add_talk_pages(titles)

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=

    # format title to save as file
    files = [title.replace(" ","_").replace(".","(dot)").replace(":", "(colon)") + ".csv" for title in titles]
    dates = [["Title", "Page Creation Date"]]

    endPrep = time.time()
    print("Prep took {0} seconds".format(str(endPrep - endLogin)))

    creation_date_directory = "creation"

    # save page creation dates with titles as csv file
    badCreation = False
    for i in range(len(titles)):
        try:
            creationDate = getCreationDate(S, url, headers, getPageId(S, url, headers, titles[i]))
            dates.append([titles[i], creationDate])
        except:
            print("Page Creation Date not found for {0}".format(titles[i]))
            print(getPageId(titles[i]))
            badCreation = True

    if ((len(dates) -1) != len(files) or badCreation):
        print("Error with collecting page creation dates!")
    elif (not (os.path.isfile(os.path.join(creation_date_directory, "creationDates.csv")))):
        dfDates = pd.DataFrame(dates[1:], columns=dates[0])
        dfDates.to_csv(os.path.join(creation_date_directory, "CreationDates.csv"), encoding="utf-8")

    endCreate = time.time()
    print("Page creation dates took {0} seconds".format(str(endCreate - endPrep)))

    # save data and redirects
    for i in range(len(titles)):
        badData = False
        badRedirect = False
        try:
            data = getRevisions(S, url, headers, getPageId(S, url, headers, titles[i]), start=startDate, end=endDate)
        except:
            print("Data not found for {0}".format(titles[i]))
            print(getPageId(S, url, headers, titles[i]))
            badData = True
        try:
            redirects = getRedirects(S, url, headers, getPageId(S, url, headers, titles[i]))
        except:
            print("Redirects not found for {0}".format(titles[i]))
            print(getPageId(S, url, headers, titles[i]))
            badRedirect = True

        path = "10years"

        if (not badData):
            if (not (os.path.isfile(os.path.join(path, "Data" + files[i])))):
                dfData = pd.DataFrame(data)
                dfData.to_csv(os.path.join(path, "Data" + files[i]), encoding="utf-8")
        if (not badRedirect):
            if (not (os.path.isfile(os.path.join(path, "Redirects" + files[i])))):
                dfRed = pd.DataFrame(redirects)
                dfRed.to_csv(os.path.join(path, "Redirects" + files[i]), encoding="utf-8")


    test = pd.read_csv(os.path.join(path, "Redirects" + files[0]))
    mydates = getPageviewsHack(S, url, headers, test)
    # printJsonTree(mydates)

    '''
        End Data Collection
    '''

    end = time.time()
    print("Data collection took {0} seconds".format(str(end - endCreate)))

    print("Time Elapsed: " + str(end-start))

if __name__ == "__main__":
    main()
