// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'

const DataCollecting = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>

                <div className={styles.charts}>
                    <ul>
                        <li><code>2015 sample data</code>: sample Twitch stream dataset, shared by from  <a href="https://clivecast.github.io">Mr. Cong Zhang (congz@sfu.ca)</a></li>

                        <li><code>analysis</code>: Python code where we do analysis on 2015, 2018 Twitch, GiantBomb.com dataset, mostly using <code>Apache Spark</code>


                            <ul>
                                <li><code>most_popular_category.py</code>: Evaluate the popularity of a category using four different perspectives</li>

                                <li><code>Best_time_of_stream.py</code>: Evaluate the best time in a day for streaming</li></ul>
                        </li>

                        <li><code>data collecting</code>: Crawler code that collect data from Twitch official api every 30 minutes, and fetch all games information from <code>GiantBomb.com</code> <br />


                            <ul>
                                <li><code>crawl_twitch.py</code>: Made use of twitch api to access and download live streaming data from twitch database. The work was running with multi-threads every half an hour, from 11/13/2018 to 11/26/2018. About 50 gigabytes of data were collected at the end</li>

                                <li><code>fetch_games.py</code>: Used api provided by Giantbomb.com to collect game data from its database</li>

                                <li><code>get_giantbomb_genre.py</code>: With guid of game, which was collected from Giantbomb api, call another api from Giantbomb to get detailed game information, including genres</li></ul>
                        </li>

                        <li><code>ETL</code>: Extract, transform, load code written in <code>Python</code>, using <code>Apache Spark</code>


                            <ul>
                                <li><code>twitch_raw_data_clean.py</code>: grab useful features for <code>stream</code> objects and <code>channel</code> objects from dirty json files</li>

                                <li><code>twitch_dataframe_ETL.py</code>: reconstruct the dataframe using customized schema</li>

                                <li><code>giantbomb_game_info_ETL.py</code>: grab useful features for <code>game</code> objects from dirty json files</li>

                                <li><code>join_with_giantbomb.py</code>: join <code>stream</code> with <code>game</code>, creating a new table including both stream and game information</li>

                                <li><code>read_guid.py</code>: get game <code>genres</code> from dirty json files</li></ul>
                        </li>

                        <li><code>frontend</code>: web frontend written in <code>JavaScript</code>, mostly in <code>React.js</code></li>

                        <li><code>docs</code>: production build of react web frontend</li>
                    </ul>
                </div>
            </div>

        </main>
    )
}

export default DataCollecting
