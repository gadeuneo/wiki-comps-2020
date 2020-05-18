'''
    Plots top 10 articles in single plot.

    Written by ???
'''

import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import numpy as np
from static_helpers import *

def get_dfs(top_articles):

    path = "10 Year Revision Data"

    top_articles_dfs = dict()

    for article in top_articles:
        complete_path = os.path.join(path, article)

        if file_exists(complete_path):
            top_articles_dfs[article] = pd.read_csv(complete_path)

            top_articles_dfs[article]['pythontime'] = \
                pd.to_datetime(top_articles_dfs[article]['timestamp'])

            top_articles_dfs[article].sort_values(by='pythontime', inplace=True)
        else:
            print("Could not find this file: {0}".format(article))

    return top_articles_dfs

def main():
    top_articles = [
        "2019–20 Hong Kong protests",
        "Hong Kong",
        "Carrie Lam",
        "2019 Hong Kong extradition bill",
        "2019 Hong Kong local elections",
        "Reactions to the 2019–20 Hong Kong protests",
        "2019 Yuen Long attack",
        "Tactics and methods surrounding the 2019–20 Hong Kong protests",
        "One country, two systems",
        "Umbrella Movement"
    ]

    top_articles = [article + ".csv" for article in top_articles]

    dfs = get_dfs(top_articles)
    time_period = "1"

    time_df = pd.DataFrame(columns=["NumRevisions", "Article"])
    time_df["date"] = pd.date_range(start="2009-12-10", end="2019-12-10",
        freq=time_period + "D", tz="UTC")

    articles_dfs = pd.DataFrame(columns=["NumRevisions","Article","date"])
    for article in top_articles:
        for index, row in time_df.iterrows():
            start = row["date"]
            end = start + timedelta(days=int(time_period))

            mask = (dfs[article]["pythontime"] > start) \
                & (dfs[article]["pythontime"] <= end)

            time_df.loc[index, "NumRevisions"] = len(dfs[article].loc[mask].index)
            time_df.loc[index, "Article"] = article[:-4]
        articles_dfs = pd.concat([articles_dfs, time_df], ignore_index=True, sort=False)

    articles_dfs = articles_dfs.pivot(index="date", columns="Article", values="NumRevisions")
    articles_dfs.plot()
    plt.xlabel("Years")
    plt.ylabel("Revisions")
    plt.gcf().set_size_inches(15,7)
    ax = plt.subplot(111)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.5, box.height])
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    plt.savefig("Multi-Line/10 Year Daily Edits")

    return

if __name__ == '__main__':
    main()
