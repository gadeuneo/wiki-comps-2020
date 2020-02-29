import pandas as pd
import os
import sys
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import matplotlib.pyplot as plt
import numpy as np
#uhuh
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.ticker as ticker
from static_helpers import *

from selenium import webdriver



path = "WikiData-pageviews"
newpath = "dailyPageviews"
# pageviewFile = "2019–20 Hong Kong protests-20150701-20200225.csv"

if (not os.path.exists(newpath)):
    os.mkdir(newpath)

# Convert date to Unix Timestamp
startDate = dt.strptime("2009-12-10", "%Y-%m-%d")
endDate = dt.strptime("2019-12-10", "%Y-%m-%d")
today = dt.today()

# Assertions for proper date args
assert(startDate <= endDate)
assert(endDate <= today)


url = '''https://tools.wmflabs.org/redirectviews/?project=en.wikipedia.org
        &platform=all-access&agent=user&range=all-time&sort=views
        &direction=1&view=list&page='''

titles = get_titles()
titles = add_talk_pages(titles)
# driverPath = os.path.join("D:", "james", "Downloads", "chromedriver_linux64", "chromedriver.exe")
driverPath = os.path.join("mnt", "d", "james", "Downloads", "chromedriver_linux64", "chromedriver.exe")
driver = webdriver.Chrome(executable_path=driverPath)
driver.get(url + titles[0])
button = driver.find_elements_by_class_name("btn btn-default btn-sm dropdown-toggle")
button.click()
button = driver.find_elements_by_class_name("download-csv")
button.click()


sys.exit(0)

pageDf = pd.read_csv(os.path.join(path, pageviewFile))
# prints daily sums
# print(pageDf.sum(axis=0, skipna=True))
# prints page title sums
# print(pageDf.sum(axis=1, skipna=True))

pageviews = [["Date", "Count"]]

for col in pageDf.columns[1:]:
    if (dt.strptime(col, "%Y-%m-%d") > endDate):
        break
    else:
        pageviews.append([col, pageDf[col].sum()])

if (not (os.path.isfile(os.path.join(newpath, "2019-20 Hong Kong protests.csv")))):
                dfData = pd.DataFrame(pageviews[1:], columns=pageviews[0])
                dfData.to_csv(os.path.join(newpath, "2019-20 Hong Kong protests.csv"), encoding="utf-8")

