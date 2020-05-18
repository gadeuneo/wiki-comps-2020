# wiki-comps-2020 Project Description
Carleton College Computer Science Comps

__Advisor:__ Sneha Narayan

__Students:__ Jackie Chan, James Gardner, Junyi Min, Kirby Mitchell

__Source:__ http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php

__Paper:__ https://doi.org/10.1145/2998181.2998232

# Codebase Overview

### `cluster.py`
Creates dendrograms based on hierarichal clustering from correlation values based on pageviews, revisons, and pageview-revisons. NOTE: must run `correlation.py` first to get the calculated values.

### `corrleation.py`
Contains code that generates `pageviewCorr.csv`, `revisionCorr.csv`, and `pageview-revisionCorr.csv` (top 5). Also `allPageviewCorr.csv`, `allRevisionCorr.csv`, and `allPRCorr.csv` that contain all the correlation data for hierarchical clustering. Uses the data from `pull_data.py` and `wmlflabs.py` to do the analysis; returns Pearson's coefficient using the built-in Pandas analysis.

### `corpus_unique_editors.py`
Plots unique editors aggregated across corpus - monthly unique editors across corpus. NOTE: must run `pull_data.py` first for making plots.

### `create_comp_csv.ipynb`
Contains the code that generates the `10 Year Updated.csv` file that concatenates all the .csv files in `10 Year Revision Data`.

### `editor_fraction.py`
Plots fraction of top 10 articles' editors by revison count that edit a page on the non-top 10 articles on daily basis.

### `edits_per_interval.py`
Plots aggregate number of edits, editors, and pages edited for different time intervals.

### `jaccard_editorpagecount.py`
Plots pagecount vs number of editors with normalization based on the number of pages being actively editied.

### `jaccard.py`
Plots Jaccard similarity scores for the top 10 articles by revision count in a single plot. Plots individual Jaccard similarity scores for articles.

### `median_top_ten.py`
Plots the median edit size for the top 10 articles by revision count for 14 day periods.

### `multiline.py`
Plots revision activity for the top 10 articles by revision count on a single figure.

### `pageviews.py`
Plots pageviews for articles: top 4 most correlated, single pages, and aggregate plots.

### `pull_data.py`
Contains all the code that pulls the relevant, necessary data for analysis. This includes: `creation/creation_dates.csv`, `10 Year Redirect Data/*`, and `10 Year Revision Data/*`. If data needs to be updated, delete the relevant file and rerun the relevant helper function to pull that data. These *user-facing* functions include: `generate_creation_dates_data()`, `generate_revision_data()`, and `generate_redirect_data()`.

*Note: `main.py` access MediaWiki API using a Wiki bot user account with login credentials stored in `credentials.txt` which is excluded via `.gitignore`. The bot user allows authenciated requests to the MediaWiki API for less restricted access. Follows guidelines here: https://www.mediawiki.org/wiki/API:Login*

### `reformat_pageview_files.py`
Manually reformats downloaded pageview file data from the WikiMedia Foundation Labs tool (WMF labs).

### `requirements.txt`
List of required Python packages to run files in the repository.

### `static_helpers.py`
Contains helper functions for use by multiple files.

### `table.py`
Generates a table that reviews the top 10 articles by revision count and the totals for the top 10 and the entire corpus.

### `time_difference.py`
Contains the code that generates the `day_difference_figure.png` file. It generates this data with the `creation_dates_analysis.csv` file which contains the event start dates and their page creation dates that were manually inputted and cited in the `start_dates_doc.md`.

### `titles.txt`
Contains all the Wikipedia articles in our analysis.

### `wmflabs.py`
Helper code that automates the downloading and reformatting of pageview data from the WikiMediaFoundation Labs tool (WMF). Uses `titles.txt` for reference. Utiles the Selenium library with a Linux Firefox geckodriver for web rendering.


