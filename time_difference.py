'''
    Creates the time difference plot showing the interval of time between event
    start date and page creation date found in the creation_dates_analysis.csv
    file.

    Written by Jackie Chan and Kirby Mitchell.
'''

# Importing required packages/boilerplate code
import pandas as pd
import os
import sys
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import datetime as dt

from static_helpers import *

'''
    Function: get_creation_dates

    Input: The path to the creation dates CSV file.

    Output: Prints whether the file was successfully loaded and returns either
    the dataframe containing the contains of the file or None.
'''
def get_creation_dates(path):

    if file_exists(path):
        df = pd.read_csv(path)
        print("File was successfully loaded in.")
    else:
        print("FAIL: File was not loaded in.")

    return df

'''
    Function: format_date_columns

    Input: Takes the dataframe containing the creation dates and formats the
    dates/timestamps to a datatime object for later comparisons.

    Output: The same dataframe but the strings containing date/timestamp data
    is converted to datatime objects.
'''
def format_date_columns(dates_df):

    dates_df["Start Date"] = \
        pd.to_datetime(dates_df["Start Date"], format="%Y-%m-%d")
    dates_df["Page Creation Date"] = \
        pd.to_datetime(dates_df["Page Creation Date"], format="%Y-%m-%dT%H:%M:%SZ")

    return

'''
    Function: calculate_time_difference

    Input: Takes the dataframe containing all the creation dates and event start
    dates.

    Output: Generates two columns called Time Difference and Days Difference
    which are occupied by the time difference between creation dates and event
    start date. If creation date is before the event start date, then an error
    will print and the cell will remain as NaN for later removal.
'''
def calculate_time_difference(dates_df):

    for i, row in dates_df.iterrows():

        start_date = dates_df.at[i, "Start Date"]
        page_date = dates_df.at[i, "Page Creation Date"]

        if (start_date < page_date):
            dates_df.at[i, "Time Difference"] = page_date - start_date

            dates_df.at[i, "Days Difference"] = dates_df.at[i, "Time Difference"].days

        else:
            print("ERROR: {0} created before start date.".format(row["Titles"]))

    # print(dates_df[["Titles", "Time Difference", "Days Difference"]])

    return

'''
    Function: remove_errors

    Input: Takes the dataframe containing all the creation dates and event start
    dates.

    Output: Returns the same dataframe without the rows containing NaN because
    they were not calculated properly. Look at calculate_time_difference for the
    errors.
'''
def remove_errors(dates_df):

    dates_df = dates_df.dropna()

    return dates_df


def main():

    directory = "creation"
    file_name = "creation_dates_analysis.csv"
    complete_path = os.path.join(directory, file_name)


    # Generates the dataframe.
    dates_df = get_creation_dates(complete_path)

    format_date_columns(dates_df)

    calculate_time_difference(dates_df)

    dates_df = remove_errors(dates_df)

    dates_df = dates_df.sort_values(by=["Start Date"], ascending=False)
    # Finishes generating the dataframe.

    x = dates_df["Days Difference"].tolist()
    y = dates_df["Titles"].tolist()

    # Dictionary containing the color information for the diagram.
    colors = {
        'Siege of the Hong Kong Polytechnic University':'r',
        'Chinese University of Hong Kong conflict':'r', 
        'Death of Chow Tsz-lok':'orange', 
        'HKmap.live':'c', 
        'Death of Chan Yin-lam':'orange', 
        '2019 Prince Edward station attack':'r', 
        'Glory to Hong Kong':'c', 
        'Hong Kong Way':'r', 
        '2019 Yuen Long attack':'r', 
        'Storming of the Legislative Council Complex':'r', 
        '12 June 2019 Hong Kong protest':'r', 
        '2019–20 Hong Kong protests':'r', 
        '2019 Hong Kong extradition bill':'m', 
        'Murder of Poon Hiu-wing':'orange', 
        'Hong Kong Human Rights and Democracy Act':'m', 
        'Lennon Wall (Hong Kong)':'c', 
        'Umbrella Movement':'r', 
        'Demosistō':'g', 
        'Civil Human Rights Front':'g'
    }

    fig, ax = plt.subplots()

    # Plots the points individually.
    for i, j in zip(x, y):
        
        # Fixes rounding issue with the days.
        if (i >= 1.0):
            plt.scatter(i, j, c=colors[j])
        else:
            # Rounds up the day if it is below twenty-four hours.
            plt.scatter(1.0, j, c=colors[j])

    plt.xlabel("Time Difference (days)")

    # Constructing legend.
    red_dot = mlines.Line2D([], [], color="r", marker="o", linestyle="None",
        markersize=5, label="Protests/Attacks")
    orange_dot = mlines.Line2D([], [], color="orange", marker="o",
        linestyle="None", markersize=5, label="Deaths")
    cyan_dot = mlines.Line2D([], [], color="c", marker="o", linestyle="None",
        markersize=5, label="General/Miscellaneous")
    magenta_dot = mlines.Line2D([], [], color="m", marker="o", linestyle="None",
        markersize=5, label="Policies/Legislation")
    green_dot = mlines.Line2D([], [], color="g", marker="o", linestyle="None",
        markersize=5, label="Actors/Organizations")
    plt.legend(handles=[red_dot, orange_dot, cyan_dot, magenta_dot, green_dot],
        loc="lower right")

    # https://stackoverflow.com/questions/14530113/set-ticks-with-logarithmic-scale
    ax.set_xscale("log")
    ax.set_xticks([1, 7, 30, 60, 100, 365, 1000])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())

    fig.set_size_inches(10, 5, forward=True)

    plt.grid(True)

    plt.tight_layout()

    plt.savefig("figures/Time Difference Diagram", dpi=300)

    plt.show()

    return

if __name__ == "__main__":
    main()