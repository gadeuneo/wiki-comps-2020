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

def create_creation_dates_data(session, url, headers, titles):

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

def create_revision_data(session, url, headers, titles, start_date, end_date):

    start_time = time.time()

    directory = "10 Year Revision Data"
    create_directory(directory)

    file_names = [title + ".csv" for title in titles]

    for title, file_name in zip(titles, file_names):

        try:
            page_id = get_page_id(session, url, headers, title)
            revision_data = get_revisions(session, url, headers, page_id,
                start=start_date, end=end_date)

            complete_path = os.path.join(directory, file_name)

            if (not os.path.isfile(complete_path)):
                df_revisions = pd.DataFrame(revision_data)

                # Add page_id as a column in the dataframe.
                df_revisions['page_id'] = page_id

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

def generate_redirect_data(session, url, headers, titles, start_date, end_date):

    start_time = time.time()

    directory = "10 Year Redirect Data"
    create_directory(directory)

    file_names = [title + ".csv" for title in titles]

    for title, file_name in zip(titles, file_names):

        try:
            page_id = get_page_id(session, url, headers, title)
            redirect_data = get_redirects(session, url, headers, page_id)
            
            complete_path = os.path.join(directory, file_name)

            if (not os.path.isfile(complete_path)):
                df_redirects = pd.DataFrame(redirect_data)
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

    start_date, end_date = format_time(start_date="2009-12-10",
        end_date="2019-12-10")

    titles_plus_talk = add_talk_pages(titles)

    # Use pageid for curid to check if correct page is found
    # https://en.wikipedia.org/?curid=

    # generate_creation_dates_data(S, url, headers, titles)


    '''
        Uncomment the relevant data you want updated or generated.
    '''

    start_collection = time.time()

    '''
        BUG: Pages: "Death/Killing of Luo Changqing" and "List of March-June
        2019 Hong Kong protests" were not found. This includes their talk pages.
    '''
    create_revision_data(S, url, headers, titles_plus_talk,
        start_date, end_date)

    '''
        BUG: Pages: "Civil Human Rights Front", "Hong Kong Way",  and "List of
        {March-June, December} 2019 Hong Kong protests" were not found.
    '''
    # create_redirect_data(S, url, headers, titles,
    #     start_date, end_date)

    end_collection = time.time()

    print("Data collection took {0} seconds."
        .format(str(end_collection - start_collection)))

    end = time.time()
    print("Time Elapsed: " + str(end - start))

if __name__ == "__main__":
    main()
