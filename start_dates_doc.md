# Documentation and Citations for Start Date Column in `creation_dates_analysis.csv`
`creation_dates_analysis.csv` is a copy of `creation_dates.csv` without talk 
pages and articles that do not have recent start dates, e.g. Hong Kong. These 
articles will not be relevant to our analysis as we are trying to look at the 
delay between event start time and page creation time.

In addition to copying and deleting irrelevant articles, 
`creation_dates_analysis.csv` was also reindex using the Pandas function
`reset_index(inplace=True, drop=True)` on the dataframe. Further analysis will
be done in a Jupyter Notebook file located in the root directory.


All articles with start dates in `creation_dates_analysis.csv` will have 
relevant citations below for the date we chose. These citations will mainly be 
news articles. We will *not* be using Wikipedia articles for our citations as 
they can change.

# Removed Titles
Hong Kong, List of {early 2019, July 2019, August 2019, September 2019,
October 2019, November 2019, December 2019, January 2020} Hong Kong protests,
Carrie Lam, Tactics and methods surrounding the 2019-20 Hong Kong protests,
Causes of  the 2019-20 Hong Kong protests, Art of the 2019-20 Hong Kong
protests, List of protests in Hong Kong, 2019 Hong Kong local elections,
Hong Kong-Mainland China conflict, "One Country, two systems", Government of 
Hong Kong


# 2019-20 Hong Kong protests: 3/15/19


2019-20 Hong Kong protests: https://en.wikipedia.org/wiki/2019%E2%80%9320_Hong_Kong_protests
Look at Date on summary.

2019 Hong Kong extradition bill: https://en.wikipedia.org/wiki/2019_Hong_Kong_extradition_bill
Using date that bill was published.

Murder of Poon Hiu-wing: https://en.wikipedia.org/wiki/Murder_of_Poon_Hiu-wing
Look at Date on summary.

Demosistō: https://en.wikipedia.org/wiki/Demosist%C5%8D
"The party was officially established on 10 April 2016"

Civil Human Rights Front: https://en.wikipedia.org/wiki/Civil_Human_Rights_Front
"Civil Human Rights Front was founded on 13 September 2002"

Hong Kong Human Rights and Democracy Act: https://en.wikipedia.org/wiki/Hong_Kong_Human_Rights_and_Democracy_Act
"Introduced in the Senate as... on June 13, 2019"

Chinese University of Hong Kong conflict: https://en.wikipedia.org/wiki/Chinese_University_of_Hong_Kong_conflict
Look at Date on summary.

Death of Chow Tsz-lok: https://en.wikipedia.org/wiki/Death_of_Chow_Tsz-lok
"...occurred on 8 November 2019"

Siege of the Hong Kong Polytechnic University: https://en.wikipedia.org/wiki/Siege_of_the_Hong_Kong_Polytechnic_University
Look at Date on summary.

2019 Yuen Long attack: https://en.wikipedia.org/wiki/2019_Yuen_Long_attack
"occurred on 21 to 22 July 2019"

Storming of the Legislative Council Complex: https://www.npr.org/2019/07/01/737556501/hong-kong-protesters-take-down-wall-at-legislative-council-as-officials-mark-han
"Protesters charged Hong Kong's Legislative Council building Monday (July 1st)"

Hong Kong Way: https://www.nbcnews.com/news/world/hong-kong-protesters-form-28-mile-human-chain-demanding-democracy-n1045716
"HONG KONG — Hand-in-hand, protesters formed a 28-mile human chain across 39 train stations in Hong Kong on Friday.(August 23)"

2019 Prince Edward station attack: https://www.bbc.com/news/world-asia-china-49540751
"People took to the streets on Saturday (August 31) to..."

Death of Chan Yin-lam: https://asiatimes.com/2019/10/friends-not-convinced-girls-death-was-suicide/
"...body was found in the sea off Yau Tong on September 22."

12 June 2019 Hong Kong protest: https://www.nytimes.com/2019/06/12/world/asia/hong-kong-protest-extradition.html
"Riot police officers turned downtown Hong Kong into a tear-gas-filled battlefield on Wednesday (June 12)..."
