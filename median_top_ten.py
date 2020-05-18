'''
    Plots median edit size across top 10 pages.

    Written by Jackie Chan and Kirby Mitchell.
'''

import pandas as pd
from static_helpers import *
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt

'''
    Function: get_top_ten_dfs

    Input: List of titles for the top ten articles.

    Output: A dictionary containng dataframes generated from the CSVs of the 
    revision history. It is a helper function
'''
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

'''
    Function: get_comp_top_ten_df

    Input: List of titles for the top ten articles.

    Output: A dataframe containing all the revision histories from the top ten
    articles given. The function uses get_top_ten_dfs to produce this
    comprehensive dataframe.
'''
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

    top_files = [article + ".csv" for article in top_articles]

    comp_df = get_comp_top_ten_df(top_files)

    # Calculate median edit size per time delta.

    time_period = "14"

    week_df = pd.DataFrame(columns=["median"])
    week_df["date"] = pd.date_range(start="2009-12-10", end="2019-12-10",
        freq=time_period + "D", tz="UTC")

    for index, row in week_df.iterrows():
        start_week = row["date"]
        end_week = start_week + timedelta(days=int(time_period))

        mask = (comp_df["pythontime"] > start_week) \
            & (comp_df["pythontime"] <= end_week)

        # Gets the median from the mask and inputs into the week_df.
        week_df.loc[index, "median"] = comp_df.loc[mask]["size"].mean()

    # Plot.

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    week_df.set_index("date", inplace=True, drop=True)

    week_df.plot()

    plt.xlabel("Years")
    plt.ylabel("Median Edit Size (bytes)")
    plt.legend().remove()

    plt.savefig("figures/Median Top Ten Edits Per Week Diagram")
    plt.show()

    return

if __name__ == "__main__":
    main()
