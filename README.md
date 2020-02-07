# wiki-comps-2020
Carleton College CS Comps

Advisor: Sneha Narayan

Students: Jackie Chan, James Gardner, Junyi Min, Kirby Mitchell

Source: http://www.cs.carleton.edu/cs_comps/1920/wikipedia/index.php

Paper: https://doi.org/10.1145/2998181.2998232

## api_project.py
    Contains code for collecting redirects, revisions, pageids, and pageviews via MediaWiki API. Accesses the API using a Wiki bot user account with login credentials stored in "credentials.txt" which is excluded via gitignore.

    Broken into sections separated by docstring quotes denoting what each section is. The sections are: helper functions, bot login, data collection functions, and data collection.

### Helper Funtions:

#### printJsonTree:
    Pretty-prints a JSON/Python dictionary recursively showing dictionary keys and their corresponding values in byte-size. Mainly a helper function for debugging purposes.

#### printQueryErrors:
    Pretty-prints JSON/Python dictionary result from the MediaWiki API. Will print to the terminal if there are any errors, or print a success message if there are no errors. Mainly a helper function for debugging purposes.

#### hasError: 
    Returns True or False based on the MediaWiki API results. A helper and safety function to ensure queries do not crash the script.

### Bot Login
    Allows authenciated requests to the MediaWiki API for less restricted access. Follows guidelines here: https://www.mediawiki.org/wiki/API:Login

### Data Collection Functions

#### getRevisions
    Input: pageID, startDate, endDate (epoch times)
    Output: list of dictionaries containing revisions between date range. Returns timestamp, editor, editor id, revision id, and size in bytes of edit. 

#### getPageviews
    Input: pageID
    Output: list of dictionaires containing date and pageview count.

#### getRedirects
    Input: pageID, startDate, endDate (epoch times)
    Output: all redirects to the page within the time range as a list of dictionaries.

### Data Collection
    Contains code to collect data on a list of Wiki page titles and saves the results in csv files using pandas. Stores files in a folder called "data" and the names of the files are the titles with modifications to allow for valid filenames. Also gets Talk page information by adding "Talk:" to the front of each page title.

## stats.py
    Contains code for calculating various metrics such as Jaccard Similarity or correlations between pages and creating plots. 