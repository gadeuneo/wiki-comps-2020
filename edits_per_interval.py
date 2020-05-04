'''
    Plots the number of edits per time interval.

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

    days = "1"

    time_df = pd.DataFrame(columns=["Number of Revisions"])
    time_df["date"] = pd.date_range(start="2018-12-10", end="2019-12-10",
        freq=days + "D", tz="UTC")

    # Find the number of pages editted per time interval in days.
    for index, row in time_df.iterrows():

        start_time = row["date"]
        end_time = start_time + timedelta(days=int(days))

        mask = (comp_df["pythontime"] > start_time) \
            & (comp_df["pythontime"] <= end_time)

        # Counts the number of unique page IDs in the mask.
        time_df.loc[index, "Number of Revisions"] = \
            comp_df.loc[mask].shape[0]


    # Plot the editted pages.

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    time_df.set_index("date", inplace=True, drop=True)

    time_df.plot()

    plt.xlabel("Month")
    plt.ylabel("Frequency")
    plt.title("Number of Revisions on Our Article Corpus")

    # plt.savefig("figures/Aggregated Edits Per Week")

    plt.show()

    return

if __name__ == "__main__":
    main()
