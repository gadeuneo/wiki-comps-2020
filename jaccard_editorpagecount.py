
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

#Returns two items: a dictionary with Editor Names as keys and a Set of Pages they edit in as values.
# and a set of all unique editors
def getEditorPageDict():
    editorPageDict = dict()
    editorSet = set()
    currPgSet = set()
    for title in dataTitleArray:
        article = dataDict[title]
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

def printAveragePages():
    sum = 0
    resultList = getEditorPagecount()
    size = len(resultList)
    for item in resultList:
        sum += item[1]
    print(sum/size)

def printMedianPages():
    resultList = getEditorPagecount()
    size = len(resultList)
    size = int(size/2)
    print(resultList[size])


def bubbleSortList(dataInput):
    length = len(dataInput)
    for i in range (length):
        for j in range (0, length-i-1):
            if len(dataInput[j][1])>len(dataInput[j+1][1]):
                dataInput[j], dataInput[j+1] = dataInput[j+1], dataInput[j]
    return dataInput

def makeMultiLineGraph(start, end):
    startDate = dt.fromtimestamp(int(time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple()))).date()
    endDate = dt.fromtimestamp(int(time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple()))).date()

    for i in range (0, 6):
        endDate += relativedelta(months=+1)
        data = getPlotData()
        plt.plot(data[0], data[1], label= endDate)
        plt.gcf().set_size_inches(15,7)
    figureTitle = "Pagecount VS Editors over time"
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
    plt.ylabel("Number of Editors")

    subpath = "Jaccard"
    #
    #os.mkdir(os.path.join(plotPath, subpath))
    #newpath = os.path.join(plotPath, subpath)
    #
    if (not os.path.isfile(os.path.join(plotPath, subpath, figureTitle + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, figureTitle + ".png"), bbox_inches="tight")
    plt.close()
'''Testing below'''
start = "2009-01-01"
end = "2019-6-01"
startDate = dt.fromtimestamp(int(time.mktime(dt.strptime(start, "%Y-%m-%d").timetuple()))).date()
endDate = dt.fromtimestamp(int(time.mktime(dt.strptime(end, "%Y-%m-%d").timetuple()))).date()
makeMultiLineGraph(start, end)
#print(getEditorPageList()) # prints Editor along with the pages they editted, sorted\
#printAveragePages()
sys.exit(0)
