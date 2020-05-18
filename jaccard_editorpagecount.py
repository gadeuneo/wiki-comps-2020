
'''
    Plots Pagecount vs Number of Editors graph, with pagecount normalized (pagecount/active pages)
    And Number of Editors log-transformed

    Written by Junyi Min. Updated by James Gardner to work with new data folders.
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
import matplotlib.dates as mdates
from static_helpers import *
import math


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

#Returns two items: a dictionary with Editor Names as keys and a Set of Pages they edit in as values.
# and a set of all unique editors
def getEditorPageDict():
    editorPageDict = dict()
    editorSet = set()
    currPgSet = set()
    for title in revisionDict.keys():
        article = revisionDict[title]
        for index, rowData in article.iterrows():
            currDate = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
            if(currDate >= startDate and currDate <= endDate):
                if(rowData['userid'] != 0): #not anon
                    user = rowData['user']
                    if(editorPageDict.get(user) == None):
                        editorSet.add(user)
                        currPgSet = set()
                        currPgSet.add(title)
                        editorPageDict[user] = currPgSet
                        currPgSet = set()
                    else:
                        currPgSet = editorPageDict.get(user)
                        currPgSet.add(title)
                        editorPageDict[user] = currPgSet
                        currPgSet = set()
    return [editorPageDict, editorSet]

#Converts the dictionary into a list, sorts it by length
def getEditorPageList():
    resultList = getEditorPageDict()
    dictionary = resultList[0]
    editorSet = resultList[1]
    returnList = []
    for editor in editorSet:
        pages = dictionary.get(editor)
        returnList.append([editor, pages])
    return (bubbleSortList(returnList))

# get editor - page COUNT in a list
def getEditorPagecount():
    resultList = getEditorPageList()
    for item in resultList:
        item[1] = len(item[1])
    return resultList

#Bubble sorts a list of dictionary pairs
def bubbleSortList(dataInput):
    length = len(dataInput)
    for i in range (length):
        for j in range (0, length-i-1):
            if len(dataInput[j][1])>len(dataInput[j+1][1]):
                dataInput[j], dataInput[j+1] = dataInput[j+1], dataInput[j]
    return dataInput

#Makes a multiline pagecount vs editors over time graph that is logtransformed
def makeMultiLineGraph():
    data = getPlotData()
    print(data)
    yAxis = logTransform(data[1])
    plt.plot(data[0], yAxis, label= endDate)
    plt.gcf().set_size_inches(15,7)
    figureTitle = "Log-Transformed - Pagecount VS Editors over time ending" + str(endDate)
    plt.title(figureTitle)
    plt.xlabel("Number of Pages Editors Edit In")
    plt.ylabel("Number of Editors")

    subpath = "Jaccard"
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    # Need to add subpath so that its easier to change which directory being used
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()

#Gets the data to plot in Editor/Pagecount graph
#Returns xAxisElements: a list of pagecounts
#And also yAxisElements: a list of number of editors that edit with that specific pagecount
def getPlotData():
    list = getEditorPagecount()
    myDict = dict()
    for item in list:
        if(myDict.get(item[1])==None):
            myDict[item[1]] = 1
        else:
            myDict[item[1]] += 1

    xAxisElements = []
    yAxisElements = []
    for key, value in myDict.items():
        xAxisElements.append(key)
        yAxisElements.append(value)
    returnVal = [xAxisElements, yAxisElements]
    return returnVal

#Plots the number of editors that edit a certain amount of pages
def makePagecountVSNumOfEditors():
    list = getEditorPagecount()
    myDict = dict()
    for item in list:
        if(myDict.get(item[1])==None):
            myDict[item[1]] = 1
        else:
            myDict[item[1]] += 1

    xAxisElements = []
    yAxisElements = []
    for key, value in myDict.items():
        xAxisElements.append(key)
        yAxisElements.append(value)
    fig, ax = plt.subplots(figsize=(15,4))
    ax.plot(xAxisElements, yAxisElements)

    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    #ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    #ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    #ax.format_xdata = mdates.DateFormatter('%Y-%m')
    figureTitle = "Pagecount VS Editors ending " + str(endDate)
    fig.autofmt_xdate()
    plt.title(figureTitle)
    #plt.suptitle("10 year aggregate data. Shows number of edits per week in 6 month intervals.")
    plt.xlabel("Number of Pages Editors Edit In")
    plt.ylabel("Number of Editors (10^x)")

    subpath = "Jaccard"
    #
    #os.mkdir(os.path.join(plotPath, subpath))
    #newpath = os.path.join(plotPath, subpath)
    #
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()

#Log transforms a set of data
def logTransform(data):
    returnData = []
    for item in data:
        returnData.append(math.log(item, 10))
    return returnData

#Normalizes pagecount data by returning a list of data with pagecount divided by number of active articles
def normalize(data, date):
    returnData = []
    for item in data:
        returnData.append(item/numActiveArticleDict.get(date))
    return returnData


#For Nomalization of Data - produces a dictionary of the number of active articles each day
start = "2009-01-10"
end = "2019-12-10"
startDate = dt.fromtimestamp(int(time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple()))).date()
endDate = dt.fromtimestamp(int(time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple()))).date()
numActiveArticleDict = dict()
for title in revisionDict.keys():
    article = revisionDict[title]
    rowData = article.loc[0]
    time = dt.strptime(rowData['timestamp'], "%Y-%m-%dT%H:%M:%SZ").date()
    while(time <= endDate):
        if(numActiveArticleDict.get(time)==None):
            numActiveArticleDict[time] = 1
        else:
            numActiveArticleDict[time] = numActiveArticleDict.get(time)+1
        time += timedelta(days=1)


#MultiLineGraph Code Below - moved here due to global variable problems
graphColor = ['#000000','#003300','#005900','#198c19','#7fbf7f','#e5f2e5',    #green
              '#330033', '#590059', '#800080', '#a64ca6', '#cc99cc', '#f2e5f2'] #purple
'''
start = "2009-01-10"
end = "2019-12-10"
startDate = dt.fromtimestamp(int(time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple()))).date()
endDate = dt.fromtimestamp(int(time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple()))).date()'''

for i in range (0, 12):
    data = getPlotData()
    xAxis = normalize(data[0], endDate)
    yAxis = logTransform(data[1])
    plt.plot(xAxis, yAxis,graphColor[i],label= endDate)
    plt.gcf().set_size_inches(15,7)
    endDate -= relativedelta(months=+1)
figureTitle = "Normalized - Page Count vs Number Editors"
plt.title(figureTitle)
plt.xlabel("Pages Editted/Active Pages")
plt.ylabel("Number of Editors (in log base 10)")

subpath = "Jaccard"
ax = plt.subplot(111)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
    plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
plt.close()
#MultiLineGraph Code ends

sys.exit(0)
