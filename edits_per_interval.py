'''
    Plots the number of edits, editors, and pages editted per time interval.

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

    # Denotes the number of days for the time interval.
    days = "7"

    time_df = pd.DataFrame(columns=["Revisions", "Editors", "Pages"])

    # Specify the analysis period here for the diagram.
    time_df["date"] = pd.date_range(start="2018-12-10", end="2019-12-10",
        freq=days + "D", tz="UTC")

    # Find the number of edits, editors, and pages editted per time interval in
    # days.
    for index, row in time_df.iterrows():

        start_time = row["date"]
        end_time = start_time + timedelta(days=int(days))

        mask = (comp_df["pythontime"] > start_time) \
            & (comp_df["pythontime"] <= end_time)

        # Counts the number of unique page IDs in the mask.
        time_df.loc[index, "Revisions"] = \
            comp_df.loc[mask].shape[0]
        
        # Counts anonymous users as individuals if they come from different 
        # IP addresses.
        time_df.loc[index, "Editors"] = \
            comp_df.loc[mask]["userid"].nunique()

        time_df.loc[index, "Pages"] = \
            comp_df.loc[mask]["page_id"].nunique()


    # Plot the editted pages.

    # https://stackoverflow.com/questions/52266076/plotting-using-pandas-and-datetime-format/52266133
    time_df.set_index("date", inplace=True, drop=True)

    time_df.plot()

    plt.xlabel("Months")
    plt.ylabel("Revisions/Editors/Pages Edited Count")
    plt.yscale("log")

    plt.tick_params(bottom=False)
    plt.legend(loc="upper left")

    # Toggle to save figure.
    # plt.savefig("figures/Aggregated Edits Per Week")

    plt.show()

    return

if __name__ == "__main__":
    main()
