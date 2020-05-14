'''
    Calculates Pearson's correlation coefficient for
    pageview, revision, and pageview-revision data.
    Excludes Talk pages for analysis.

    Written by James Gardner
'''

import pandas as pd
import os
import sys
from datetime import datetime as dt
import time
import math
from itertools import combinations
from static_helpers import *

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

pageviewTable = [["Article 1", "Article 2", "Corr."]]
revisionTable = [["Article 1", "Article 2", "Corr."]]
PRTable = [["Pageview", "Revision", "Corr."]]

start = time.time()

def plotViewCorrelations(dct):
    keys = list(dct.keys())
    keys = [x for x in keys if "Talk" not in x]
    heap = []
    viewComb = list(combinations(keys, 2))
    for pair in viewComb:
        xKey = pair[0]
        xDct = dct[xKey]
        xDct['Date'] = pd.to_datetime(xDct['Date'])
        # https://stackoverflow.com/questions/29370057/select-dataframe-rows-between-two-dates
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

        pageviewTable.append([xKey, yKey, corr])

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

    pageDf = pd.DataFrame(pageviewTable[1:], columns=pageviewTable[0])
    pageDf = pageDf.sort_values(by="Corr.", ascending=False)
    pageDf.to_csv("allPageviewCorr.csv", encoding="utf-8")

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

        revisionTable.append([xKey, yKey, corr])

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

    revDf = pd.DataFrame(revisionTable[1:], columns=revisionTable[0])
    revDf = revDf.sort_values(by="Corr.", ascending=False)
    revDf.to_csv("allRevisionCorr.csv", encoding="utf-8")


def plotRVCorrelations(viewDct, revDct):
    viewKeys = list(viewDct.keys())
    revKeys = list(revDct.keys())
    vKeys = [x for x in viewKeys if "Talk" not in x]
    rKeys = [x for x in revKeys if "Talk" not in x]
    # tuple pair (pageviews, revisions) for each page
    allKeys = [(x,y) for x,y in zip(vKeys, rKeys) if prettyPrint(x) == prettyPrint(y)]
    # combinations of different tuple pairs per page
    allComb = list(combinations(allKeys, 2))

    heap = []
    # x is (xPageviews, xRevisions) combined, same for y (yPageviews, yRevisions)
    for pair in allComb:
        xKey = pair[0][0]
        xDct = viewDct[xKey]
        xDct['Date'] = pd.to_datetime(xDct['Date'])
        xMask = (xDct['Date'] >= startDate) & (xDct['Date'] <= endDate)
        xDf = xDct.loc[xMask]
        # x1 is Pandas Series for pageview counts
        x1 = xDf['Count']

        xKey = pair[0][1]
        xDct = revDct[xKey]
        xDct['timestamp'] = pd.to_datetime(xDct['timestamp'])
        xDct = xDct.set_index('timestamp').resample('D')['size'].count()
        xDct = xDct.to_frame().reset_index()
        xDct.columns = ['timestamp', 'Count']
        xDct['timestamp'] = xDct['timestamp'].dt.tz_localize(None)
        xMask = (xDct['timestamp'] >= startDate) & (xDct['timestamp'] <= endDate)
        xDf = xDct.loc[xMask]
        # x2 is Pandas Series for revision counts
        x2 = xDf['Count']

        x = x1.append(x2, ignore_index=True)

        yKey = pair[1][0]
        yDct = viewDct[yKey]
        yDct['Date'] = pd.to_datetime(yDct['Date'])
        yMask = (yDct['Date'] >= startDate) & (yDct['Date'] <= endDate)
        yDf = yDct.loc[yMask]
        # y1 is Pandas Series for pageview counts
        y1 = yDf['Count']

        yKey = pair[1][1]
        yDct = revDct[yKey]
        yDct['timestamp'] = pd.to_datetime(yDct['timestamp'])
        yDct = yDct.set_index('timestamp').resample('D')['size'].count()
        yDct = yDct.to_frame().reset_index()
        yDct.columns = ['timestamp', 'Count']
        yDct['timestamp'] = yDct['timestamp'].dt.tz_localize(None)
        yMask = (yDct['timestamp'] >= startDate) & (yDct['timestamp'] <= endDate)
        yDf = yDct.loc[yMask]
        # y2 is Pandas Series for revision counts
        y2 = yDf['Count']

        y = y1.append(y2, ignore_index=True)
        
        # Pearson's correlation coefficient
        corr = x.corr(y)
        if (math.isnan(corr)):
            print("ERROR")
            print(pair)
            continue
        
        PRTable.append([xKey, yKey, corr])

        # change for top N views corr
        if (len(heap) < 5):
            heappush(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))
        else:
            heappushpop(heap, KeyDict(corr, [x, y, xKey, yKey, corr]))

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
        sns_plot.set(xlabel = keyx + " Pageviews-Revisions", ylabel=keyy + " Pageviews-Revisions")
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

    prDf = pd.DataFrame(PRTable[1:], columns=PRTable[0])
    prDf = prDf.sort_values(by="Corr.", ascending=False)
    prDf.to_csv("allPRCorr.csv", encoding="utf-8")

plotViewCorrelations(viewDict)
pageTime = time.time()
print("Pageview Corr took {0} seconds".format(str(pageTime - start)))
plotRevisonCorrelations(revisionDict)
revTime = time.time()
print("Revision Corr took {0} seconds".format(str(revTime - pageTime)))
plotRVCorrelations(viewDict, revisionDict)
prTime = time.time()
end = time.time()
print("Pageview-Revision Corr took {0} seconds".format(str(prTime - revTime)))
print("Total elasped time: {0} seconds".format(str(end - start)))