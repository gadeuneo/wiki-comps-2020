'''
    Gets metadata of wikipage per revision.
    Saves in csv format per revision.

    Written by James Gardner; refactored by Jackie Chan.
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

'''
    Collects revision data from MediaWiki API
    Inputs: Requests Session, url, headers, pageid, startDate, endDate
    Outputs: list of lists of revision data: 
        timestamp of data, username of editor, editor id, revision id,
        and edit size
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

'''
    Collects all redirect page ids from past pages due to
    page moves/redirects/renames.
    Inputs: Requests Session, url, headers, pageid
    Output: list of lists of page id, old page title
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

'''
    Get the creation date of a specified page from pageid input.
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

'''
    Initial collection of all creation dates from list of page titles.
'''
def create_creation_dates_data(session, url, headers, titles, debug_mode=False):

    start_time = time.time()

    # Why is it formatted this way? - Jackie
    dates = [["Titles", "Page Creation Date"]]

    bad_creation = False

    # finding and appending all creation dates in the titles list
    for i in range(len(titles)):
        page_id = get_page_id(session, url, headers, titles[i])

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

    if (not debug_mode):
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
    Secondary function to correct page creation dates as redirected pages
    do not properly store the original page creation date. Returns the oldest
    page creation date found.
'''
def date_sanity_check(S, url, headers):
    path = "10 Year Redirect Data"
    creation = "creation"
    creation_file = "creation_dates.csv"
    creationDf = pd.read_csv(os.path.join(creation, creation_file))
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

'''
    Collects revision data of list of titles.
'''
def create_revision_data(session, url, headers, titles, start_date, end_date,
    debug_mode=False):

    start_time = time.time()

    directory = "10 Year Revision Data"
    create_directory(directory)

    file_names = [title.replace(":", "-") + ".csv" for title in titles]

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
                else:
                    print("Did not overwrite {0} because it currently exists!"
                        .format(file_name))
        except:
            print("Data not found for {0}.".format(title))
            print("Page ID: {0}".format(page_id))



    end_time = time.time()
    print("Page revision data took {0} seconds."
        .format(str(end_time - start_time)))

    return

'''
    Collects redirect data from list of titles.
'''
def create_redirect_data(session, url, headers, titles, start_date, end_date,
    debug_mode=False):

    start_time = time.time()

    directory = "10 Year Redirect Data"
    create_directory(directory)

    file_names = [title + ".csv" for title in titles]

    for title, file_name in zip(titles, file_names):

        try:
            page_id = get_page_id(session, url, headers, title)
            redirect_data = get_redirects(session, url, headers, page_id)
            
            complete_path = os.path.join(directory, file_name)
            
            df_redirects = pd.DataFrame(redirect_data)

            if (not debug_mode):
                if (not os.path.isfile(complete_path)):
                    df_redirects.to_csv(complete_path, encoding="utf-8")
                else:
                    print("Did not overwrite {0} because it currently exists!"
                        .format(file_name))
        except:
            print("Data not found for {0}.".format(title))
            print("Page ID: {0}".format(page_id))
        

    end_time = time.time()
    print("Page redirect data took {0} seconds."
        .format(str(end_time - start_time)))

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

    endLogin = time.time()
    print("Login took {0} seconds.".format(str(endLogin - start)))

    # To change included titles, go to titles.txt
    titles = get_titles()
    titles_plus_talk = add_talk_pages(titles)

    start_date, end_date = format_time(start_date="2009-12-10",
        end_date="2019-12-10")

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=

    '''
        Uncomment the relevant data you want updated or generated.
    '''

    start_collection = time.time()

    # create_creation_dates_data(S, url, headers, titles, debug_mode=False)

    create_revision_data(S, url, headers, titles_plus_talk,
        start_date, end_date, debug_mode=False)

    # create_redirect_data(S, url, headers, titles,
    #     start_date, end_date, debug_mode=False)

    end_collection = time.time()

    print("Data collection took {0} seconds."
        .format(str(end_collection - start_collection)))

    date_sanity_check(S, url, headers)

    date_check = time.time()

    print("Date checking took {0} seconds."
        .format(str(date_check - end_collection)))

    end = time.time()
    print("Time Elapsed: " + str(end - start))

if __name__ == "__main__":
    main()
