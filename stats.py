'''
    File for manipulating data.
'''

import pandas as pd
from pandas.plotting import register_matplotlib_converters
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
#uhuh
import copy
from static_helpers import *

# register_matplotlib_converters()
# start = time.time()

# # folder of files
# path = "10years"
# plotPath = "figures"

# directories = ["figures"]

# create_directories(directories)

# # working list of Wiki pages
# titles = get_titles()

# # adds talk pages
# titles = add_talk_pages(titles)

# # converts titles to filename format
# titles = [format_file_names(title) for title in titles]
# titleArray = []
# for title in titles:
#     titleArray.append("Data" + title)
#     titleArray.append("Redirects" + title)

# # check if file exists, if not, remove from list of titles
# for title in titles:
#     if (not os.path.isfile(os.path.join(path, "Data" + title))):
#         filename = "Data" + title
#         titleArray.remove(filename)

#     if (not (os.path.isfile(os.path.join(path, "Redirects" + title)))):
#         filename = "Redirects" + title
#         titleArray.remove(filename)


# ##### TODO: merge files? -- Which ones? How?
# ##### TODO: save merged files?


# dataDict = dict()


# for f in titleArray:
#     dataDict[f[:-4]] = pd.read_csv(os.path.join(path, f))

# # print(dataDict.keys())

# allData = []
# allRed = []
# for key in dataDict.keys():
#     if ("Data" in key):
#         allData.append(dataDict[key])
#     else:
#         allRed.append(dataDict[key])

# revisionData = pd.concat(allData, ignore_index=True, sort=False)
# revisionData['timestamp'] = pd.to_datetime(revisionData['timestamp'])
# # TODO: double check inplace param
# revisionData.sort_values(by='timestamp', inplace = True)
# revisionData['timestamp'] = revisionData['timestamp'].astype(str)
# revisionData['timestamp'] = revisionData['timestamp'].str.replace(" ", "T").str[:-6] + "Z"
# #print(revisionData.to_string())

# # Convert date to Unix Timestamp
# startDate = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
# endDate = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
# today = int(time.mktime(dt.today().timetuple()))
# # Assertions for proper date args
# assert(startDate <= endDate)
# assert(endDate <= today)

# #separate out "DATA-" articles from "REVISION-", without the .csv
# dataTitleArray = []
# for title in titleArray:
#     if title[0:4] == "Data":
#         dataTitleArray.append(title[:-4])

# # TODO: loop over timestamps and get count for each (day/week/month?)

def topTenAfterDate(date, data_title_array, data_dict):
    start_date = dt.fromtimestamp(int(time.mktime(dt.strptime(date, "%Y-%m-%d").timetuple())))
    top_ten_list = []
    curr = []
    for title in data_title_array:
        article = data_dict[title]
        edit_count = 0
        for index, row in article.iterrows():
            curr_date = dt.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
            if(curr_date >= start_date):
                editCount+=1
        curr.append(title)
        curr.append(edit_count)
        topTenList.append(curr)
        curr = []
    #bubble sort
    length = len(top_ten_list)
    for i in range (length):
        for j in range (0, length-i-1):
            if top_ten_list[j][1] > top_ten_list[j+1][1]:
                top_ten_list[j], top_ten_list[j+1] = top_ten_list[j+1], top_ten_list[j]
    print(top_ten_list)

def makeTimeXNumEditorsFigure(start_date, title, data_title_array, data_dict):
    article = data_dict[title]
    new_date = dt.fromtimestamp(start_date)
    curr_month = dt.fromtimestamp(start_date).month
    editor_set = set()
    size_of_article = article.shape[0]
    count_arr = []
    date_arr = []
    new_date = dt.fromtimestamp(start_date)
    for index, row in article.iterrows():
        edit_time = dt.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%SZ")
        while(new_date < edit_time):
            if(new_date.month != curr_nonth):
                count_arr.append(len(editor_set))
                epoch = int((newDate - timedelta(days=1)).timestamp())
                date_arr.append(dt.fromtimestamp(epoch))
                editor_set.clear()
                new_date = new_date + timedelta(days=1)
                curr_month = new_date.month
            else:
                new_date = new_date + timedelta(days=1)
        #out of while loop, means newDate = editTime
        #edge case of last index
        if(index == (size_of_article - 1)):
            if(curr_month == edit_time.month):
                editor_set.add(row['user'])
            else:
                count_arr.append(len(editor_set))
                epoch = int(edit_time.timestamp())
                date_arr.append(dt.fromtimestamp(epoch))
                editor_set.clear()
                editor_set.add(row['user'])
                curr_month = edit_time.month
            count_arr.append(len(editor_set))
            date_arr.append(dt.fromtimestamp(epoch))
        else:
            if(curr_month == edit_time.month):
                editor_set.add(row['user'])
            else:
                count_arr.append(len(editor_set))
                epoch = int(edit_time.timestamp())
                date_arr.append(dt.fromtimestamp(epoch))
                editor_set.clear()
                editor_set.add(row['user'])
                curr_month = edit_time.month

    fig, ax = plt.subplots(figsize=(15,7))
    ax.plot(dateArr, countArr)

    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m'))
    #ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.format_xdata = mdates.DateFormatter('%Y-%m')

    fig.autofmt_xdate()
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Number of Editors Per Month")
    subpath = "10y Time vs Number Editors Per Month"
    # os.mkdir(os.path.join(plotPath, subpath))
    # newpath = os.path.join(plotPath, subpath)
    if (not os.path.isfile(os.path.join(plotPath, subpath, title + ".png"))):
        plt.savefig(os.path.join(plotPath, subpath, title + ".png"), bbox_inches="tight")
    plt.close()

'''testing/making statistics below'''
'''for title in dataTitleArray:
    makeTimeXNumEditorsFigure(title)'''

def get_files_to_generate(path):

    all_articles = get_titles_and_talk_pages()

    file_names = [format_file_names(article) for article in all_articles]

    files = []

    # Throw all the file_names into files.
    for file_name in file_names:
        files.append("Data" + file_name)
        files.append("Redirects" + file_name)

    # Remove existing files.
    for file in files:
        complete_path = os.path.join(path, file)
        if file_exists(complete_path):
            files.remove(file)

    return files


def main():

    register_matplotlib_converters()
    
    start = time.time()

    path = "10years"
    plot_path = "figures"

    create_directory("figures")

    files = get_files_to_generate(path)

    data_dict = dict()

    all_data = []
    all_redirects = []

    
    for file in files:
        complete_path = os.path.join(path, file)
        # -4 is to remove the .csv suffix.
        data_dict[file[:-4]] = pd.read_csv(complete_path)

    # Placing the 
    for key in data_dict.keys():
        if ("Data" in key):
            all_data.append(data_dict[key])
        else:
            all_red.append(data_dict[key])

    # Convert date to Unix Timestamp
    start_date = int(time.mktime(dt.strptime("2009-12-10", "%Y-%m-%d").timetuple()))
    end_date = int(time.mktime(dt.strptime("2019-12-10", "%Y-%m-%d").timetuple()))
    today = int(time.mktime(dt.today().timetuple()))
    # Assertions for proper date args
    assert(start_date <= end_date)
    assert(end_date <= today)

    # Separate out "Data" articles from "Revision", without the .csv suffix.
    data_title_array = []

    for file in files:
        if title[0:4] == "Data":
            data_title_array.append(title[:-4])




if __name__ == "__main__":
    main()

# sys.exit(0)
