'''
Gets pageview data of wikipage per date.
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
from static_helpers import *
#from selenium import webdriver
import shutil


path = "WikiData-pageviews"
newpath = "dailyPageviews"

if (not os.path.exists(newpath)):
    os.mkdir(newpath)

# Convert date to Unix Timestamp
startDate = dt.strptime("2009-12-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")
today = dt.today()

# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

titles = get_titles()
titles = add_talk_pages(titles)

'''
Begin WFMLABS pageview collection
'''

url = '''https://tools.wmflabs.org/redirectviews/?project=en.wikipedia.org
        &platform=all-access&agent=user&range=all-time&sort=views
        &direction=1&view=list&page='''

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
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", downloadPath)
    profile.set_preference("browser.download.downloadDir", downloadPath)
    # profile.set_preference("browser.helperApps.neverAsk.openFile", ",".join(mime_types))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ",".join(mime_types))
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.get(url + title)
    time.sleep(10)
    button = driver.find_elements_by_class_name("btn.btn-default.btn-sm.dropdown-toggle")[2]
    button.click()
    time.sleep(1)
    button = driver.find_elements_by_class_name("download-csv")[0]
    button.click()
    time.sleep(5)
    driver.close()

files = [format_file_names(title) for title in titles]
assert(len(titles) == len(files))

'''
    moves from download folder to new folder specified above.
'''
def getPageviews():
    # may need different download path if above browser preference did not change default path
    downloadPath = "/home/james/Downloads/"
    for i in range(len(titles)):
        getFile(titles[i])
        f = [x for x in os.listdir(downloadPath) if x.endswith('.csv')]
        # find the most recently modified csv file
        paths = [os.path.join(downloadPath, name) for name in f]
        newest = max(paths, key=os.path.getctime)
        shutil.move(newest, os.path.join(newpath, files[i]))


if (len(os.listdir(path)) != len(titles)):
    getPageviews()

'''
    Reformats csv file from columns as dates to rows as date
'''
def reformatFiles():
    for i in range(len(titles)):
        pageDf = pd.read_csv(os.path.join(path, files[i]))
        # prints daily sums
        # print(pageDf.sum(axis=0, skipna=True))
        # prints page title sums
        # print(pageDf.sum(axis=1, skipna=True))
        pageviews = [["Date", "Count"]]

        for col in pageDf.columns[1:]:
            if (dt.strptime(col, "%Y-%m-%d") > endDate):
                break
            else:
                pageviews.append([col, pageDf[col].sum()])

        if (not (os.path.isfile(os.path.join(newpath, files[i])))):
                        dfData = pd.DataFrame(pageviews[1:], columns=pageviews[0])
                        dfData.to_csv(os.path.join(newpath, files[i]), encoding="utf-8")

if (len(os.listdir(newpath)) != len(titles)):
    reformatFiles()

'''
End WFMLABS pageview collection
'''

'''
Begin REST API pageview collection
'''
## YYYYMMDDHH format for dates
beginDate = 2019121000
stopDate = 2019121000

restUrl = '''https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{0}/daily/{1}/{2}'''
header = {
    "accept": "application/json"
}

S = rq.Session()

def getRESTPageviews(S, url, headers, title, begin, end):
    rest = url.format(title, begin, end)
    rest = rest.replace(" ","")
    data = S.get(url=rest, headers = headers).json()
    return data

pageData = dict()

fomrattedTitles = [t.replace(" ","_") for t in titles]

for title in fomrattedTitles:
    pageData[title] = getRESTPageviews(S, restUrl, header, title, beginDate, stopDate)

for i in fomrattedTitles:
    print(pageData[i])

'''
End REST API pageview collection
'''