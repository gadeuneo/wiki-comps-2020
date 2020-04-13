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
    newTitle = newTitle.replace("Data", "").replace("_", " ").replace("(dot)",".").replace("(colon)","-")
    return newTitle

def formatTop(title):
    new = str(title)
    new = new.replace("Data", "")
    return new

def addUnderscore(key):
    s = str(key)
    s = s.replace(" ", "_")
    return s

def formatTalk(key):
    s = str(key)
    s = s.replace("Talk-", "Talk(colon)")
    return s

#### TODO: determine top 10 metric - exclude Talk pages
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

####


path = "10 Year Revision Data"
viewPath = "dailyPageviews"

revisionFiles = os.listdir(path)


dataDict = dict()

for f in revisionFiles:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))


viewFiles = os.listdir(viewPath)

viewDict = dict()

for f in viewFiles:
    viewDict[f[:-4]] = pd.read_csv(os.path.join(viewPath, f))

# for f in viewFiles:
#     print(prettyPrint(f))
#     print(prettyPrint(f) in revisionFiles)


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
        # will update once pageview data collection has been done
        # https://stackoverflow.com/questions/10367020/compare-two-lists-in-python-and-return-indices-of-matched-values
        revIndex = [i for i, s in enumerate(revisionFiles) if key in s]
        viewIndex = [i for i, s in enumerate(viewFiles) if addUnderscore(key) in s]
        if (len(viewIndex) != 0):
            # https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
            temp = viewDict[viewFiles[viewIndex[0]][:-4]]
            temp['Date'] = pd.to_datetime(temp['Date'])
            mask = (temp['Date'] > dt.strptime("2009-12-10", "%Y-%m-%d")) & (temp['Date'] <= dt.strptime("2019-12-10", "%Y-%m-%d"))
            df = temp.loc[mask]
            pageviews = df['Count'].sum()
            # pageviews = viewDict[viewFiles[viewIndex[0]][:-4]]['Count'].sum()
        else:
            print(key + " Pageview file not found")
        for talk in dataDict.keys():
            if ("Talk" in talk and key.replace("Data","") in talk):
                talkRev = int(dataDict[talk]['revid'].count())
                talkEd = int(dataDict[talk]['userid'].nunique())
                talkList = dataDict[talk]['userid'].tolist()
                talkSet.update(talkList)
                if (formatTop(talk) in top10):
                    topTalkSet.update(talkList)
                revIndex = [i for i, s in enumerate(revisionFiles) if talk in s]
                viewIndex = [i for i, s in enumerate(viewFiles) if formatTalk(addUnderscore(talk)) in s]
                # if (len(viewIndex) != 0):
                #     pageviews += viewDict[viewFiles[viewIndex[0]][:-4]]['Count'].sum()
                # else:
                #     print(talk + " pageview file not found")
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

