# Lil-Data
The official repository for Team Lil Data, CMPT 732 final project at Simon Fraser University.
##### To visit the site please visit https://www.devxia.com/Lil-Data
## Repository structure:
* `2015 sample data`: sample Twitch stream dataset, shared by from  [Mr. Cong Zhang (congz@sfu.ca)](https://clivecast.github.io)
* `analysis`: Python code where we do analysis on 2015, 2018 Twitch, GiantBomb.com dataset, mostly using ``Apache Spark`` 
* `data collecting`: Crawler code that collect data from Twitch official api every 30 minutes, and fetch all games information from ``GiantBomb.com``  
* `ETL`: Extract, transform, load code written in ``Python``, using ``Apache Spark`` 
* `frontend`: web frontend written in ``JavaScript``, mostly in ``React.js``
* `docs`: production build of react web frontend
    
## Local Setup
[Yarn](https://yarnpkg.com/en/) is our package manager of choice for the frontend project, not to be confused with [Apache Hadoop YARN](https://hadoop.apache.org/docs/current/hadoop-yarn/hadoop-yarn-site/YARN.html) since this is also a "Big Data" project. 

To setup environment for the frontend app (/frontend), do ``yarn install`` or just ``yarn``.

To start, do ``yarn start`` 

To perform static type checking, do ``yarn flow``

## Analysis Results

Under 'results' folder

1. Top 20 most popular categories by evaluating their:
    1) Number of reviews on GiantBomb (which are all 0, though)
    2) Number of live streams that were broadcasting a game in this category
    3) Number of viewers that are watching a game in this category
    4) Number of followers that are following a channel that broadcasts this category of game

2. Best time frame to broadcast stream by evaluating:
    1) Number of streams:
        1) Number of streams in each time frame in each day
        2) Sum of number of streams in each time frame throughout entire data collecting period
        3) A trend of change of number of streams for each time frame throughout all days
    2) Number of veiwers:
        1) Number of viewers in each time frame in each day
        2) Sum of number of viewers in each time frame throughout entire data collecting period
        3) A trend of change of number of viewers for each time frame throughout all days

