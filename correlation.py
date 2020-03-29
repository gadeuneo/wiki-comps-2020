import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import scipy.stats
import matplotlib.pyplot as plt
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

for key in keys:
    x = viewDict[key]['Count']
    for k in keys:
        if (key != k):
            y = viewDict[k]['Count']
            # print(x.corr(y))
            slope, intercept, r, p, stderr = scipy.stats.linregress(x, y)
            line = "Regression line: y={0} + {1}x, r={2}".format(intercept, slope, r)
            fig, ax = plt.subplots()
            ax.plot(x, y, linewidth=0, marker='s', label='Data points')
            ax.plot(x, intercept + slope * x, label=line)
            ax.set_xlabel(key + " Pageviews")
            ax.set_ylabel(k + " Pageviews")
            ax.legend(facecolor='white')
            plt.savefig(os.path.join(savepath, key+k + ".png"), dpi=300)
            plt.close()
            sys.exit(0)

            

# TODO: save only top 5 correlations (only positive? or top abs values?)