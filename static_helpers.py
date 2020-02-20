import os

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

def create_directories(directory_names):

    for directory_name in directory_names:
        if (not os.path.exists(directory_name)):
            os.mkdir(directory_name)

    return

def add_talk_pages(titles):

    for i in range(len(titles)):
        titles.append("Talk:" + titles[i])

    return titles
