import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
# https://realpython.com/numpy-scipy-pandas-correlation-python/
import scipy.stats
import matplotlib.pyplot as plt

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

pageviewPath = "dailyPageviews"
figPath = "pageCorr"
savepath = os.path.join("figures", figPath)

if (not os.path.exists(savepath)):
    os.mkdir(savepath)


viewFiles = os.listdir(pageviewPath)

viewDict = dict()

for f in viewFiles:
    viewDict[f[:-4]] = pd.read_csv(os.path.join(pageviewPath, f))

# print(viewDict.keys())

keys = list(viewDict.keys())

heap = []

for keyx in keys:
    x = viewDict[keyx]['Count']
    for keyy in keys:
        if (keyx != keyy):
            y = viewDict[keyy]['Count']

            corr = x.corr(y)
            # change for top N views corr
            if (len(heap) < 10):
                heappush(heap, KeyDict(corr, [x, y, keyx, keyy, corr]))
            else:
                heappushpop(heap, KeyDict(corr, [x, y, keyx, keyy, corr]))

topNViews = sorted(heap, reverse=True)

for item in topNViews:
    x = item.lst[0]
    y = item.lst[1]
    keyx = item.lst[2]
    keyy = item.lst[3]
    slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
    line = "Regression line: y={0} + {1}x, r={2}".format(intercept, slope, r)
    fig, ax = plt.subplots()
    ax.plot(x, y, linewidth=0, marker='s', label='Data points')
    ax.plot(x, intercept + slope * x, label=line)
    ax.set_xlabel(keyx + " Pageviews")
    ax.set_ylabel(keyy + " Pageviews")
    ax.legend(facecolor='white')
    plt.savefig(os.path.join(savepath, keyx+" " +keyy + ".png"), dpi=300)
    plt.close()