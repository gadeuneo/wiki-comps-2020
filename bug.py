import pandas as pd
import os
import sys
import requests as rq
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
# functions that are frequently accessed by other files
from static_helpers import *

path = "dailyPageviews"

titles = ["Death_of_Luo_Changqing.csv", "Talk(colon)Death_of_Luo_Changqing.csv"]

def reformatFiles():

    for i in range(len(titles)):
        pageDf = pd.read_csv(os.path.join(path, titles[i]))
        # prints daily sums
        # print(pageDf.sum(axis=0, skipna=True))
        # prints page title sums
        # print(pageDf.sum(axis=1, skipna=True))
        pageviews = [["Date", "Count"]]

        for col in pageDf.columns[1:]:
            if (dt.strptime(col, "%Y-%m-%d") > dt.strptime("2019-12-10", "%Y-%m-%d")):
                break
            else:
                pageviews.append([col, pageDf[col].sum()])

        dfData = pd.DataFrame(pageviews[1:], columns=pageviews[0])
        dfData.to_csv(os.path.join(path, titles[i]), encoding="utf-8")



reformatFiles()