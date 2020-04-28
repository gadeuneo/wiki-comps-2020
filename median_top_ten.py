import pandas as pd
from static_helpers import *
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time

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

    print(comp_df)

    # Calculate median edit size per time delta.

    # Plot.

    return

if __name__ == "__main__":
    main()