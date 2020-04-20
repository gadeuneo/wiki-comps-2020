'''
    Creates pre-analysis table of data.
    Includes totals for the top 10 pages by revision count
    (not including Talk pages).
    Also has grand totals (including Talk pages).
'''

import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
from static_helpers import *

# Helper functions to compare files of pageviews and revisions
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


path = "10 Year Revision Data"
viewPath = "dailyPageviews"

revisionFiles = os.listdir(path)
viewFiles = os.listdir(viewPath)

dataDict = dict()
for f in revisionFiles:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

viewDict = dict()
for f in viewFiles:
    viewDict[f[:-4]] = pd.read_csv(os.path.join(viewPath, f))

# for f in viewFiles:
#     print(prettyPrint(f))
#     print(prettyPrint(f) in revisionFiles)


table = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]

edSets = dict()
talkSets = dict()

talkPageviews = 0

startDate = dt.strptime("2009-12-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")

for key in dataDict.keys():
    if ("Talk" not in key):
        page = prettyPrint(key)
        revDict = dataDict[key]
        revDict['timestamp'] = pd.to_datetime(revDict['timestamp'])
        revDict['timestamp'] = revDict['timestamp'].dt.tz_localize(None)
        mask = (revDict['timestamp'] >= startDate) & (revDict['timestamp'] <= endDate)
        revDict = revDict.loc[mask]

        revCount = int(revDict['revid'].count())
        edCount = int(revDict['userid'].nunique())
        edList = revDict['userid'].tolist()

        # revCount = int(dataDict[key]['revid'].count())
        # edCount = int(dataDict[key]['userid'].nunique())
        # edList = dataDict[key]['userid'].tolist()
        edSets[key] = set(edList)
        talkRev = 0
        talkEd = 0
        # Pageview totals
        # https://stackoverflow.com/questions/10367020/compare-two-lists-in-python-and-return-indices-of-matched-values
        revIndex = [i for i, s in enumerate(revisionFiles) if key in s]
        viewIndex = [i for i, s in enumerate(viewFiles) if addUnderscore(key) in s]
        if (len(viewIndex) != 0):
            # https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
            temp = viewDict[viewFiles[viewIndex[0]][:-4]]
            temp['Date'] = pd.to_datetime(temp['Date'])
            mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
            df = temp.loc[mask]
            pageviews = df['Count'].sum()
            # pageviews = viewDict[viewFiles[viewIndex[0]][:-4]]['Count'].sum()
        else:
            print(key + " Pageview file not found")
        for talk in dataDict.keys():
            if ("Talk" in talk and key.replace("Data","") in talk):
                revDict = dataDict[key]
                revDict['timestamp'] = pd.to_datetime(revDict['timestamp'])
                mask = (revDict['timestamp'] >= startDate) & (revDict['timestamp'] <= endDate)
                revDict = revDict.loc[mask]

                talkRev = int(revDict['revid'].count())
                talkEd = int(revDict['userid'].nunique())
                talkList = revDict['userid'].tolist()
                talkSets[key] = set(talkList)

                # talkRev = int(dataDict[talk]['revid'].count())
                # talkEd = int(dataDict[talk]['userid'].nunique())
                # talkList = dataDict[talk]['userid'].tolist()
                revIndex = [i for i, s in enumerate(revisionFiles) if talk in s]
                viewIndex = [i for i, s in enumerate(viewFiles) if formatTalk(addUnderscore(talk)) in s]
                if (len(viewIndex) != 0):
                    temp = viewDict[viewFiles[viewIndex[0]][:-4]]
                    temp['Date'] = pd.to_datetime(temp['Date'])
                    mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
                    df = temp.loc[mask]
                    talkPageviews += df['Count'].sum()
                    # talkPageviews += viewDict[viewFiles[viewIndex[0]][:-4]]['Count'].sum()
                # else:
                #     print(talk + " pageview file not found")
        table.append([page, revCount, edCount, talkRev, talkEd, pageviews])

topEdSet = set()
topTalkSet = set()

total = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]
grandTotal = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]

tableDf = pd.DataFrame(table[1:], columns=table[0])
tableDf = tableDf.sort_values(by="Revisions", ascending=False)
# top 10 rows of dataframe
top = tableDf.head(10)

revSum = tableDf['Revisions'].sum()
talkSum = tableDf['Talk Revisions'].sum()
pageSum = tableDf['Pageviews'].sum()

# sums for all pages, edit/talk
for k in dataDict.keys():
    if (prettyPrint(k) in top['Article']):
        topEdSet.update(edSets[k])

editorSum = len(topEdSet)
talkEditSum = len(topTalkSet)

# TODO: get total for top 10 pages
# totalSet = set()
# totalSet.update(edSet)
# totalSet.update(talkSet)

# total unique editor count for all pages including talk
# totalSum = len(totalSet)

topEditorSum = len(topEdSet)
topTalkSum = len(topTalkSet)

total.append(["Total of Top 10 pages by Revision Count", revSum, topEditorSum, talkSum, topTalkSum, pageSum])
totalDf = pd.DataFrame(total[1:], columns=table[0])

tableDf = tableDf.append(totalDf)
# print(tableDf.to_string())
tableDf.to_csv("Table.csv", encoding="utf-8")

