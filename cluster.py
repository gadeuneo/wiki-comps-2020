'''
    Creates Hierarchical Clustering graphs of article correlations. Or something?

    Written by Jackie Chan and Kirby Mitchell.
'''

import pandas as pd
from static_helpers import *
import matplotlib.pyplot as plt
import networkx as nx

def mirror_table(df):
    mirror_df = pd.DataFrame(columns = ['Article 1', 'Article 2', 'Corr.'])
    for index, row in df.iterrows():
        mirror_df = mirror_df.append(pd.DataFrame([[row["Article 2"], row["Article 1"], row["Corr."]]], columns=["Article 1", "Article 2", "Corr."]))
    return mirror_df

def make_table(file):
    table_df = pd.read_csv(file)
    mirror_df = mirror_table(table_df)
    full_table_df = pd.concat([table_df, mirror_df], ignore_index=True, sort=False)
    # Convert dataframe to n x n table where articles are the rows/columns and
    # correlation values are values.
    # Source: https://stackoverflow.com/questions/47683642/how-to-create-a-square-dataframe-matrix-given-3-columns-python
    full_table_df = full_table_df.pivot(index= 'Article 1', columns= 'Article 2', values= 'Corr.')
    # Correlation between same article is NaN.
    return full_table_df

def main():
    table_df = make_table("allPageViewCorr.csv")
    #print(table_df)
if __name__ == "__main__":
    main()
