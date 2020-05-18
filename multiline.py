'''
    Creates multiple-line figure showing revision history of the ten most
    revised articles in our corpus.

    Written by Kirby Mitchell.
'''
import pandas as pd
from datetime import datetime as dt
from datetime import timedelta
import matplotlib.pyplot as plt
from static_helpers import *

# Function that creates the DataFrames from the csv files for the ten most
# revised articles in our corpus. Returns dictionary of DataFrames for the
# articles in the corpus.
def get_dfs(top_articles):
    path = "10 Year Revision Data"
    top_articles_dfs = dict()
    # For each of the top ten articles, add a DataFrame of the csv file into the
    # dictionary where the article title is the key and the DataFrame is the
    # value.
    for article in top_articles:
        complete_path = os.path.join(path, article)
        if file_exists(complete_path):
            top_articles_dfs[article] = pd.read_csv(complete_path)
            # Convert the timestamp column in csv into datetime and add it as
            # column in DataFrame.
            top_articles_dfs[article]['pythontime'] = \
                pd.to_datetime(top_articles_dfs[article]['timestamp'])
            # Sort rows in DataFrame by the time that edits occurred.
            top_articles_dfs[article].sort_values(by='pythontime', inplace=True)
        else:
            print("Could not find this file: {0}".format(article))

    return top_articles_dfs

# Main function that creates multiline diagram.
def main():
    # List that contains titles of top ten most revised articles in our corpus.
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
    # Appends ".csv" to article names.
    top_articles = [article + ".csv" for article in top_articles]
    dfs = get_dfs(top_articles)
    # Changing time_period changes the time periods added to the time_df
    # DataFrame. 1 = 1 day, 30 = 30 days, etc.
    time_period = "1"
    time_df = pd.DataFrame(columns=["NumRevisions", "Article"])
    time_df["date"] = pd.date_range(start="2018-12-10", end="2019-12-10",
        freq=time_period + "D", tz="UTC")
    articles_dfs = pd.DataFrame(columns=["NumRevisions","Article","date"])
    for article in top_articles:
        for index, row in time_df.iterrows():
            start = row["date"]
            end = start + timedelta(days=int(time_period))
            # Sliding window that looks at edits made within a certain period of
            # time such as a day, week, or month. Based on time_period.
            mask = (dfs[article]["pythontime"] > start) \
                & (dfs[article]["pythontime"] <= end)
            # Finds the revisions within the time period specified by mask.
            time_df.loc[index, "NumRevisions"] = len(dfs[article].loc[mask].index)
            time_df.loc[index, "Article"] = article[:-4]
        articles_dfs = pd.concat([articles_dfs, time_df], ignore_index=True, sort=False)

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    articles_dfs = articles_dfs.pivot(index="date", columns="Article", values="NumRevisions")
    # Plots graph.
    articles_dfs.plot()
    plt.xlabel("Months")
    plt.ylabel("Revisions")
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', borderaxespad=0.)
    plt.savefig("figures/Multi-Line/1 Year Daily Edits", bbox_inches='tight')
    return

if __name__ == '__main__':
    main()
