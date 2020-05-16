'''
    Creates dendrograms of article correlations.

    Written by Jackie Chan and Kirby Mitchell.
'''
import pandas as pd
import numpy as np
from static_helpers import *
import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
from scipy.cluster import hierarchy

# Function that duplicates the values from the passed in DataFrame, but switches
# the associated values in the Article columns. Used in case the correlation
# from Article A to Article B is in the DataFrame but not Article B to Article A
def mirror_table(df):
    mirror_df = pd.DataFrame(columns = ['Article 1', 'Article 2', 'Corr.'])
    for index, row in df.iterrows():
        mirror_df = mirror_df.append(pd.DataFrame([[row["Article 2"], row["Article 1"], row["Corr."]]], columns=["Article 1", "Article 2", "Corr."]))
    return mirror_df

# Function that creates an n x n matrix from the provided csv file that contains
# article correlations. Returns the matrix.
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

# Main method that creates dendrograms for page view correlations and page
# revision correlations.
def main():
    # Names of the files that contain the relevant correlation values.
    pageViewsCorrelations = "allRevisionCorr.csv"
    pageRevisionsCorrelations = "allPageViewCorr.csv"
    # Creates n x n matrix of article correlation values.
    df = make_table(pageRevisionsCorrelations)
    # Negate the values in the correlation, then add 1 so that the highest
    # correlation values will be considered the ones with minimum distance
    # between them by the single-linkage algorithm.
    df = df.mul(-1)
    df = df.add(1)
    df = df.replace(np.NaN, 0)
    # Format n x n matrix into condensed distance matrix.
    distArray = ssd.squareform(df)
    # Create dendrogram using the single-linkage algorithm implemented by SciPy.
    # Source for Dendrogram code: https://python-graph-gallery.com/401-customised-dendrogram/
    Z = hierarchy.linkage(distArray, 'single')
    hierarchy.dendrogram(Z, leaf_rotation=90, leaf_font_size=8, labels=df.index)
    plt.gcf().subplots_adjust(bottom=0.65)
    plt.savefig("figures/Page Revision Correlation Dendrogram")
    plt.show()
    return

if __name__ == "__main__":
    main()
