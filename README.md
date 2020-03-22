# wiki-comps-2020 Project Description
Carleton College Computer Science Comps

__Advisor:__ Sneha Narayan

__Students:__ Jackie Chan, James Gardner, Junyi Min, Kirby Mitchell

__Source:__ http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php

__Paper:__ https://doi.org/10.1145/2998181.2998232

__Project Task Board:__ https://github.com/gadeuneo/wiki-comps-2020/projects/1

# Codebase Overview

### `titles.txt`
Contains all the Wikipedia articles in our analysis.

### `main.py`
Contains all the code that pulls the relevant, necessary data for analysis. This includes: `creation/creation_dates.csv`, `10 Year Redirect Data/*`, and `10 Year Revision Data/*`. If data needs to be updated, delete the relevant file and rerun the relevant helper function to pull that data. These *user-facing* functions include: `generate_creation_dates_data()`, `generate_revision_data()`, and `generate_redirect_data()`.

*Note: `main.py` access MediaWiki API using a Wiki bot user account with login credentials stored in `credentials.txt` which is excluded via `.gitignore`.*

### `wiki_notebook.ipynb`
Contains the code that generates the `10year.csv` file that concatenates all the .csv files in `10 Year Revision Data`.

### `stats.py`
Contains code for calculating various metrics such as Jaccard Similarity or correlations between pages and creating plots.

### Bot Login
Allows authenciated requests to the MediaWiki API for less restricted access. Follows guidelines here: https://www.mediawiki.org/wiki/API:Login