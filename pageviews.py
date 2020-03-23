'''
Gets pageview data of wikipage per date from the MediaWiki API.
Saves in csv format per page.

James Gardner
'''

import pandas as pd
import os
import sys
import requests as rq
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time

# functions that are frequently accessed by other files
from static_helpers import *


'''
Begin MediaWiki API pageview collection
'''

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

def get_redirects(S, url, headers, pageid):
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

def get_page_id(session, url, headers, title):
    page = {
            "action": "query",
            "prop": "revisions",
            "titles": title,
            "format": "json"
        }

    data = session.get(url=url, headers=headers, params=page).json()
    if (hasError(data)):
        print("Query Error! Exiting program!")
        sys.exit(1)
    if (int(list(data['query']['pages'].keys())[0]) == -1):
        print("Title: {0} not found! Please check the spelling!".format(title))
        sys.exit(1)
    page_id = list(data['query']['pages'].keys())[0]
    return page_id


'''
    End Data Collection Functions
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

    # To change included titles, go to local titles.txt file
    titles = get_titles()
    titles_plus_talk = add_talk_pages(titles)

    start_date, end_date = format_time(start_date="2009-12-10",
        end_date="2019-12-10")

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=

    




if __name__ == "__main__":
    main()

'''
End MediaWiki API pageview collection
'''