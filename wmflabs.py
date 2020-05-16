'''
    Gets pageview data of wikipage per date from the wmflabs site.
    Saves in csv format per page.

    Written by James Gardner
'''

import pandas as pd
import os
import sys
from datetime import datetime as dt
import time
# allows Python webdriver functionality for automation
from selenium import webdriver
import shutil
from static_helpers import *

# file paths to save data
newpath = "dailyPageviews"

path = "WikiData-pageviews"

if (not os.path.exists(path)):
    os.mkdir(path)

if (not os.path.exists(newpath)):
    os.mkdir(newpath)

# pages to collect pageview data from
titles = get_titles()
titles = add_talk_pages(titles)

'''
Begin WFMLABS pageview collection
'''
# base url to collect pageview data
url = '''https://tools.wmflabs.org/redirectviews/?project=en.wikipedia.org
        &platform=all-access&agent=user&range=all-time&sort=views
        &direction=1&view=list&page='''

# https://stackoverflow.com/questions/38458811/control-firefox-download-prompt-using-selenium-and-python
mime_types = [
    'text/plain', 
    'application/vnd.ms-excel', 
    'text/csv', 
    'application/csv', 
    'text/comma-separated-values', 
    'application/download', 
    'application/octet-stream', 
    'binary/octet-stream', 
    'application/binary', 
    'application/x-unknown'
]

downloadPath = "/home/james/GitHub/wiki-comps-2020/WikiData-pageviews/"


'''
    Auto download file from wmflabs.org tool for redirects pageviews
'''
def getFile(title):
    # https://stackoverflow.com/questions/44175006/windows-popup-interaction-for-downloading-using-selenium-webdriver-in-python
    # webdriver preferences for file saving - finicky, didn't work sometimes
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", downloadPath)
    profile.set_preference("browser.download.downloadDir", downloadPath)
    # profile.set_preference("browser.helperApps.neverAsk.openFile", ",".join(mime_types))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(url + title)

    # hardcode wait for button element to appear
    # TODO: check if element exists instead?
    time.sleep(10)
    button = driver.find_elements_by_class_name("btn.btn-default.btn-sm.dropdown-toggle")[2]
    button.click()
    # hardcode wait for button element to appear
    # TODO: check if element exists instead?
    time.sleep(1)
    button = driver.find_elements_by_class_name("download-csv")[0]
    button.click()
    # hardcode wait for download to complete
    # TODO: check if file exists instead?
    time.sleep(5)
    driver.close()

files = [format_file_names(title) for title in titles]
assert(len(titles) == len(files))

'''
    moves from download folder to new folder specified above.
'''
def movePageviews():
    # may need different download path if above browser preference did not change default path
    downloadPath = "/home/james/Downloads/"
    for i in range(len(titles)):
        getFile(titles[i])
        # https://stackoverflow.com/questions/5899497/how-can-i-check-the-extension-of-a-file
        f = [x for x in os.listdir(downloadPath) if x.endswith('.csv')]
        # find the most recently modified csv file
        # https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder-using-python
        paths = [os.path.join(downloadPath, name) for name in f]
        newest = max(paths, key=os.path.getctime)
        # https://docs.python.org/3.8/library/shutil.html#shutil.move
        shutil.move(newest, os.path.join(newpath, files[i]))


if (len(os.listdir(path)) != len(titles)):
    movePageviews()

'''
    Reformats csv file from columns as dates to rows as date
'''
def reformatFiles():
    for i in range(len(titles)):
        pageDf = pd.read_csv(os.path.join(path, files[i]))
        pageviews = [["Date", "Count"]]

        for col in pageDf.columns[1:]:
            pageviews.append([col, pageDf[col].sum()])

        if (not (os.path.isfile(os.path.join(newpath, files[i])))):
            dfData = pd.DataFrame(pageviews[1:], columns=pageviews[0])
            dfData.to_csv(os.path.join(newpath, files[i]), encoding="utf-8")

if (len(os.listdir(newpath)) != len(titles)):
    reformatFiles()

'''
End WFMLABS pageview collection
'''