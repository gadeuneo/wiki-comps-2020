'''
    Functions that are commonly called by other functions in this repo.

    Written by Jackie Chan.
'''

import os
import sys

import time
from datetime import datetime

'''
    Description: Reads the first two lines in credentials.txt which should be
    the username and password of the MediaWiki API bot.

    Input: Nothing.

    Output: Two strings, username and password.
'''
def get_credentials():

    if (not os.path.isfile("credentials.txt")):
        print("You are missing the credentials.txt file. Exiting program.")
        exit()

    with open("credentials.txt", "r", encoding="utf-8") as file:
        credentials = file.read()

    credentials = credentials.split()
    username = credentials[0]
    password = credentials[1]

    return username, password

'''
    Description: Reads the titles in titles.txt and returns a list of titles in
    the file. Omits any empty strings.

    Input: Nothing.

    Output: A list of titles from titles.txt.
'''
def get_titles():

    with open("titles.txt", "r", encoding="utf-8") as file:
        titles = file.read()

    titles = titles.split("\n")

    # Remove empty strings
    while ("" in titles):
        titles.remove("")

    return titles

'''
    Description: Creates directories for the given list of directory names if
    they do not exist.

    Input: A list of strings of directory names.

    Output: Directories in the root directory.
'''
def create_directories(directory_names):

    for directory_name in directory_names:
        create_directory(directory_name)

    return

'''
    Description: Creates the directory with the given name/string if it does not
    exist already.

    Input: A string for the directory name.

    Output: A directory with the given name if it does not exist.
'''
def create_directory(directory_name):
    if (not os.path.exists(directory_name)):
        os.mkdir(directory_name)

    return

'''
    Description: Given a list of titles, appends the string "Talk:" to the
    beginning of it. Does NOT modify the given list.

    Input: A list of strings.

    Output: A copy of the list with the additional titles with "Talk:" appended
    to the front.
'''
def add_talk_pages(titles):

    titles_copy = titles.copy()

    for title in titles:
        titles_copy.append("Talk:" + title)

    return titles_copy


'''
    Description: Returns the list of titles with talk pages.

    Input: None.

    Output: Returns the list of titles with talk pages.
'''
def get_titles_and_talk_pages():

    titles = get_titles()
    titles = add_revision_talk_pages(titles)

    return titles

'''
    Description: Performs same task as add_talk_pages(). Used to handle files
    that are formatted in a different way than the files found in the other
    file directories.

    Input: A list of strings.

    Output: A copy of the list with the additional titles with "Talk-" appended
    to the front.
'''
def add_revision_talk_pages(titles):

    titles_copy = titles.copy()

    for title in titles:
        titles_copy.append("Talk-" + title)

    return titles_copy

'''
    Descripton: Given a string, replaces spaces with underscores, periods with
    "(dot)", and colons with "(colon)". With the modified string, it then
    appends ".csv" to the title.

    Input: A string/title.

    Output: A modified string based on the rules in the description.
'''
def format_file_names(title):

    rules = {
        " ": "_",
        ".": "(dot)",
        ":": "(colon)"
    }

    for key in rules.keys():
        title = title.replace(key, rules[key])

    return title + ".csv"

'''
    Description: Given a string, appends ".csv" to the title. Needed to handle
    files that are formatted in a different way than the files found in the other
    file directories.

    Input: A string/title.

    Output: A modified string that has ".csv" appended to the end.
'''

def add_file_extension(title):
    return title + ".csv"
'''
    Description: Given a complete path to a particular file, returns True or
    False based on if it exists.

    Input: A complete path to a particular file.

    Output: True or False based on if the file exists.
'''
def file_exists(complete_file_name):

    if os.path.isfile(complete_file_name):
        return True

    return False

'''
    Description: Prints the different levels of nested keys in a JSON object.
    When there are no more dictionaries to key into, prints objects type and
    byte-size. Also iterates through lists of dictionaries.

    Input: A dictionary representing a JSON object.

    Output: Prints to console.
'''
def printJsonTree(d, indent=0):
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

'''
    Description: Pretty-prints JSON/Python dictionary result from the MediaWiki
    API. Will print to the terminal if there are any errors, or print a success
    message if there are no errors.

    Input: A request object.

    Output: Nothing, it prints to the terminal.
'''
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
    Description: Checks for a given request object if there were any warning or
    errors contained in it. A helper function to ensure queries do not crash
    the script.

    Input: A request object.

    Output: True or False based on the containment of warnings or errors.
'''
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
    Description: Initializes the start and end dates for analysis when formatted
    in "YYYY-MM-DD". Enforces some sanity checks as well and returns the
    formatted dates.

    Input: Two dates formatted in "YYYY-MM-DD".

    Output: Correctly formatted time for analysis.
'''
def format_time(start_date, end_date):
    # Convert date to Unix Timestamp
    start_date = int(time.mktime(datetime.strptime(start_date, "%Y-%m-%d").timetuple()))
    end_date = int(time.mktime(datetime.strptime(end_date, "%Y-%m-%d").timetuple()))
    today = int(time.mktime(datetime.today().timetuple()))

    # Assertions for proper date args
    assert(start_date <= end_date)
    assert(end_date <= today)

    return start_date, end_date

'''
    Description: Given a title, makes a request to the MediaWiki API to get the
    page ID.

    Input: The current session, url, headers, and the title of the article.

    Output: The page ID for the article.
'''
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

def prettyPrint(dictKey):
    newTitle = str(dictKey)
    newTitle = newTitle.replace("Data", "").replace("_", " ").replace("(dot)",".").replace("(colon)","-")
    return newTitle