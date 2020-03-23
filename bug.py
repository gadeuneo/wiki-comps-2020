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

# functions that are frequently accessed by other files
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



'''
    Begin Data Collection Functions
'''

def get_revisions(S, url, headers, pageid, start=None, end=None):
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


def create_revision_data(session, url, headers, titles, start_date, end_date,
    debug_mode=False):

    directory = "10 Year Revision Data"
    create_directory(directory)

    file_names = [title + ".csv" for title in titles]

    for title, file_name in zip(titles, file_names):

        try:
            page_id = get_page_id(session, url, headers, title)
            revision_data = get_revisions(session, url, headers, page_id,
                start=start_date, end=end_date)

            complete_path = os.path.join(directory, file_name)

            df_revisions = pd.DataFrame(revision_data)

            # Add page_id as a column in the dataframe.
            df_revisions['page_id'] = page_id

            if (not debug_mode):
                if (not os.path.isfile(complete_path)):
                    df_revisions.to_csv(complete_path, encoding="utf-8")
                # else:
                #     print("Did not overwrite {0} because it currently exists!"
                #         .format(file_name))
        except:
            print("Data not found for {0}.".format(title))
            print("Page ID: {0}".format(page_id))

    return

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

    # To change included titles, go to titles.txt
    titles = get_titles()
    titles = add_talk_pages(titles)

    start_date, end_date = format_time(start_date="2009-12-10",
        end_date="2019-12-10")

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=


    '''
        BUG: Pages: "Death/Killing of Luo Changqing" and "List of March-June
        2019 Hong Kong protests" were not found. This includes their talk pages.
    '''

    '''
        BUG: Pages: "Civil Human Rights Front", "Hong Kong Way",  and "List of
        {March-June, December} 2019 Hong Kong protests" were not found.
    '''

    create_revision_data(S, url, headers, titles,
        start_date, end_date)

if __name__ == "__main__":
    main()
