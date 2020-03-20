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

def get_creation_date(S, url, headers, pageid):
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

def create_creation_dates_CSV(session, url, headers, titles):

    start_time = time.time()

    # Why is it formatted this way? - Jackie
    dates = [["Titles", "Page Creation Date"]]

    bad_creation = False

    # finding and appending all creation dates in the titles list
    for i in range(len(titles)):
        page_id = getPageId(session, url, headers, titles[i])

        try:
            creation_date = get_creation_date(session, url, headers, page_id)
            dates.append([titles[i],creation_date])
        except:
            print("Page Creation Date not found for {0}".format(titles[i]))
            print(page_id)
            bad_creation = True
    
    # sanity checking the dates
    if ((len(dates) - 1) != len(titles) or bad_creation):
        print("Error with collecting page creation dates. Nothing was changed.")
        return

    creation_date_directory = "creation"
    CSV_file_name = "creation_dates.csv"
    CSV_location = os.path.join(creation_date_directory, CSV_file_name)

    # convert dates into a CSV file
    if (not os.path.isfile(CSV_location)):
        df_dates = pd.DataFrame(dates[1:], columns=dates[0])
        df_dates.to_csv(CSV_location, encoding="utf-8")

    # make changes to already created CSV file
    else:
        creation_csv = pd.read_csv(CSV_location)

        for i in range(len(titles)):
            if (titles[i] not in creation_csv['Titles']):
                creation_csv.append(dates[i], ignore_index=True)
        
        creation_csv.to_csv(CSV_location, encoding="utf-8")

    # print the time it took
    end_time = time.time()
    print("Page creation dates took {0} seconds."
        .format(str(end_time - start_time)))
    
    return

'''
    End Data Collection Functions
'''

'''
    Begin Data Collection
'''
def main():

    S = rq.Session()

    url = "https://en.wikipedia.org/w/api.php?"

    headers = {
        "User-Agent": "BotCarletonComps2020/0.8 \
            (http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php) \
            Python/3.6.9 Requests/2.18.14",
        "connection": "keep-alive"
        # "Connection": "close"
    }

    login(S, url, headers)

    endLogin = time.time()
    print("Login took {0} seconds".format(str(endLogin - start)))

    # To change included titles, go to titles.txt
    titles = get_titles()

    # Simple assertions about the time
    time_sanity_check()

    # Create is going to be deprecated
    directories = ["10years", "creation"]

    create_directories(directories)

    titles_plus_talk = add_talk_pages(titles)

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=

    files = [format_file_names(title) for title in titles_plus_talk]

    create_creation_dates_CSV(S, url, headers, titles)

    # save data and redirects
    # for i in range(len(titles)):
    #     badData = False
    #     badRedirect = False
    #     try:
    #         data = getRevisions(S, url, headers, getPageId(S, url, headers, titles[i]), start=startDate, end=endDate)
    #     except:
    #         print("Data not found for {0}".format(titles[i]))
    #         print(getPageId(S, url, headers, titles[i]))
    #         badData = True
    #     try:
    #         redirects = getRedirects(S, url, headers, getPageId(S, url, headers, titles[i]))
    #     except:
    #         print("Redirects not found for {0}".format(titles[i]))
    #         print(getPageId(S, url, headers, titles[i]))
    #         badRedirect = True
    #     # TODO: modify path variable
    #     path = "10years"

    #     if (not badData):
    #         if (not (os.path.isfile(os.path.join(path, "Data" + files[i])))):
    #             dfData = pd.DataFrame(data)
    #             dfData.to_csv(os.path.join(path, "Data" + files[i]), encoding="utf-8")
    #     if (not badRedirect):
    #         if (not (os.path.isfile(os.path.join(path, "Redirects" + files[i])))):
    #             dfRed = pd.DataFrame(redirects)
    #             dfRed.to_csv(os.path.join(path, "Redirects" + files[i]), encoding="utf-8")

    '''
        End Data Collection
    '''

    # print("Data collection took {0} seconds".format(str(end - endCreate)))

    end = time.time()
    print("Time Elapsed: " + str(end - start))

if __name__ == "__main__":
    main()
