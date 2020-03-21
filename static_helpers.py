import os
import sys

import time
from datetime import datetime

def get_credentials():

    with open("credentials.txt", "r", encoding="utf-8") as file:
        credentials = file.read()

    credentials = credentials.split()
    username = credentials[0]
    password = credentials[1]

    return username, password

def get_titles():

    with open("titles.txt", "r", encoding="utf-8") as file:
        titles = file.read()

    titles = titles.split("\n")

    # Remove empty strings
    while ("" in titles):
        titles.remove("")

    return titles

# Pass in a list of directories to create
def create_directories(directory_names):

    for directory_name in directory_names:
        if (not os.path.exists(directory_name)):
            os.mkdir(directory_name)

    return

# Given a list of titles, returns a copy of the list with talk pages.
# Doesn't change the original list given.
def add_talk_pages(titles):

    titles_copy = titles.copy()

    for i in range(len(titles)):
        titles_copy.append("Talk:" + titles[i])

    return titles_copy

def format_file_names(title):

    rules = {
        " ": "_",
        ".": "(dot)",
        ":": "(colon)"
    }

    for key in rules.keys():
        title = title.replace(key, rules[key])

    return title + ".csv"

def file_exists(complete_file_name):

    if os.path.isfile(complete_file_name):
        return True

    return False

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

def time_sanity_check():
    # Convert date to Unix Timestamp
    start_date = int(time.mktime(datetime.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
    end_date = int(time.mktime(datetime.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
    today = int(time.mktime(datetime.today().timetuple()))

    # Assertions for proper date args
    assert(start_date <= end_date)
    assert(end_date <= today)

    return

def get_page_id(S, url, headers, title):
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
    page_id = list(data['query']['pages'].keys())[0]
    return page_id