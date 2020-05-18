'''
    Plots fraction of top 10 pages' editors that
    edit a page on the non-top 10 pages.

    Written by Kirby Mitchell
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
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
import copy
from static_helpers import *

register_matplotlib_converters()
start = time.time()

# folder of files
path = "10 Year Revision Data"
plotPath = "figures"
startDatePath = "creation/creation_dates.csv"

directories = ["figures"]

create_directories(directories)

# working list of Wiki pages
titles = get_titles()

titles = add_revision_talk_pages(titles)

titles = [add_file_extension(title) for title in titles]
titleArray = []
for title in titles:
    if title[0:4] != "Talk":
        titleArray.append(title)

dataDict = dict()
startDateDict = dict()

# Holds the data from csv files for articles in our corpus.
for f in titleArray:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

# Dictionary to hold article start dates. Article title is the key, start date is value.
file = pd.read_csv(os.path.join(startDatePath))
file["Page Creation Date"] = pd.to_datetime(file["Page Creation Date"])
for title, startDay in zip(file['Titles'], file['Page Creation Date']):
    startDay = startDay.date()
    startDateDict[title] = startDay

allData = []
allRed = []
for key in dataDict.keys():
    if ("Data" in key):
        allData.append(dataDict[key])
    else:
        allRed.append(dataDict[key])

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))

# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# Pulls editors from top 10 articles.
topTenEditorSet = set()
for title in titleArray[:10]:
    key = title[:-4]
    if key[0:4]!="Talk":
        article = dataDict[key]
        for user in article['user']:
            topTenEditorSet.add(user)

# Set to hold editors that edited on a given date
dailyEditorSet = set()
# Run through the non-top ten articles
for title in titleArray[11:]:
    key = title[:-4]
    if key[0:4] != "Talk":
        article = dataDict[key]
        sizeOfArticle = article.shape[0]
        newDate = dt.fromtimestamp(startDate)
        nextTimeDate = newDate.date()
        days = []
        editorFraction = []
        dayCount = 0
        prevEditTimeDate = startDate
        for day, editor in zip(article['timestamp'], article['user']):
            dayCount += 1
            editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
            # Floor Date here
            editTimeDate = editTime.date()
            # While nextTimeDate does not equal the editTimeDate taken from the csv file, increment nextTimeDate
            # it is possible this will miss the very last one since it only adds to the list if newTimeDate goes
            # beyond editTimeDate
            while(editTimeDate != nextTimeDate):
                newDate = newDate + timedelta(days=1)
                nextTimeDate = newDate.date()
                # if set is empty, don't add values
                if len(dailyEditorSet) != 0:
                    # Encountered a bug after creation_dates.csv was changed.
                    # had to have an edge case for negative relative dates.
                    dayDiff = prevEditTimeDate - startDateDict[key]
                    dayDiff = dayDiff.total_seconds() / 86400
                    if dayDiff >= 0:
                        # Calculates the fraction of editors that are from
                        # top ten articles and calculates the days since
                        # article creation. Pairs them together in separate
                        # lists for plotting later.
                        intersectionEditors = topTenEditorSet.intersection(dailyEditorSet)
                        fractionOfEditors = len(intersectionEditors) / len(topTenEditorSet)
                        editorFraction.append(fractionOfEditors)
                        days.append(dayDiff)
                        dailyEditorSet.clear()
                    else:
                        dailyEditorSet.clear()

            prevEditTimeDate = editTimeDate
            dailyEditorSet.add(editor)
            # Not an elegant way to handle edge case of last editTimeDate from csv file
            if dayCount == sizeOfArticle:
                # Calculates the fraction of editors that are from
                # top ten articles and calculates the days since
                # article creation. Pairs them together in separate
                # lists for plotting later.
                intersectionEditors = topTenEditorSet.intersection(dailyEditorSet)
                fractionOfEditors = len(intersectionEditors) / len(topTenEditorSet)
                editorFraction.append(fractionOfEditors)
                dayDiff = prevEditTimeDate - startDateDict[key]
                dayDiff = dayDiff.total_seconds() / 86400
                days.append(dayDiff)
                dailyEditorSet.clear()

        plt.plot(days, editorFraction, label=key)
        plt.gcf().set_size_inches(15,7)
        
# Plots graph.
# Leave as plt.title(key) for individual graphs
plt.xlabel("Days Since Article Creation")
plt.ylabel("Fraction of Editors")
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
plt.savefig("figures/New Top Ten Editors Fraction", bbox_inches="tight")
plt.close()
