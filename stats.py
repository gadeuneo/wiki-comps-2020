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
path = "10years"
plotPath = "figures"

directories = ["figures"]

create_directories(directories)

# working list of Wiki pages
titles = get_titles()

# adds talk pages
titles = add_talk_pages(titles)

# converts titles to filename format
titles = [formatFileNames(title) for title in titles]
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

revisionData = pd.concat(allData, ignore_index=True, sort=False)
revisionData['timestamp'] = pd.to_datetime(revisionData['timestamp'])
revisionData.sort_values(by='timestamp', inplace = True)
revisionData['timestamp'] = revisionData['timestamp'].astype(str)
revisionData['timestamp'] = revisionData['timestamp'].str.replace(" ", "T").str[:-6] + "Z"
#print(revisionData.to_string())

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# TODO: loop over timestamps and get count for each (day/week/month?)

# test get next day epoch time

def makeTimeXRevisionFigure(title):
    article = dataDict[title]
    newDate = dt.fromtimestamp(startDate)
    days = []
    counts = []
    #counts the edits
    edits = 0
    for day in article['timestamp']:
        editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
        while(editTime > newDate):
            counts.append(edits)
            epoch = int(newDate.timestamp())
            days.append(dt.fromtimestamp(epoch))
            newDate = newDate + timedelta(days=1)
            #newDate = newDate + timedelta(days=7)
            edits = 0
        edits += 1
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

    subpath = "10y Time vs Num Revisions"
    # os.mkdir(os.path.join(plotPath, subpath))
    # newpath = os.path.join(plotPath, subpath)
    if (not os.path.isfile(os.path.join(plotPath, subpath, title + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, title + ".png"), bbox_inches="tight")
    plt.close()

def makeTimeXNumEditorsFigure(title):
    article = dataDict[title]
    newDate = dt.fromtimestamp(startDate)
    currMonth = dt.fromtimestamp(startDate).month
    editorSet = set()
    sizeOfArticle = article.shape[0]
    countArr = []
    dateArr = []
    newDate = dt.fromtimestamp(startDate)
    for index, row in article.iterrows():
        editTime = dt.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        while(newDate < editTime):
            if(newDate.month!=currMonth):
                countArr.append(len(editorSet))
                epoch = int((newDate-timedelta(days=1)).timestamp())
                dateArr.append(dt.fromtimestamp(epoch))
                editorSet.clear()
                newDate = newDate+timedelta(days=1)
                currMonth = newDate.month
            else:
                newDate = newDate+timedelta(days=1)
        #out of while loop, means newDate = editTime
        #edge case of last index
        if(index == (sizeOfArticle-1)):
            if(currMonth == editTime.month):
                editorSet.add(row['user'])
            else:
                countArr.append(len(editorSet))
                epoch = int(editTime.timestamp())
                dateArr.append(dt.fromtimestamp(epoch))
                editorSet.clear()
                editorSet.add(row['user'])
                currMonth = editTime.month
            countArr.append(len(editorSet))
            dateArr.append(dt.fromtimestamp(epoch))
        else:
            if(currMonth == editTime.month):
                editorSet.add(row['user'])
            else:
                countArr.append(len(editorSet))
                epoch = int(editTime.timestamp())
                dateArr.append(dt.fromtimestamp(epoch))
                editorSet.clear()
                editorSet.add(row['user'])
                currMonth = editTime.month

    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(dateArr, countArr)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')

    fig.autofmt_xdate()
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Number of Editors Per Month")
    subpath = "10y Time vs Number Editors Per Month"
    # os.mkdir(os.path.join(plotPath, subpath))
    # newpath = os.path.join(plotPath, subpath)
    if (not os.path.isfile(os.path.join(plotPath, subpath, title + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, title + ".png"), bbox_inches="tight")
    plt.close()

def makeMultipleLineFigure(titleArray, titles):
    for title in titleArray:
        key = title[:-4]
        if key[0:4]=="Data":
            article = dataDict[key]
            newDate = dt.fromtimestamp(startDate)
            days = []
            counts = []
            #counts the edits
            edits = 0
            for day in article['timestamp']:
                editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
                while(editTime > newDate):
                    counts.append(edits)
                    epoch = int(newDate.timestamp())
                    days.append(dt.fromtimestamp(epoch))
                    newDate = newDate + timedelta(days=1)
                    #newDate = newDate + timedelta(days=7)
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
            plt.plot(days, counts)

    plt.title(titles)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time")
    plt.ylabel("Number Edits")
    if (not os.path.isfile(os.path.join(plotPath, titles+".png"))):
        plt.savefig(os.path.join(plotPath, titles+".png"), bbox_inches="tight")
    plt.close()

#separate out "DATA-" articles from "REVISION-", without the .csv
dataTitleArray = []
for title in titleArray:
    if title[0:4] == "Data":
        dataTitleArray.append(title[:-4])

'''testing/making statistics below'''
'''for title in dataTitleArray:
    makeTimeXNumEditorsFigure(title)'''

#makeMultipleLineFigure(titleArray, "Muliple Line Graph - Edits per Day")


##### TODO: Make plots
#### https://matplotlib.org/tutorials/introductory/pyplot.html

### SAMPLE CODE
# https://towardsdatascience.com/matplotlib-tutorial-learn-basics-of-pythons-powerful-plotting-library-b5d1b8f67596

# plots x values, then y values
'''plt.plot([1,2,3,4], [1,4,9,16])
plt.title("Sample plot")
plt.xlabel("Sample x axis label")
plt.ylabel("Sample y axis label")

if (not os.path.isfile(os.path.join(plotPath, "sample.png"))):
    plt.savefig(os.path.join(plotPath, "sample.png"), bbox_inches="tight")
'''

end = time.time()
print("Time Elapsed: " + str(end-start))

sys.exit(0)
