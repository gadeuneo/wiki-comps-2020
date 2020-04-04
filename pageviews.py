'''
Creates figures for pageviews.

James Gardner
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

# functions that are frequently accessed by other files
from static_helpers import *

path = "dailyPageviews"

figPath = "pageviews"

savepath = os.path.join("figures", figPath)

if (not os.path.exists(savepath)):
    os.mkdir(savepath)

topNCorr = [
    "List_of_December_2019_Hong_Kong_Protests",
    "Murder_of_Poon_Hiu-wing",
    "12_June_2019_Hong_Kong_protest",
    "Death_of_Chow_Tsz-lok",
    "List_of_protests_in_Hong_Kong",
    "Hong_Kong–Mainland_China_conflict",
    "Police_misconduct_allegations_during_the_2019–20_Hong_Kong_protests",
    "Reactions_to_the_2019–20_Hong_Kong_protests"
]

views = dict()

startDate = dt.strptime("2019-6-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")
today = dt.today()

for f in os.listdir(path):
    views[f[:-4]] = pd.read_csv(os.path.join(path, f))

# What is this? - borrowed from multiline.py
register_matplotlib_converters()



def plotPageviews(pageDict):
    for key in pageDict.keys():
        days = []
        numViews = []
        for index, row in pageDict[key].iterrows():
            viewDate = dt.strptime(row['Date'], "%Y-%m-%d")
            days.append(viewDate)
            numViews.append(row['Count'])

        plt.plot(days, numViews)
        plt.title(key)
        plt.xlabel("Days")
        plt.ylabel("Pageview Count")
        plt.savefig(os.path.join(savepath, key + ".png"), dpi=300)
        plt.close()

plotPageviews(views)

def plotTopNPageviews(pageDict):
    allDays = []
    allNumViews = []
    for key in pageDict.keys():
        if (key in topNCorr):
            days = []
            numViews = []
            for index, row in pageDict[key].iterrows():
                viewDate = dt.strptime(row['Date'], "%Y-%m-%d")
                if (viewDate > dt.strptime("2019-01-01", "%Y-%m-%d")):
                    days.append(viewDate)
                    numViews.append(row['Count'])

            allDays.append(days)
            allNumViews.append(numViews)
    for i in range(len(allDays)):
        plt.plot(allDays[i], allNumViews[i])
    plt.title("Top N Pageviews Corr")
    plt.xlabel("Days")
    plt.ylabel("Pageview Count")
    plt.savefig(os.path.join(savepath,"TopNPageviewCorrSince2019.png"), dpi=300)
    plt.close()

plotTopNPageviews(views)