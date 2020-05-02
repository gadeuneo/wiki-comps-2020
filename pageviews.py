'''
    Plots pageviews for top 4 most correlated pages.

    Written by James Gardner
'''

import pandas as pd
from pandas.plotting import register_matplotlib_converters
import os
import sys
import requests as rq
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker

# what does this do?
register_matplotlib_converters()

# functions that are frequently accessed by other files
from static_helpers import *

start = time.time()

path = "dailyPageviews"

figPath = "pageviews"

savepath = os.path.join("figures", figPath)

if (not os.path.exists(savepath)):
    os.mkdir(savepath)

topNCorr = [
    "List_of_December_2019_Hong_Kong_protests",
    "Murder_of_Poon_Hiu-wing",
    "12_June_2019_Hong_Kong_protest",
    "Death_of_Chow_Tsz-lok",
    "2019–20_Hong_Kong_protests"
    # "List_of_protests_in_Hong_Kong",
    # "Hong_Kong–Mainland_China_conflict",
    # "Police_misconduct_allegations_during_the_2019–20_Hong_Kong_protests",
    # "Reactions_to_the_2019–20_Hong_Kong_protests"
]

views = dict()

startDate = dt.strptime("2019-6-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")

for f in os.listdir(path):
    views[f[:-4]] = pd.read_csv(os.path.join(path, f))

# What is this? - borrowed from multiline.py
register_matplotlib_converters()



def plotPageviews(pageDict):
    for key in pageDict.keys():
        days = []
        numViews = []

        temp = pageDict[key]
        temp['Date'] = pd.to_datetime(temp['Date'])
        mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
        df = temp.loc[mask]
        days = df['Date'].tolist()
        numViews = df['Count'].tolist()

        plt.plot(days, numViews)
        plt.title(key)
        plt.xlabel("Days")
        plt.ylabel("Pageview Count")
        plt.savefig(os.path.join(savepath, key + ".png"), dpi=300)
        plt.close()

plotPageviews(views)

endPage = time.time()
print("Plotting pageviews took {0} seconds.".format(str(endPage - start)))

def plotTopNPageviews(pageDict):
    allDays = []
    allNumViews = []
    keyNames = []
    for key in pageDict.keys():
        if (key in topNCorr):
            days = []
            numViews = []
            temp = pageDict[key]
            temp['Date'] = pd.to_datetime(temp['Date'])
            mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
            df = temp.loc[mask]
            days = df['Date'].tolist()
            numViews = df['Count'].tolist()
            keyNames.append(key)
            # for index, row in pageDict[key].iterrows():
            #     viewDate = dt.strptime(row['Date'], "%Y-%m-%d")
            #     if (viewDate >= dt.strptime("2019-06-01", "%Y-%m-%d") and viewDate <= dt.strptime("2019-12-10", "%Y-%m-%d")):
            #         days.append(viewDate)
            #         numViews.append(row['Count'])

            allDays.append(days)
            allNumViews.append(numViews)
    for i in range(len(allDays)):
        plt.plot(allDays[i], allNumViews[i], label=keyNames[i])
    plt.title("Top N Pageviews Corr")
    plt.xlabel("Days")
    plt.ylabel("Pageview Count")
    plt.yscale("log")
    plt.legend()
    plt.savefig(os.path.join("figures","TopNPageviewCorrSince2019.png"), dpi=300)
    plt.close()

plotTopNPageviews(views)
endTop = time.time()
print("Plotting top pageviews took {0} seconds".format(str(endTop - endPage)))