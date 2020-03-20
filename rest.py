'''
Gets pageview data of wikipage per date via REST API.
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

# Convert date to REST API Time format
## YYYYMMDDHH format for dates
startDate = dt.strptime("20191210", "%Y%m%d")
endDate = dt.strptime("20191210", "%Y%m%d")
today = dt.today()

# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

titles = get_titles()
titles = add_talk_pages(titles)

'''
Begin REST API pageview collection
'''

restUrl = '''https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia.org/all-access/all-agents/{0}/daily/{1}/{2}'''
header = {
    "accept": "application/json"
}

S = rq.Session()

def getRESTPageviews(S, url, headers, title, begin, end):
    start = dt.strftime(begin, "%Y%m%d")
    newDate = startDate
    
    pageviews = [["Date", "Pageviews"]]

    while (newDate <= endDate):       
        stop = dt.strftime(newDate, "%Y%m%d")
        rest = url.format(title, start, stop)
        rest = rest.replace(" ","")
        data = S.get(url=rest, headers = headers).json()
        newDate = newDate + timedelta(days=1)
        if ('type' in data.keys()):
            continue
        else:
            saveDate = dt.strftime(newDate, "%Y-%m-%d")
            pageviews.append([saveDate, data['items'][0]['views']])

    return pageviews

pageData = dict()

fomrattedTitles = [t.replace(" ","_") for t in titles]

for title in fomrattedTitles:
    pageData[title] = getRESTPageviews(S, restUrl, header, title, startDate, endDate)

# TODO: save data

'''
End REST API pageview collection
'''