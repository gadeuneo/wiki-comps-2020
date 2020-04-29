'''
    Creates a CSV file concatenating all the revisions dataframes into one
    comprehensive dataframe for analysis.

    Written by Jackie Chan.
'''

import pandas as pd
import os
import sys
import time
import matplotlib.pyplot as pyplot
import numpy

from static_helpers import *

def create_df_dictionary(titles, directory):

    df_dict = {}

    for title in titles:
        complete_path = os.path.join(directory, title)

        if file_exists(complete_path):
            df_dict[title] = pd.read_csv(complete_path)

            # Creates pythontime column which is converted from the timestamp
            # column.
            df_dict[title]["pythontime"] = \
                pd.to_datetime(df_dict[title]['timestamp'])

            # Sorts each dataframe by pythontime.
            df_dict[title].sort_values(by="pythontime", inplace=True)

        else:
            print("File was not added to dictionary: {0}".format(title))

    return df_dict

def print_editor_details(comp_df):

    anon_df = comp_df[comp_df["anon"] == True]
    reg_df = comp_df[comp_df["anon"] != True]

    unique_anon_editors = anon_df["user"].nunique()
    unique_reg_editors = reg_df["user"].nunique()

    print("Registered Editors: {0}".format(unique_reg_editors))
    print("Anon Editors: {0}".format(unique_anon_editors))

    return

def print_edit_size_details(comp_df):

    mean_edit_size = comp_df["size"].mean()
    median_edit_size = comp_df["size"].median()

    print("Mean Edit Size: {0} bytes".format(mean_edit_size))
    print("Median Edit Size: {0} bytes".format(median_edit_size))

    return

def main():

    comp_df_file_name = "10 Year.csv"

    titles = get_titles_and_talk_pages()
    titles = [title + ".csv" for title in titles]

    directory = "10 Year Revision Data"
    df_dict = create_df_dictionary(titles, directory)


    df_list = []

    # Appends all dataframes in dictionary to df_list.
    for key in df_dict.keys():
        df_list.append(df_dict[key])

    comp_df = pd.concat(df_list, ignore_index=True, sort=False)
    comp_df.sort_values(by="pythontime", inplace=True)



    if not file_exists(comp_df_file_name):
        comp_df.to_csv(comp_df_file_name)

    print_editor_details(comp_df)
    print_edit_size_details(comp_df)

    return


if __name__ == "__main__":
    main()