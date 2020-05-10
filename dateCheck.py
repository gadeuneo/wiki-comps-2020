'''
    Sanity check of page creation date to handle page move/rename/redirect.

    Written by James Gardner
'''

import requests as rq
import json
import os
import sys
from datetime import datetime as dt
import time
import pandas as pd

from static_helpers import *



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



def date_sanity_check(S, url, headers):
    path = "10 Year Redirect Data"
    creation = "creation"
    creation_file = "creation_dates.csv"
    creationDf = pd.read_csv(os.path.join(creation, creation_file), index_col=0)
    redirectFiles = os.listdir(path)
    redirectDict = dict()
    for f in redirectFiles:
        redirectDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

    keys = list(redirectDict.keys())
    titleList = creationDf['Titles'].tolist()

    for key in keys:
        df = redirectDict[key]
        pageids = df['pageid']
        dates = []
        for pageid in pageids:
            try:
                d = get_creation_date(S, url, headers, pageid)
                dates.append(d)
            except:
                # Note, this shouldn't happen unless page deleted?
                print("Page Creation Date not found for {0}".format(pageid))
                print(prettyPrint(key))
                print("")
                continue

        dates = [dt.strptime(d[0:d.find('T')], "%Y-%m-%d") for d in dates]
        if len(dates) != 0:
            equal = all(d == dates[0] for d in dates)
            if not equal:
                print("WARNING: DIFFERENT PAGE CREATION DATES!")
                print("For this page: {0}".format(prettyPrint(key)))
                print("Earliest page creation date is {0}".format(min(dates)))
                print("Changing 'creation_dates.csv' to match earliest date!")
                print("")
                if (prettyPrint(key) in titleList):
                    # https://stackoverflow.com/questions/21800169/python-pandas-get-index-of-rows-which-column-matches-certain-value
                    ix = creationDf.index[creationDf['Titles'] == prettyPrint(key)]
                    # Solves https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
                    creationDf.loc[ix, 'Page Creation Date'] = min(dates)

            else:
                print("This page's creation dates are good! {0}".format(prettyPrint(key)))
                print("")
        else:
            print("ERROR! Could not find creation dates for this page! {0}".format(prettyPrint(key)))
            print("")

    creationDf.to_csv(os.path.join(creation, creation_file), encoding="utf-8")



def main():

    start = time.time()

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
    print("Login took {0} seconds.".format(str(endLogin - start)))

    date_sanity_check(S, url, headers)

    endCheck = time.time()
    print("Sanity check took {0} seconds.".format(str(endCheck - endLogin)))

    endTime = time.time()
    print("Total time elapsed: {0} seconds.".format(str(endTime - start)))

if __name__ == "__main__":
    main()