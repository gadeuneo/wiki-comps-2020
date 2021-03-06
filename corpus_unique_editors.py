'''
    Plots unique editors aggregated across corpus
    Plots monthly unique editors across corpus


    Written by Junyi.  Updated by James Gardner to work with new data folders.
'''

import pandas as pd
from pandas.plotting import register_matplotlib_converters
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from static_helpers import *

register_matplotlib_converters()
start = time.time()

# folder of files
path = "10 Year Revision Data"
plotPath = "figures"
directories = ["figures"]
create_directories(directories)

revisonFiles = os.listdir(path)
revisionDict = dict()
for r in revisonFiles:
    revisionDict[r[:-4]] = pd.read_csv(os.path.join(path, r))

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

#Plots monthly unique editors over time
def plotMonthly():
    data = returnData()
    monthlyDict = dict()
    for item in data:
        month = item[0].month
        if(month<10):
            month = "0" + str(month)
        year = item[0].year
        yearMonth = str(year) + "-" + str(month)

        if(monthlyDict.get(yearMonth) == None):
            monthlyDict[yearMonth] = item[1]
        else:
            oldSet = monthlyDict.get(yearMonth)
            newSet = oldSet.union(item[1])
            monthlyDict[yearMonth] = newSet

    xAxisElements = []
    yAxisElements = []
    for key in monthlyDict:
        xAxisElements.append(key)
        yAxisElements.append(len(monthlyDict[key]))

    fig, ax = plt.subplots(figsize=(15,4))
    ax.plot(xAxisElements, yAxisElements)

    figureTitle = "Aggregated monthly unique editors"
    fig.autofmt_xdate()
    plt.title(figureTitle)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time (Year-Month)")
    plt.ylabel("Number of Editors")

    subpath = "editoranalysis"
    #
    #os.mkdir(os.path.join(plotPath, subpath))
    #newpath = os.path.join(plotPath, subpath)
    #
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()

#Plots unique editors over time
def plotAbsoluteOverTimeGraph():
    data = returnData()
    xAxisElements = []
    yAxisElements = []
    editorSet = set()
    for pair in data:
        xAxisElements.append(pair[0])
        editorSet = editorSet.union(pair[1])
        yAxisElements.append(len(editorSet))
    fig, ax = plt.subplots(figsize=(15,4))
    ax.plot(xAxisElements, yAxisElements)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    #ax.format_xdata = mdates.DateFormatter('%Y-%m')
    figureTitle = "Number of Unique Editors Over Time"
    fig.autofmt_xdate()
    plt.title(figureTitle)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time")
    plt.ylabel("Number of Editors")

    subpath = "editoranalysis"
    #
    #os.mkdir(os.path.join(plotPath, subpath))
    #newpath = os.path.join(plotPath, subpath)
    #
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()

#Returns the data in the form of [date - set of editors on that date]
def returnData():
    editorDict = dict()
    for title in revisionDict.keys():
        article = revisionDict[title]
        for index, rowData in article.iterrows():
            editDate = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
            if(rowData['userid'] != 0): #not anon
                user = rowData['user']
                if(editorDict.get(editDate)==None):
                    newSet = set()
                    newSet.add(user)
                    editorDict[editDate] = newSet
                else:
                    currSet = editorDict.get(editDate)
                    currSet.add(user)
                    editorDict[editDate] = currSet
    return(dictToList(editorDict))

#Converts dictionary items into a list of date and set
def dictToList(dict):
    resultList = []
    currDate = startDate
    while(currDate<=endDate):
        if(dict.get(currDate)==None):
            pair = [currDate, set()]
            resultList.append(pair)
        else:
            pair = [currDate, dict.get(currDate)]
            resultList.append(pair)
        currDate += timedelta(days=1)
    return resultList

'''Testing Below'''
start = "2009-01-10"
end = "2019-12-10"
startDate = dt.fromtimestamp(int(time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple()))).date()
endDate = dt.fromtimestamp(int(time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple()))).date()

plotMonthly()


sys.exit(0)
