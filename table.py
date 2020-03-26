import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
from static_helpers import *

def prettyPrint(dictKey):
    newTitle = str(dictKey)
    newTitle = newTitle.replace("Data", "").replace("_", " ").replace("(dot)",".")
    return newTitle

def formatTop(title):
    new = str(title)
    new = new.replace("Data", "")
    return new

top10 = [
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

top10 = add_talk_pages(top10)
top10 = [format_file_names(title)[:-4] for title in top10]
top10 = [formatTop(title) for title in top10]

path = "10years"
viewPath = "dailyPageviews"
titles = get_titles()
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
    if ("Data" in f):
        dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

# print(dataDict.keys())

allData = []
for key in dataDict.keys():
    if ("Data" in key):
        allData.append(dataDict[key])

table = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]

edSet = set()
topEdSet = set()
talkSet = set()
topTalkSet = set()

for key in dataDict.keys():
    if ("Talk" not in key):
        page = prettyPrint(key)
        revCount = int(dataDict[key]['revid'].count())
        edCount = int(dataDict[key]['userid'].nunique())
        edList = dataDict[key]['userid'].tolist()
        edSet.update(edList)
        if (formatTop(key) in top10):
            topEdSet.update(edList)
        talkRev = 0
        talkEd = 0
        print(key)
        # will update once pageview data collection has been done
        pageviews = 0
        for talk in dataDict.keys():
            if ("Talk" in talk and key.replace("Data","") in talk):
                print(talk)
                talkRev = int(dataDict[talk]['revid'].count())
                talkEd = int(dataDict[talk]['userid'].nunique())
                talkList = dataDict[talk]['userid'].tolist()
                talkSet.update(talkList)
                if (formatTop(talk) in top10):
                    topTalkSet.update(talkList)
        table.append([page, revCount, edCount, talkRev, talkEd, pageviews])


total = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]


tableDf = pd.DataFrame(table[1:], columns=table[0])
tableDf = tableDf.sort_values(by="Revisions", ascending=False)
# top 10 rows of dataframe
tableDf = tableDf.head(10)

revSum = tableDf['Revisions'].sum()
talkSum = tableDf['Talk Revisions'].sum()
pageSum = tableDf['Pageviews'].sum()

# sums for all pages, edit/talk
editorSum = len(edSet)
talkEditSum = len(talkSet)

totalSet = set()
totalSet.update(edSet)
totalSet.update(talkSet)
# total unique editor count for all pages including talk
totalSum = len(totalSet)

topEditorSum = len(topEdSet)
topTalkSum = len(topTalkSet)

total.append(["Total", revSum, topEditorSum, talkSum, topTalkSum, pageSum])
totalDf = pd.DataFrame(total[1:], columns=table[0])

tableDf = tableDf.append(totalDf)
# print(tableDf.to_string())
tableDf.to_csv("Table.csv", encoding="utf-8")

