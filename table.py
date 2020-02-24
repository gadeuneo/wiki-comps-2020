import pandas as pd
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
from static_helpers import *

path = "10years"
titles = get_titles()
titles = add_talk_pages(titles)

# converts titles to filename format
titles = [formatFileNames(title) for title in titles]
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

# print(dataDict.keys())

allData = []
allRed = []
for key in dataDict.keys():
    if ("Data" in key):
        allData.append(dataDict[key])
    else:
        allRed.append(dataDict[key])

# TODO grab data and make table

table = [["Article", "Num Revisions", "Num Editors (unique)"]]

for key in dataDict.keys():
    if ("Data" in key):
        table.append([key, dataDict[key]['revid'].count(), dataDict[key]['userid'].nunique()])

tableDf = pd.DataFrame(table[1:], columns=table[0])
tableDf.sort_values(by="Num Revisions", inplace=False)
tableDf.to_csv("Table.csv", encoding="utf-8")

