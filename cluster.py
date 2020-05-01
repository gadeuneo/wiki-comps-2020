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
    df = make_table("allPageViewCorr.csv")

    # Creates a series that has the articles paired with their highest
    # correlation values.
    max_series = df.max()

    # Finds the first article name that has the max correlation value out of
    # the series of max correlation values.
    first_max_article = max_series.idxmax()

    # Gets the series associated with the label found earlier to find the article
    # that makes the max correlation value.
    article_series = df.loc[first_max_article]

    # This is the second article that pairs with the one found earlier to make
    # the max correlation value.
    second_max_article = article_series.idxmax()

    # Variable for holding the max correlation value out of the data frame.
    max_correlation_value = df.loc[first_max_article, second_max_article]
    print("Highest Correlation: ", df.loc[first_max_article, second_max_article]
    , "\n Articles: ", first_max_article," ", second_max_article)
    # while df.shape[0] != 1:
    #     df.max()
    # print(df)

    # graph = nx.from_pandas_adjacency(df)
    # graph.name = "Whatever"
    #
    # print(nx.info(graph))
    #
    # print(type(graph))
    #
    # nx.draw(graph)
    # plt.show()

    return

if __name__ == "__main__":
    main()
