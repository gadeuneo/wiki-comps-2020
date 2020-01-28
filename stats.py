'''
File for manipulating data.

James Gardner
'''

import pandas as pd
import os

path = "data"
title = "protests.csv"

with open(os.path.join(path, title), "r", encoding="utf-8") as f:
    csv = f.readlines()


data = pd.read_csv(os.path.join(path, title))
