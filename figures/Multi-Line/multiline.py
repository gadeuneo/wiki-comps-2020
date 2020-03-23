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
path = "data"
plotPath = "figures"

directories = ["figures"]

create_directories(directories)

# working list of Wiki pages
titles = get_titles()

# adds talk pages
titles = add_talk_pages(titles)

# converts titles to filename format
titles = [format_file_names(title) for title in titles]
titleArray = []
for title in titles:
    titleArray.append("Data" + title)
    titleArray.append("Redirects" + title)

# check if file exists, if not, remove from list of titles
for title in titles:
    if (not os.path.isfile(os.path.join(path, "Data" + title))):
        filename = "Data" + title
        titleArray.remove(filename)

    if (not (os.path.isfile(os.path.join(path, "Redirects" + title)))):
        filename = "Redirects" + title
        titleArray.remove(filename)


##### TODO: merge files? -- Which ones? How?
##### TODO: save merged files?


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
# revisionData.sort_values(by='timestamp', inplace = True)
# revisionData['timestamp'] = revisionData['timestamp'].astype(str)
# revisionData['timestamp'] = revisionData['timestamp'].str.replace(" ", "T").str[:-6] + "Z"
#print(revisionData.to_string())

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2019-6-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# TODO: loop over timestamps and get count for each (day/week/month?)

# test get next day epoch time


def makeMultipleLineFigure(titleArray, titles):
    for title in titleArray[:19]:
        key = title[:-4]
        if key[0:4]=="Data":
            article = dataDict[key]
            newDate = dt.fromtimestamp(startDate)
            days = []
            counts = []
            #counts the edits
            edits = 0
            #plt.figure(figsize=(15,7))
            for day in article['timestamp']:
                editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
                while(editTime > newDate):
                    counts.append(edits)
                    epoch = int(newDate.timestamp())
                    days.append(dt.fromtimestamp(epoch))
                    #newDate = newDate + timedelta(days=1)
                    newDate = newDate + timedelta(days=7)
                    edits = 0
                edits += 1
            '''fig, ax = plt.subplots(figsize=(15,7))
            ax.plot(days, counts)
            ax.xaxis.set_major_locator(mdates.MonthLocator())
            #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
            ax.xaxis.set_minor_locator(mdates.DayLocator())
            ax.format_xdata = mdates.DateFormatter('%Y-%m')

            fig.autofmt_xdate()'''
            plt.plot(days, counts, label= title)
            plt.gcf().set_size_inches(15,7)

    plt.title(titles)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time")
    plt.ylabel("Number Edits")

    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    if (not os.path.isfile(os.path.join(plotPath, titles+".png"))):
        plt.savefig(os.path.join(plotPath, titles+".png"), bbox_inches="tight")
    plt.close()

#separate out "DATA-" articles from "REVISION-", without the .csv
dataTitleArray = []
for title in titleArray:
    if title[0:4] == "Data":
        dataTitleArray.append(title[:-4])

#makeMultipleLineFigure(titleArray, "Edits by Day of Top 10 Most Revised Articles")
makeMultipleLineFigure(titleArray, "Edits by Week of Top 10 Most Revised Articles - 6 Month Span")


end = time.time()
print("Time Elapsed: " + str(end-start))

sys.exit(0)
