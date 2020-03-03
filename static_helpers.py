import os
import sys

def get_credentials():

    with open("credentials.txt", "r", encoding="utf-8") as file:
        credentials = file.read()

    credentials = credentials.split()
    username = credentials[0]
    password = credentials[1]

    return username, credentials

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

def add_talk_pages(titles):

    for i in range(len(titles)):
        titles.append("Talk:" + titles[i])

    return titles

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