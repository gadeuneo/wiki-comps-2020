
'''
    Plots Jaccard similarity multiline graph for Top 10 Articles.
    Plots Jaccard similarity graph for a target article
    Written by Junyi Min. Updated by James Gardner.
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

# taken from table.csv
top = [
    "2019–20 Hong Kong protests",
    "Hong Kong",
    "Carrie Lam",
    "2019 Hong Kong extradition bill",
    "2019 Hong Kong local elections",
    "Reactions to the 2019–20 Hong Kong protests",
    "2019 Yuen Long attack",
    "Tactics and methods surrounding the 2019–20 Hong Kong protests",
    "One country, two systems",
    "Umbrella Movement"
]
topData = dict()
for f in top:
    topData[f] = pd.read_csv(os.path.join(path, f+".csv"))


# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)


#Makes multiline plot for jaccard similarity for Top 10 Articles
def makeTop10Figures():
    for i in range (0, 10): #top ten articles is first 10 in the list
        title = list(topData.keys())[i]
        data = top10Helper(title)
        plt.plot(data[0], data[1],label= prettyPrint(title))
        plt.gcf().set_size_inches(15,7)
    plt.ylim([0, 3])

    figureTitle = "Top 10 Article's Jaccard Scores"
    plt.title(figureTitle)
    plt.xlabel("Days")
    plt.ylabel("Jaccard Score (%)")

    subpath = "Jaccard"
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')
    '''
    startNum = int(time.mktime(dt.strptime("2019-06-10", "%Y-%m-%d").timetuple()))
    endNum = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
    ax.set_xlim([startNum, endNum])
    '''
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()

#Takes in an article title and returns a list of dates and its corresponding Jaccard score for the specific article
def top10Helper(title):
    article = topData[title]
    firstDay = dt.fromtimestamp(int(time.mktime(dt.strptime("2019-05-01", "%Y-%m-%d").timetuple()))).date()
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

    answer = [days, jaccard]

    return answer

# Makes jaccard score for a target article
def makeDayXJaccardFigure(title):
    article = revisionDict[title]
    firstDay = dt.fromtimestamp(int(time.mktime(dt.strptime("2018-12-10", "%Y-%m-%d").timetuple()))).date()
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

#Receives targetTitle, the target article's title, and returns a dictionary
#Where the key is a date, and the value is the set of editors that edits in all
#non-target articles on that date
#Firstday and lastday represents the start and end of analysis for sanity check
def returnAllOtherDict(targetTitle, firstDay, lastDay):
    allOtherDict = dict()
    #Setup
    currDate=firstDay
    while(currDate<=lastDay):
        allOtherDict[currDate] = set()
        currDate+=timedelta(days=1)
    currDate = firstDay

    for otherTitle in revisionDict:
        dailyEditorSet = set()
        currDate = firstDay
        article = revisionDict[otherTitle]
        sizeOfArticle = article.shape[0]
        for index, rowData in article.iterrows():
            editDay = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
            if(currDate == editDay):
                if(rowData['userid'] == 0): #anon
                    p=0
                    #dailyEditorSet.add("ANON " + rowData['user'])
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
                    p=0
                    #dailyEditorSet.add("ANON " + rowData['user'])
                else: #registered user
                    dailyEditorSet.add(rowData['userid'])
            if(index == (sizeOfArticle-1)):
                    tempSet = allOtherDict.get(currDate)
                    allOtherDict[currDate] = dailyEditorSet.union(tempSet)
                    dailyEditorSet = set()
    return allOtherDict


#Receives targetTitle, the target article's title, and returns a dictionary
#Where the key is a date, and the value is the set of editors that edits in
#the target article on that date.
#Firstday and lastday represents the start and end of analysis for sanity check
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
                p = 0
                #dailyEditorSet.add("ANON " + rowData['user'])
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
                p = 0
                #dailyEditorSet.add("ANON " + rowData['user'])
            else: #registered user
                dailyEditorSet.add(rowData['userid'])
        if(index == (sizeOfArticle-1)):
            targetDict[currDate] = dailyEditorSet
            dailyEditorSet = set()
    return targetDict

#Using the parameters, calculates the Jaccard score for the target articles
#And returns a list of Jaccard score corresponding to the order of the dates in
#input "days"
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
    return jaccard

'''Testing below'''
makeTop10Figures()

sys.exit(0)
