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

### `pull_data.py`
Contains all the code that pulls the relevant, necessary data for analysis. This includes: `creation/creation_dates.csv`, `10 Year Redirect Data/*`, and `10 Year Revision Data/*`. If data needs to be updated, delete the relevant file and rerun the relevant helper function to pull that data. These *user-facing* functions include: `generate_creation_dates_data()`, `generate_revision_data()`, and `generate_redirect_data()`.

*Note: `main.py` access MediaWiki API using a Wiki bot user account with login credentials stored in `credentials.txt` which is excluded via `.gitignore`.*

### `create_comp_csv.ipynb`
Contains the code that generates the `10year.csv` file that concatenates all the .csv files in `10 Year Revision Data`.

### `time_diagram.ipynb`
Contains the code that generates the `day_difference_figure.png` file. It generates this data with the `creation_dates_analysis.csv` file which contains the event start dates and their page creation dates that were manually inputted and cited in the `start_dates_doc.md`.

### `revision_analysis.ipynb`
Contains the code that generates both `desc_all.csv` and `desc_page.csv`. This notebook requires the revision data contained in the `10 Year Revision Data` directory.

### `stats.py`
Contains code for calculating the top ten articles and for making plots of number of revisions over time.

### `corrleation.py`
Contains code that generates `pageviewCorr.csv`, `revisionCorr.csv`, and `pageview-revisionCorr.csv` (top 5). Also `allPageviewCorr.csv`, `allRevisionCorr.csv`, and `allPRCorr.csv` that contain all the correlation data for hierarchical clustering. Uses the data from `pull_data.py` and `wmlflabs.py` to do the analysis; returns Pearson's coefficient using the built-in Pandas analysis.

### `table.py`
Generates the pre-analysis table that review the top 10 articles by revision count and the totals for the top 10 and the entire corpus.

### `wmflabs.py`
Helper code that automates the downloading and reformatting of pageview data from the WikiMediaFoundation Labs tool (WMF). Uses `titles.txt` for reference. Utiles the Selenium library with a Linux Firefox geckodriver for web rendering.

### `reformat_pageview_files.py`
Helper code for manual downloading of pageview files from the WMF labs tool. Mainly used to add pages outside of the automatic tool.

### `median_top_ten.py`
Plots the median edit size from top ten articles per time interval (in days) using the data from `10 Year Revision Data`.

### `pages_edited.py`
Plots the number of pages edited per time interval (in days) using the data from the `10 Year Updated.csv`.

### Bot Login
Allows authenciated requests to the MediaWiki API for less restricted access. Follows guidelines here: https://www.mediawiki.org/wiki/API:Login
