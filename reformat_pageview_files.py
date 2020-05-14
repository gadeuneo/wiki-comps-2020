'''
    Manually reformats downloaded pageview files from WMF Labs tool.

    Written by James Gardner
'''

import pandas as pd
import os
import sys
import requests as rq
from datetime import datetime as dt
import time
from static_helpers import *

# base url to use for manual download
url = '''https://tools.wmflabs.org/redirectviews/?project=en.wikipedia.org
        &platform=all-access&agent=user&range=all-time&sort=views
        &direction=1&view=list&page='''

# path where manual download of file is saved
path = "dailyPageviews"

# list of full filenames
titles = []

def reformatFiles():

    for i in range(len(titles)):
        pageDf = pd.read_csv(os.path.join(path, titles[i]))
        pageviews = [["Date", "Count"]]

        for col in pageDf.columns[1:]:
            pageviews.append([col, pageDf[col].sum()])

        dfData = pd.DataFrame(pageviews[1:], columns=pageviews[0])
        dfData.to_csv(os.path.join(path, titles[i]), encoding="utf-8")



reformatFiles()