'''
File for manipulating data.

James Gardner
'''

import pandas as pd
import os
import sys
from datetime import datetime
import time
import matplotlib.pyplot as plt
import numpy as np
import copy

start = time.time()

# folder of files
path = "data"
plotPath = "figures"

if (not os.path.exists(plotPath)):
    os.mkdir(plotPath)

# working list of Wiki pages
titles = [
    "2019–20 Hong Kong protests",
    "Hong Kong",
    "2019 Hong Kong extradition bill",
    "Government of Hong Kong",
    "Murder of Poon Hiu-wing",
    "One country, two systems",
    "Demosistō",
    "Hong Kong 1 July marches",
    "Civil Human Rights Front",
    "Hong Kong Human Rights and Democracy Act",
    "Chinese University of Hong Kong conflict",
    "Death of Chow Tsz-lok",
    "Siege of the Hong Kong Polytechnic University",
    "2019 Yuen Long attack",
    "Hong Kong–Mainland China conflict",
    "Storming of the Legislative Council Complex",
    "Hong Kong Way",
    "2019 Prince Edward station attack",
    "Death of Chan Yin-lam",
    "2019 Hong Kong local elections",
    "List of protests in Hong Kong",
    "Police misconduct allegations during the 2019–20 Hong Kong protests",
    "Art of the 2019–20 Hong Kong protests",
    "12 June 2019 Hong Kong protest",
    "Umbrella Movement",
    "Causes of the 2019–20 Hong Kong protests",
    "Tactics and methods surrounding the 2019–20 Hong Kong protests",
    "Carrie Lam",
    "Reactions to the 2019–20 Hong Kong protests",
    "List of early 2019 Hong Kong protests",
    "List of July 2019 Hong Kong protests",
    "List of August 2019 Hong Kong protests",
    "List of September 2019 Hong Kong protests",
    "List of October 2019 Hong Kong protests",
    "List of November 2019 Hong Kong protests",
    "List of December 2019 Hong Kong protests",
    "List of January 2020 Hong Kong protests",
    "Glory to Hong Kong",
    "Lennon Wall (Hong Kong)",
    "HKmap.live",
    "Killing of Luo Changqing"
]

# adds talk pages
for i in range(len(titles)):
    titles.append("Talk:" + titles[i])

# converts titles to filename format
titles = [title.replace(" ","_").replace(".","(dot)").replace(":", "(colon)") + ".csv" for title in titles]
dataTitles = []
for title in titles:
    dataTitles.append("Data" + title)
    dataTitles.append("Redirects" + title)

# check if file exists, if not, remove from list of titles
for title in titles:
    if (not os.path.isfile(os.path.join(path, "Data" + title))):
        filename = "Data" + title
        dataTitles.remove(filename)

    if (not (os.path.isfile(os.path.join(path, "Redirects" + title)))):
        filename = "Redirects" + title
        dataTitles.remove(filename)


##### TODO: merge files? -- Which ones? How?
##### TODO: save merged files?


dataDict = dict()


for f in dataTitles:
    dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

# print(dataDict.keys())
print(len(dataDict))


##### TODO: Make plots
#### https://matplotlib.org/tutorials/introductory/pyplot.html

### SAMPLE CODE
# https://towardsdatascience.com/matplotlib-tutorial-learn-basics-of-pythons-powerful-plotting-library-b5d1b8f67596

# plots x values, then y values
plt.plot([1,2,3,4], [1,4,9,16])
plt.title("Sample plot")
plt.xlabel("Sample x axis label")
plt.ylabel("Sample y axis label")

if (not os.path.isfile(os.path.join(plotPath, "sample.png"))):
    plt.savefig(os.path.join(plotPath, "sample.png"), bbox_inches="tight")



end = time.time()
print("Time Elapsed: " + str(end-start))

sys.exit(0)