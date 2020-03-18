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


path = "10years"
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

# TODO grab data and make table

table = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]

for key in dataDict.keys():
    if ("Talk" not in key):
        page = prettyPrint(key)
        revCount = int(dataDict[key]['revid'].count())
        edCount = int(dataDict[key]['userid'].nunique())
        talkRev = 0
        talkEd = 0
        # will update once pageview data collection has been done
        pageviews = 0
        for talk in dataDict.keys():
            if ("Talk" in talk and key.replace("Data","") in talk):
                talkRev = int(dataDict[talk]['revid'].count())
                talkEd = int(dataDict[talk]['userid'].nunique())
        table.append([page, revCount, edCount, talkRev, talkEd, pageviews])


total = [["Article", "Revisions", "Editors (unique)", "Talk Revisions", "Talk Editors", "Pageviews"]]


tableDf = pd.DataFrame(table[1:], columns=table[0])
tableDf = tableDf.sort_values(by="Revisions", ascending=False)

revSum = tableDf['Revisions'].sum()
talkSum = tableDf['Talk Revisions'].sum()
pageSum = tableDf['Pageviews'].sum()

# Working -- need to separate talk pages out
editorSum = 0
talkEditSum = 0


total.append(["Total", revSum, editorSum, talkSum, talkEditSum, pageSum])
totalDf = pd.DataFrame(total[1:], columns=table[0])

tableDf = tableDf.append(totalDf)
# print(tableDf.to_string())
tableDf.to_csv("Table.csv", encoding="utf-8")

