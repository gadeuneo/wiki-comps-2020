
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

dataDict = dict()

for f in titleArray:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))
allData = []
allRed = []
for key in dataDict.keys():
    if ("Data" in key):
        allData.append(dataDict[key])
    else:
        allRed.append(dataDict[key])

revisionData = pd.concat(allData, ignore_index=True, sort=False)
revisionData['timestamp'] = pd.to_datetime(revisionData['timestamp'])
# TODO: double check inplace param
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

#separate out "DATA-" articles from "REVISION-", without the .csv
dataTitleArray = []
for title in titleArray:
    if title[0:4] == "Data":
        dataTitleArray.append(title[:-4])


# test get next day epoch time
def makeDayXJaccardFigure(title):
    article = dataDict[title]
    firstDay = dt.fromtimestamp(int(time.mktime(dt.strptime("2019-06-01", "%Y-%m-%d").timetuple()))).date()
    lastDay = dt.fromtimestamp(endDate).date()
    days = []
    jaccard = [] #jaccard score of each day
    edits = 0
    articleIndex = 0
    dailyEditorSet = set()
    sizeOfArticle = article.shape[0]

    #Setup
    currDate = firstDay
    while(currDate<=lastDay):
        days.append(currDate)
        currDate+=timedelta(days=1)
    #Fills up targetDict
    targetDict = returnTargetDict(article, firstDay, lastDay)

    #Fills up allOtherDict
    allOtherDict = returnAllOtherDict(title, firstDay, lastDay)
    #Calculate Jaccard, but also
    jaccard = calculateAndPrintJaccard(days, targetDict, allOtherDict, firstDay, lastDay)

    fig, ax = plt.subplots(figsize=(20,4))
    ax.plot(days, jaccard)

    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')

    fig.autofmt_xdate()
    plt.title(title)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Time")
    plt.ylabel("Jaccard Score")

    subpath = "Jaccard"
    #
    #os.mkdir(os.path.join(plotPath, subpath))
    #newpath = os.path.join(plotPath, subpath)
    #
    if (not os.path.isfile(os.path.join(plotPath, subpath, title + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, title + ".png"), bbox_inches="tight")
    plt.close()

def returnAllOtherDict(targetTitle, firstDay, lastDay):
    allOtherDict = dict()
    #Setup
    currDate=firstDay
    while(currDate<=lastDay):
        allOtherDict[currDate] = set()
        currDate+=timedelta(days=1)
    currDate = firstDay

    for otherTitle in dataTitleArray:
        dailyEditorSet = set()
        currDate = firstDay
        if (otherTitle != targetTitle):
            article = dataDict[otherTitle]
            sizeOfArticle = article.shape[0]
            for index, rowData in article.iterrows():
                editDay = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
                if(currDate == editDay):
                    if(rowData['userid'] == 0): #anon
                        dailyEditorSet.add("ANON " + rowData['user'])
                    else: #registered user
                        dailyEditorSet.add(rowData['userid'])
                else:
                    while(currDate<firstDay):
                        currDate += timedelta(days=1)
                    while(currDate<editDay):
                        tempSet = allOtherDict.get(currDate)
                        allOtherDict[currDate] = dailyEditorSet.union(tempSet)
                        dailyEditorSet = set()
                        currDate += timedelta(days=1)
                    if(rowData['userid'] == 0): #anon
                        dailyEditorSet.add("ANON " + rowData['user'])
                    else: #registered user
                        dailyEditorSet.add(rowData['userid'])
                if(index == (sizeOfArticle-1)):
                        tempSet = allOtherDict.get(currDate)
                        allOtherDict[currDate] = dailyEditorSet.union(tempSet)
                        dailyEditorSet = set()
    return allOtherDict

def returnTargetDict(article, firstDay, lastDay):
    dailyEditorSet = set()
    sizeOfArticle = article.shape[0]
    targetDict = dict()
    #Setup
    currDate=firstDay
    while(currDate<=lastDay):
        targetDict[currDate] = set()
        currDate+=timedelta(days=1)
    currDate = firstDay
    for index, rowData in article.iterrows():
        editDay = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
        if(currDate == editDay):
            if(rowData['userid'] == 0): #anon
                dailyEditorSet.add("ANON " + rowData['user'])
            else: #registered user
                dailyEditorSet.add(rowData['userid'])
        else:
            while(currDate<firstDay):
                currDate += timedelta(days=1)
            while(currDate<editDay):
                targetDict[currDate] = dailyEditorSet
                dailyEditorSet = set()
                currDate += timedelta(days=1)
            if(rowData['userid'] == 0): #anon
                dailyEditorSet.add("ANON " + rowData['user'])
            else: #registered user
                dailyEditorSet.add(rowData['userid'])
        if(index == (sizeOfArticle-1)):
            targetDict[currDate] = dailyEditorSet
            dailyEditorSet = set()
    return targetDict

def calculateAndPrintJaccard(days, targetDict, allOtherDict, firstDay, lastDay):
    jaccard = []
    jaccardAndEditor = [] #compiles a list of [date/jaccardScore/NumUniqueEditorsOfTargetArticle/NumUniqueEditorsOfOtherArticles] items
    currItem = []
    setB = set()
    for day in days:
        setA = targetDict[day]
        setB = setB.union(allOtherDict[day])
        if(len(setA.union(setB))==0):
            jScore = 0
        else:
            jScore = len(setA.intersection(setB))/len(setA.union(setB))*100
        jaccard.append(jScore)
        currItem.append(day)
        currItem.append(jScore)
        currItem.append(len(setA))
        currItem.append(len(setB))
        jaccardAndEditor.append(currItem)
        currItem = []
        setA = set()
    printPeaks(jaccardAndEditor, 10) #Finds top 10 peaks
    return jaccard


def printPeaks(dataInput, num):
    length = len(dataInput)
    for i in range (length):
        for j in range (0, length-i-1):
            if dataInput[j][1]<dataInput[j+1][1]:
                dataInput[j], dataInput[j+1] = dataInput[j+1], dataInput[j]
    for i in range (0, 10):
        print(dataInput[i])


'''Testing below'''
for title in dataTitleArray:
    makeDayXJaccardFigure(title)
    print(title)


sys.exit(0)
