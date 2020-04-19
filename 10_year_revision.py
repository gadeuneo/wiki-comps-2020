'''
File for manipulating data.

James Gardner
'''

import pandas as pd
from pandas.plotting import register_matplotlib_converters
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import matplotlib.pyplot as plt
import numpy as np
#uhuh
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
#uhuh
import copy
from static_helpers import *

register_matplotlib_converters()
start = time.time()

# folder of files
path = "10 Year Revision Data"
plotPath = "figures"

directories = ["figures"]

create_directories(directories)

# working list of Wiki pages
titles = get_titles()

# adds talk pages
# titles = add_talk_pages(titles)

titles = add_revision_talk_pages(titles)

# converts titles to filename format
# titles = [format_file_names(title) for title in titles]
# titleArray = []
# for title in titles:
#     titleArray.append("Data" + title)
#     titleArray.append("Redirects" + title)
#
# # check if file exists, if not, remove from list of titles
# for title in titles:
#     if (not os.path.isfile(os.path.join(path, "Data" + title))):
#         filename = "Data" + title
#         titleArray.remove(filename)
#
#     if (not (os.path.isfile(os.path.join(path, "Redirects" + title)))):
#         filename = "Redirects" + title
#         titleArray.remove(filename)


##### TODO: merge files? -- Which ones? How?
##### TODO: save merged files?
titles = [add_file_extension(title) for title in titles]
titleArray = []
for title in titles:
    titleArray.append(title)
    
dataDict = dict()


for f in titleArray:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

# print(dataDict.keys())

allData = []
allRed = []
for key in dataDict.keys():
    if ("Data" in key):
        allData.append(dataDict[key])
    else:
        allRed.append(dataDict[key])

# revisionData = pd.concat(allData, ignore_index=True, sort=False)
# revisionData['timestamp'] = pd.to_datetime(revisionData['timestamp'])
# # TODO: double check inplace param
# revisionData.sort_values(by='timestamp', inplace = True)
# revisionData['timestamp'] = revisionData['timestamp'].astype(str)
# revisionData['timestamp'] = revisionData['timestamp'].str.replace(" ", "T").str[:-6] + "Z"
#print(revisionData.to_string())

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

#separate out "DATA-" articles from "REVISION-", without the .csv
dataTitleArray = []
for title in titleArray:
    if title[0:4] == "Data":
        dataTitleArray.append(title[:-4])

def makeTimeXRevisionFigure(title):
    key = title[:-4]
    article = dataDict[key]
    sizeOfArticle = article.shape[0]
    newDate = dt.fromtimestamp(startDate)
    prevDate = newDate
    days = []
    counts = []
    #counts the edits
    dayCount = 0
    edits = 0
    for day in article['timestamp']:
        editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
        dayCount += 1
        while(editTime > newDate):
            counts.append(edits)
            epoch = int(prevDate.timestamp())
            days.append(dt.fromtimestamp(epoch))
            # alter the timedelta to set edits by day, week, or month
            #newDate = newDate + timedelta(days=1)
            #newDate = newDate + timedelta(days=7)
            prevDate = newDate
            newDate = newDate + timedelta(days=30)
            edits = 0
        edits += 1
        if dayCount == sizeOfArticle:
            counts.append(edits)
            # Changed to prevDate so that edits are paired with the
            # correct timedelta.
            epoch = int(prevDate.timestamp())
            days.append(dt.fromtimestamp(epoch))

    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(days, counts)

    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')

    fig.autofmt_xdate()
    plt.title(title)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time")
    plt.ylabel("Number Edits")

    # subpath = "10y Time vs Num Revisions"
    subpath = "10y Time vs Num Revisions - Edits by Month"
    # os.mkdir(os.path.join(plotPath, subpath))
    # newpath = os.path.join(plotPath, subpath)
    if (not os.path.isfile(os.path.join(plotPath, subpath, title + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, title + ".png"), bbox_inches="tight")
    plt.close()

for title in titleArray:
    makeTimeXRevisionFigure(title)
