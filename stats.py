'''
File for manipulating data.

James Gardner
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
#uhuh
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
#uhuh
import copy

register_matplotlib_converters()
start = time.time()

# folder of files
path = "data"
plotPath = "figures"

if (not os.path.exists(plotPath)):
    os.mkdir(plotPath)

# working list of Wiki pages
titles = [
    "2019–20 Hong Kong protests",
    "Hong Kong",
    "2019 Hong Kong extradition bill",
    "Government of Hong Kong",
    "Murder of Poon Hiu-wing",
    "One country, two systems",
    "Demosistō",
    "Hong Kong 1 July marches",
    "Civil Human Rights Front",
    "Hong Kong Human Rights and Democracy Act",
    "Chinese University of Hong Kong conflict",
    "Death of Chow Tsz-lok",
    "Siege of the Hong Kong Polytechnic University",
    "2019 Yuen Long attack",
    "Hong Kong–Mainland China conflict",
    "Storming of the Legislative Council Complex",
    "Hong Kong Way",
    "2019 Prince Edward station attack",
    "Death of Chan Yin-lam",
    "2019 Hong Kong local elections",
    "List of protests in Hong Kong",
    "Police misconduct allegations during the 2019–20 Hong Kong protests",
    "Art of the 2019–20 Hong Kong protests",
    "12 June 2019 Hong Kong protest",
    "Umbrella Movement",
    "Causes of the 2019–20 Hong Kong protests",
    "Tactics and methods surrounding the 2019–20 Hong Kong protests",
    "Carrie Lam",
    "Reactions to the 2019–20 Hong Kong protests",
    "List of early 2019 Hong Kong protests",
    "List of July 2019 Hong Kong protests",
    "List of August 2019 Hong Kong protests",
    "List of September 2019 Hong Kong protests",
    "List of October 2019 Hong Kong protests",
    "List of November 2019 Hong Kong protests",
    "List of December 2019 Hong Kong protests",
    "List of January 2020 Hong Kong protests",
    "Glory to Hong Kong",
    "Lennon Wall (Hong Kong)",
    "HKmap.live",
    "Killing of Luo Changqing"
]

# adds talk pages
for i in range(len(titles)):
    titles.append("Talk:" + titles[i])

# converts titles to filename format
titles = [title.replace(" ","_").replace(".","(dot)").replace(":", "(colon)") + ".csv" for title in titles]
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


##### TODO: merge files? -- Which ones? How?
##### TODO: save merged files?


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

revisionData = pd.concat(allData, ignore_index=True, sort=False)
revisionData['timestamp'] = pd.to_datetime(revisionData['timestamp'])
revisionData.sort_values(by='timestamp')
revisionData['timestamp'] = revisionData['timestamp'].astype(str)
#revisionData['timestamp'] = revisionData['timestamp'][:-6]
#print(revisionData.to_string())

# Convert date to Unix Timestamp
startDate = int(time.mktime(dt.strptime("2019-06-10", "%Y-%m-%d").timetuple()))
endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
today = int(time.mktime(dt.today().timetuple()))
# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)

# TODO: loop over timestamps and get count for each (day/week/month?)

# test get next day epoch time

def makeTimeXRevisionFigure(article, title):
    newDate = dt.fromtimestamp(startDate)
    days = []
    counts = []
    #counts the edits
    edits = 0
    for day in article['timestamp']:
        editTime = dt.strptime(day, "%Y-%m-%dT%H:%M:%SZ")
        while(editTime > newDate):
            counts.append(edits)
            epoch = int(newDate.timestamp())
            days.append(dt.fromtimestamp(epoch))
            newDate = newDate + timedelta(days=1)
            edits = 0
        edits += 1
    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(days, counts)

    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')

    fig.autofmt_xdate()

    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Number Edits")
    if (not os.path.isfile(os.path.join(plotPath, title+".png"))):
        fig.savefig(os.path.join(plotPath, title+".png"), bbox_inches="tight")
    plt.close()

#separate out "DATA-" articles from "REVISION-", without the .csv
dataTitleArray = []
for title in titleArray:
    if title[0:4] == "Data":
        dataTitleArray.append(title[:-4])

# makes all Time-RevisionNumber figures
'''
for title in titleArray:
    key = title[:-4]
    if key[0:4]=="Data":
        article = dataDict[key]
        makeTimeXRevisionFigure(article, key)
'''

makeTimeXRevisionFigure(revisionData, "REEEEEEEEEEEEEE")


##### TODO: Make plots
#### https://matplotlib.org/tutorials/introductory/pyplot.html

### SAMPLE CODE
# https://towardsdatascience.com/matplotlib-tutorial-learn-basics-of-pythons-powerful-plotting-library-b5d1b8f67596

# plots x values, then y values
plt.plot([1,2,3,4], [1,4,9,16])
plt.title("Sample plot")
plt.xlabel("Sample x axis label")
plt.ylabel("Sample y axis label")

if (not os.path.isfile(os.path.join(plotPath, "sample.png"))):
    plt.savefig(os.path.join(plotPath, "sample.png"), bbox_inches="tight")


end = time.time()
print("Time Elapsed: " + str(end-start))

sys.exit(0)
