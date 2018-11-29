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
    
## Setup
To setup environment for the frontend app (/frontend), do ``yarn install`` or just ``yarn``.

To start, do ``yarn start`` 

To perform static type checking, do ``yarn flow``

