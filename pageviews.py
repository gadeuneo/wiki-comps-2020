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
import time
import matplotlib.pyplot as plt
# format x-axis date labels
# https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/date.html
import matplotlib.dates as mdates


# functions that are frequently accessed by other files
from static_helpers import *

start = time.time()

path = "dailyPageviews"

figPath = "pageviews"

savepath = os.path.join("figures", figPath)

if (not os.path.exists(savepath)):
    os.mkdir(savepath)

# taken from correlation.py results
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

# taken from aggregate plots
agg = [
    "2019–20_Hong_Kong_protests",
    "Umbrella_Movement",
    "One_country,_two_systems",
    "Hong_Kong",
    "Causes_of_the_2019–20_Hong_Kong_protests",
    "Reactions_to_the_2019–20_Hong_Kong_protests"
]

startDate = dt.strptime("2019-6-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")

# dictionary of files; key = filename, value = pandas DataFrame of csv
views = dict()
for f in os.listdir(path):
    views[f[:-4]] = pd.read_csv(os.path.join(path, f))


# datetime converter for a matplotlib plotting method
register_matplotlib_converters()

'''
    Plots daily pageviews per page.
    Also aggregate for all pages.
'''

def plotPageviews(pageDict):
    allDays = []
    allNumViews = []
    keyNames = []
    focal = []
    for key in pageDict.keys():
        days = []
        numViews = []

        temp = pageDict[key]
        temp['Date'] = pd.to_datetime(temp['Date'])
        # https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
        mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
        df = temp.loc[mask]
        days = df['Date'].tolist()
        numViews = df['Count'].tolist()

        if (key == "2019–20_Hong_Kong_protests"):
            focal = [prettyPrint(key), days, numViews]
        elif ("Talk" not in key):
            keyNames.append(prettyPrint(key))
            allDays.append(days)
            allNumViews.append(numViews)

        plt.plot(days, numViews)
        plt.title(prettyPrint(key))
        plt.xlabel("Days")
        plt.ylabel("Pageview Count")
        plt.savefig(os.path.join(savepath, key + ".png"), dpi=300)
        plt.close()
        
    # aggregate plots
    section = 1
    while (len(allDays) != 0):
        even = False
        for i in range(len(allDays)):
            if (((i +1) % 5) != 0):
                even = False
                plt.plot(allDays.pop(), allNumViews.pop(), label=keyNames.pop())
            else:
                even = True
                plt.plot(focal[1], focal[2], label=focal[0])
                months = mdates.MonthLocator()  # every month
                fmt = mdates.DateFormatter('%B')
                plt.ylabel("Pageviews")
                plt.yscale("log")
                plt.xlabel("2019")
                plt.legend()
                # https://stackoverflow.com/questions/46555819/months-as-axis-ticks
                X = plt.gca().xaxis
                X.set_major_locator(months)
                X.set_major_formatter(fmt)
                plt.savefig(os.path.join("figures","Aggregate{0}Section2019.png".format(str(section))), dpi=300)
                plt.close()
                section += 1
    if (not even):
        plt.plot(focal[1], focal[2], label=focal[0])
        months = mdates.MonthLocator()  # every month
        fmt = mdates.DateFormatter('%B')
        plt.ylabel("Pageviews")
        plt.yscale("log")
        plt.xlabel("2019")
        plt.legend()
        # https://stackoverflow.com/questions/46555819/months-as-axis-ticks
        X = plt.gca().xaxis
        X.set_major_locator(months)
        X.set_major_formatter(fmt)
        plt.savefig(os.path.join("figures","Aggregate{0}Section2019.png".format(str(section))), dpi=300)
        plt.close()



plotPageviews(views)

endPage = time.time()
print("Plotting pageviews took {0} seconds.".format(str(endPage - start)))

'''
    Plots top most correlated pages and focus article.
'''
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
            keyNames.append(prettyPrint(key))

            allDays.append(days)
            allNumViews.append(numViews)
    # multi-line plot per page
    for i in range(len(allDays)):
        plt.plot(allDays[i], allNumViews[i], label=keyNames[i])
    # plt.title("Top Four Articles by Correlation and Focus Article Daily Views")
    # plt.xlabel("Days")
    months = mdates.MonthLocator()  # every month
    fmt = mdates.DateFormatter('%B')
    plt.ylabel("Pageviews")
    plt.yscale("log")
    plt.xlabel("2019")
    plt.legend()
    # https://stackoverflow.com/questions/46555819/months-as-axis-ticks
    X = plt.gca().xaxis
    X.set_major_locator(months)
    X.set_major_formatter(fmt)
    plt.savefig(os.path.join("figures","TopNPageviewCorrSince2019.png"), dpi=300)
    plt.close()

plotTopNPageviews(views)
endTop = time.time()
print("Plotting top pageviews took {0} seconds".format(str(endTop - endPage)))

'''
    Plots focus article and related pages with similar pageview trends.
'''
def plotAggregate(pageDict):
    allDays = []
    allNumViews = []
    keyNames = []
    for key in pageDict.keys():
        if (key in agg):
            days = []
            numViews = []
            temp = pageDict[key]
            temp['Date'] = pd.to_datetime(temp['Date'])
            mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
            df = temp.loc[mask]
            days = df['Date'].tolist()
            numViews = df['Count'].tolist()
            keyNames.append(prettyPrint(key))

            allDays.append(days)
            allNumViews.append(numViews)
    # multi-line plot per page
    for i in range(len(allDays)):
        plt.plot(allDays[i], allNumViews[i], label=keyNames[i])
    # plt.title("Top Four Articles by Correlation and Focus Article Daily Views")
    # plt.xlabel("Days")
    months = mdates.MonthLocator()  # every month
    fmt = mdates.DateFormatter('%B')
    plt.ylabel("Pageviews")
    plt.yscale("log")
    plt.xlabel("2019")
    # https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
    plt.legend(loc=3,prop={'size': 8})
    # https://stackoverflow.com/questions/46555819/months-as-axis-ticks
    X = plt.gca().xaxis
    X.set_major_locator(months)
    X.set_major_formatter(fmt)
    plt.savefig(os.path.join("figures","AggregatePageviews.png"), dpi=300)
    plt.close()

plotAggregate(views)
endAgg = time.time()
print("Plotting top pageviews took {0} seconds".format(str(endAgg - endTop)))