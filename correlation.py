import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import math
from itertools import combinations

# https://realpython.com/numpy-scipy-pandas-correlation-python/
import scipy.stats
import matplotlib.pyplot as plt
# https://stackoverflow.com/questions/36420908/can-i-draw-a-regression-line-and-show-parameters-using-scatterplot-with-a-pandas
import seaborn as sns

# https://stackoverflow.com/questions/30284693/pythonic-way-to-store-top-10-results
from heapq import heappush, heappushpop

# https://stackoverflow.com/questions/42985030/inserting-dictionary-to-heap-python
from functools import total_ordering

# https://docs.python.org/3.6/library/functools.html#functools.total_ordering
@total_ordering
class KeyDict(object):
    def __init__(self, key, lst):
        self.key = key
        self.lst = lst

    def __lt__(self, other):
        return self.key < other.key

    def __eq__(self, other):
        return self.key == other.key

    def __repr__(self):
        return '{0.__class__.__name__}(key={0.key}, lst={0.lst})'.format(self)


from static_helpers import *


def prettyPrint(dictKey):
    newTitle = str(dictKey)
    newTitle = newTitle.replace("Data", "").replace("_", " ").replace("(dot)",".").replace("(colon)","-")
    return newTitle

revisionPath = "10 Year Revision Data"
pageviewPath = "dailyPageviews"

pageviewSavePath = os.path.join("figures", "pageviewCorr")
revisionSavePath = os.path.join("figures", "revisionCorr")
viewRevSavePath = os.path.join("figures", "pageview-revisionCorr")

if (not os.path.exists(pageviewSavePath)):
    os.mkdir(pageviewSavePath)

if (not os.path.exists(revisionSavePath)):
    os.mkdir(revisionSavePath)

if (not os.path.exists(viewRevSavePath)):
    os.mkdir(viewRevSavePath)

viewFiles = os.listdir(pageviewPath)
revisonFiles = os.listdir(revisionPath)

viewDict = dict()
revisionDict = dict()

for f in viewFiles:
    viewDict[f[:-4]] = pd.read_csv(os.path.join(pageviewPath, f))

for r in revisonFiles:
    revisionDict[r[:-4]] = pd.read_csv(os.path.join(revisionPath, r))

startDate = dt.strptime("2009-12-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")

def plotViewCorrelations(dct):
    keys = list(dct.keys())
    keys = [x for x in keys if "Talk" not in x]
    heap = []
    viewComb = list(combinations(keys, 2))
    for pair in viewComb:
        xKey = pair[0]
        xDct = dct[xKey]
        xDct['Date'] = pd.to_datetime(xDct['Date'])
        xMask = (xDct['Date'] >= startDate) & (xDct['Date'] <= endDate)
        xDf = xDct.loc[xMask]
        x = xDf['Count']

        yKey = pair[1]
        yDct = dct[yKey]
        yDct['Date'] = pd.to_datetime(yDct['Date'])
        yMask = (yDct['Date'] >= startDate) & (yDct['Date'] <= endDate)
        yDf = yDct.loc[yMask]
        y = yDf['Count']
        
        # Pearson's correlation coefficient
        corr = x.corr(y)
        if (math.isnan(corr)):
            print("ERROR!!!! - Pageview files below have issues!")
            print(xKey)
            print(yKey)
            continue
        # change for top N views corr
        if (len(heap) < 5):
            heappush(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))
        else:
            heappushpop(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))

    topNViews = sorted(heap, reverse=True)

    table = [["Article 1", "Article 2", "Corr."]]

    for item in topNViews:
        x = item.lst[0]
        y = item.lst[1]
        keyx = prettyPrint(item.lst[2])
        keyy = prettyPrint(item.lst[3])
        slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
        line = "Regression line: y={0} + {1}x, r={2}".format(intercept, slope, r)
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=0, marker='s', label='Data points')
        ax.plot(x, intercept + slope * x, label=line)
        ax.set_xlabel(keyx + " Pageviews")
        ax.set_ylabel(keyy + " Pageviews")
        ax.legend(facecolor='white')
        plt.savefig(os.path.join(pageviewSavePath, keyx+" " +keyy + ".png"), dpi=300)
        plt.close()
        table.append([keyx, keyy, item.key])

    tableDf = pd.DataFrame(table[1:], columns=table[0])
    tableDf = tableDf.sort_values(by="Corr.", ascending=False)
    tableDf.to_csv("pageviewCorr.csv", encoding="utf-8")

