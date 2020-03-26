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