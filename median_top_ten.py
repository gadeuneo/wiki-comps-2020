'''
    Plots median edit size across top 10 pages.

    Written by Jackie Chan and Kirby Mitchell.
'''

import pandas as pd
from static_helpers import *
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import matplotlib.pyplot as plt

def get_top_ten_dfs(top_files):

    path = "10 Year Revision Data"

    top_article_dfs = dict()

    for file in top_files:
        complete_path = os.path.join(path, file)

        if file_exists(complete_path):
            top_article_dfs[file] = pd.read_csv(complete_path)

            top_article_dfs[file]['pythontime'] = \
                pd.to_datetime(top_article_dfs[file]['timestamp'])
            
            top_article_dfs[file].sort_values(by='pythontime', inplace=True)
        else:
            print("Could not find this file: {0}".format(file))

    
    return top_article_dfs

def get_comp_top_ten_df(top_files):

    top_article_dfs = get_top_ten_dfs(top_files)

    comp_df = pd.concat(top_article_dfs, ignore_index=True, sort=False)
    comp_df.sort_values(by='pythontime', inplace=True)

    return comp_df


def main():

    # First we need the top ten pages into one dataframe.

    # Please keep in mind that - and – are different characters.
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

    assert(len(top_articles) == 10)

    top_df = []

    top_files = [article + ".csv" for article in top_articles]

    comp_df = get_comp_top_ten_df(top_files)

    # Calculate median edit size per time delta.

    time_period = "7"

    week_df = pd.DataFrame(columns=["median"])
    week_df["date"] = pd.date_range(start="2009-12-10", end="2019-12-10",
        freq=time_period + "D", tz="UTC")

    for index, row in week_df.iterrows():
        start_week = row["date"]
        end_week = start_week + timedelta(days=int(time_period))

        mask = (comp_df["pythontime"] > start_week) \
            & (comp_df["pythontime"] <= end_week)

        # Gets the median from the mask and inputs into the week_df.
        week_df.loc[index, "median"] = comp_df.loc[mask]["size"].median()

    # Plot.

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    week_df.set_index("date", inplace=True, drop=True)

    week_df.plot()
    plt.show()

    return

if __name__ == "__main__":
    main()