def plotRevisonCorrelations(dct):
    keys = list(dct.keys())
    keys = [x for x in keys if "Talk" not in x]
    heap = []
    revComb = list(combinations(keys, 2))
    for pair in revComb:
        xKey = pair[0]
        xDct = dct[xKey]
        xDct['timestamp'] = pd.to_datetime(xDct['timestamp'])
        # https://stackoverflow.com/questions/48961892/python-pandas-group-by-day-and-count-for-each-day
        # https://stackoverflow.com/questions/56653774/how-do-i-fill-in-missing-dates-with-zeros-for-a-pandas-groupby-list
        xDct = xDct.set_index('timestamp').resample('D')['size'].count()
        #     # https://stackoverflow.com/questions/26097916/convert-pandas-series-to-dataframe
        xDct = xDct.to_frame().reset_index()
        xDct.columns = ['timestamp', 'Count']
        # https://stackoverflow.com/questions/46295355/pandas-cant-compare-offset-naive-and-offset-aware-datetimes
        xDct['timestamp'] = xDct['timestamp'].dt.tz_localize(None)
        xMask = (xDct['timestamp'] >= startDate) & (xDct['timestamp'] <= endDate)
        xDf = xDct.loc[xMask]
        x = xDf['Count']

        yKey = pair[1]
        yDct = dct[yKey]
        yDct['timestamp'] = pd.to_datetime(yDct['timestamp'])
        yDct = yDct.set_index('timestamp').resample('D')['size'].count()
        yDct = yDct.to_frame().reset_index()
        yDct.columns = ['timestamp', 'Count']
        yDct['timestamp'] = yDct['timestamp'].dt.tz_localize(None)
        yMask = (yDct['timestamp'] >= startDate) & (yDct['timestamp'] <= endDate)
        yDf = yDct.loc[yMask]
        y = yDf['Count']
        
        # Pearson's correlation coefficient
        corr = x.corr(y)
        if (math.isnan(corr)):
            print("ERROR!!!! - Revision files below have issues!")
            print(xKey)
            print(yKey)
            continue
        # change for top N views corr
        if (len(heap) < 5):
            heappush(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))
        else:
            heappushpop(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))

    topNViews = sorted(heap, reverse=True)

    table = [["Article 1", "Article 2", "Corr."]]

    for item in topNViews:
        x = item.lst[0]
        y = item.lst[1]
        keyx = prettyPrint(item.lst[2])
        keyy = prettyPrint(item.lst[3])
        x.name = "X"
        y.name = "Y"
        df = pd.concat([x,y], axis = 1)

        sns_plot = sns.lmplot(x='X',y='Y',data=df,fit_reg=True)
        # https://stackoverflow.com/questions/31632637/label-axes-on-seaborn-barplot
        sns_plot.set(xlabel = keyx + " Revisons", ylabel=keyy + " Revisions")
        sns_plot.savefig(os.path.join(revisionSavePath, keyx+" " +keyy + ".png"))
        # ax = df.plot(x='X', y='Y', kind='scatter')
        # ax.set_xlabel(keyx + " Revisions")
        # ax.set_ylabel(keyy + " Revisions")
        # fig = ax.get_figure()
        # fig.savefig(os.path.join(revisionSavePath, keyx+" " +keyy + ".png"), dpi=300)
        table.append([keyx, keyy, item.key])

    tableDf = pd.DataFrame(table[1:], columns=table[0])
    tableDf = tableDf.sort_values(by="Corr.", ascending=False)
    tableDf.to_csv("revisionCorr.csv", encoding="utf-8")


def plotRVCorrelations(viewDct, revDct):
    viewKeys = list(viewDct.keys())
    revKeys = list(revDct.keys())
    heap = []
    for keyx in viewKeys:
        temp = viewDct[keyx]
        temp['Date'] = pd.to_datetime(temp['Date'])
        mask = (temp['Date'] >= startDate) & (temp['Date'] <= endDate)
        df = temp.loc[mask]
        x = df['Count']

        # x = viewDct[keyx]['Count']
        for keyy in revKeys:
            if (prettyPrint(keyx) != prettyPrint(keyy) and "Talk" not in keyx and "Talk" not in keyy):
                ydf = revDct[keyy]
                ydf['timestamp'] = pd.to_datetime(ydf['timestamp'])
                ydf = ydf.set_index('timestamp').resample('D')['size'].count()
                ydf = ydf.to_frame().reset_index()
                ydf.columns = ['timestamp', 'Count']
                ydf['timestamp'] = ydf['timestamp'].dt.tz_localize(None)

                mask = (ydf['timestamp'] >= startDate) & (ydf['timestamp'] <= endDate)
                df = ydf.loc[mask]
                y = df['Count']

                # y = ydf['Count']
                corr = x.corr(y)
                if (math.isnan(corr)):
                    continue
                # change for top N views corr
                if (len(heap) < 10):
                    heappush(heap, KeyDict(corr, [x, y, keyx, keyy, corr]))
                else:
                    heappushpop(heap, KeyDict(corr, [x, y, keyx, keyy, corr]))

    topNViews = sorted(heap, reverse=True)

    table = [["Pageviews", "Revisions", "Corr."]]

    for item in topNViews:
        x = item.lst[0]
        y = item.lst[1]
        keyx = prettyPrint(item.lst[2])
        keyy = prettyPrint(item.lst[3])
        x.name = "X"
        y.name = "Y"
        df = pd.concat([x,y], axis = 1)

        sns_plot = sns.lmplot(x='X',y='Y',data=df,fit_reg=True)
        # https://stackoverflow.com/questions/31632637/label-axes-on-seaborn-barplot
        sns_plot.set(xlabel = keyx + " Pageviews", ylabel=keyy + " Revisions")
        sns_plot.savefig(os.path.join(viewRevSavePath, keyx+" " +keyy + ".png"))
        # ax = df.plot(x='X', y='Y', kind='scatter')
        # ax.set_xlabel(keyx + " Revisions")
        # ax.set_ylabel(keyy + " Revisions")
        # fig = ax.get_figure()
        # fig.savefig(os.path.join(revisionSavePath, keyx+" " +keyy + ".png"), dpi=300)
        table.append([keyx, keyy, item.lst[4]])

    tableDf = pd.DataFrame(table[1:], columns=table[0])
    tableDf = tableDf.sort_values(by="Corr.", ascending=False)
    tableDf.to_csv("pageview-revisionCorr.csv", encoding="utf-8")

plotViewCorrelations(viewDict)
plotRevisonCorrelations(revisionDict)
# plotRVCorrelations(viewDict, revisionDict)