'''
    Plots the number of pages editted in the article corpus per interval of
    time.

    Written by Jackie Chan and Kirby Mitchell.
'''

import pandas as pd
from static_helpers import *
from datetime import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta
import time
import matplotlib.pyplot as plt

def main():

    comp_df = pd.read_csv("10 Year Updated.csv")
    comp_df["pythontime"] = pd.to_datetime(comp_df["pythontime"])

    # Create the dataframe.
    days = "1"

    time_df = pd.DataFrame(columns=["pages_editted"])
    time_df["date"] = pd.date_range(start="2018-12-10", end="2019-12-10",
        freq=days + "D", tz="UTC")

    # Find the number of pages editted per time interval in days.
    for index, row in time_df.iterrows():

        start_time = row["date"]
        end_time = start_time + timedelta(days=int(days))

        mask = (comp_df["pythontime"] > start_time) \
            & (comp_df["pythontime"] <= end_time)

        # Counts the number of unique page IDs in the mask.
        time_df.loc[index, "pages_editted"] = \
            comp_df.loc[mask]["page_id"].nunique()


    # Plot the editted pages.

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    time_df.set_index("date", inplace=True, drop=True)

    time_df.plot()

    plt.xlabel("Months")
    plt.ylabel("Number of Articles Edited")
    plt.title("Number of Articles from Our Article Corpus Edited per Day in "
        "the Last Year of Our Analysis Period")
    plt.legend().remove()

    plt.savefig("figures/Edited Pages Per Week Diagram")

    plt.show()

    return

if __name__ == "__main__":
    main()
