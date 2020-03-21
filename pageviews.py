'''
Gets pageview data of wikipage per date from the MediaWiki API.
Saves in csv format per page.

James Gardner
'''

import pandas as pd
import os
import sys
import requests as rq
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
from static_helpers import *
#from selenium import webdriver
import shutil


'''
Begin MediaWiki API pageview collection
'''



'''
End MediaWiki API pageview collection
'''