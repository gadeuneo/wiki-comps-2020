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

# functions that are frequently accessed by other files
from static_helpers import *

startTime = time.time()

# Convert date to REST API Time format
## YYYYMMDD or YYYYMMDDHH format for dates
startDate = dt.strptime("20091210", "%Y%m%d")
endDate = dt.strptime("20191210", "%Y%m%d")
today = dt.today()

restPath = "restPageviews"

if (not os.path.exists(restPath)):
    os.mkdir(restPath)

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

# TODO: make more efficient way - currently takes too long
def getRESTPageviews(S, url, headers, title, begin, end):
    start = dt.strftime(begin, "%Y%m%d")
    newDate = startDate
    
    pageviews = [["Date", "Pageviews"]]

    while (newDate < endDate):       
        stop = dt.strftime(newDate, "%Y%m%d")
        rest = url.format(title, start, stop)
        rest = rest.replace(" ","")
        data = S.get(url=rest, headers = headers).json()
        newDate = newDate + timedelta(days=1)
        # Error in REST API query handling
        # TODO: figure out how to handle redirects of a page
        # NOTE: is this the same as the wmflabs tool?
        if ('type' in data.keys()):
            # Go to next iteration of loop - data not found
            continue
        else:
            saveDate = dt.strftime(newDate, "%Y-%m-%d")
            pageviews.append([saveDate, data['items'][0]['views']])

    return pageviews

pageData = dict()

fomrattedTitles = []
for t in titles:
    t = t.replace(" ", "_")
    t = t.replace(":","(colon)")
    fomrattedTitles.append(t)

for title in fomrattedTitles:
    pageData[title] = getRESTPageviews(S, restUrl, header, title, startDate, endDate)


for fileName in pageData.keys():
    if (not (os.path.isfile(os.path.join(restPath, fileName + ".csv")))):
        dfRest = pd.DataFrame(pageData[fileName][1:], columns=pageData[fileName][0])
        dfRest.to_csv(os.path.join(restPath, fileName + ".csv"))
    else:
        restcsv = pd.read_csv(os.path.join(restPath, fileName + ".csv"))
        # TODO: handle append to file once redirects sorted out


endTime = time.time()
print("Time Elapsed: " + str(endTime - startTime))

'''
End REST API pageview collection
'''