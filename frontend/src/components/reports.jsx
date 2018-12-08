// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'

const Reports = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis'
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>

                <div className={styles.reports}>
                    <div className={styles.title}>Lil’ Report</div>
                    <div className={styles.notes}>
                        The styling might be off, <a href='https://www.devxia.com/Lil-Data/assets/img/report.pdf' target='_blank'>click here to check the pdf version of the report.</a>

                        <br/>
                    </div>
                    <div className={styles.reportContainer}>
                        <p><b>Chuangxin Xia, cxa25; Chengxi Li, chengxil; Aisuluu Alymbekova, aalymbek; Risheng Wang, rishengw</b></p>

                        <p>1.1 Problem definition</p>

                        <ul>
                            <li>There is a huge amount of raw data on the internet that is generated every second which is not meaningful or comprehensible in any way. The objective of the project was to convert data into meaningful information by collecting data from sources like Twitch and Giantbomb, process it to detect interesting insights and observations about Twitch streaming service and game industry as a whole and visualize it. The major challenge was the process of data gathering and the absence of uniformity of the data. Along with that, blindly joining data would not give any value to the analysis, so understanding what kind of observations will be relevant and gripping was important.</li>
                        </ul>

                        <p>1.2 Target and Challenges</p>

                        <ol>
                            <li>1)Popularity of a game/category/stream/channel:</li>
                        </ol>

                        <p>Challenges come from how we are going to measure &#39;popularity&#39;. There are multiple perspectives out there and we need to make each of them looks convincing and meaningful. This means that the results we use must be reasonable and accurate so that they make sense. Such as number of streams vs. number of viewers regarding the popularity of a game. Which one makes more sense on conveying the concept?</p>

                        <p>And remember, we are dealing with 50 gigabytes&#39; data. The challenge could arise from the very beginning of the process: how we are going to ETL the data so that we could fetch the necessary information to convey a sense of popularity of some object.</p>

                        <p>Furthermore, the data we collected could lack the required information we need to lead to a result. Actually, twitch does not provide category data for games. We may find more of this kind of issue as we are making progress</p>

                        <ol>
                            <li>2)Popularity in time frame scale:</li>
                        </ol>

                        <p>The challenge is simple: how do we define &#39;time frame&#39;? We can arbitrarily make some definition, but the result could seems ridiculous based on our &#39;guess&#39;. When is morning, noon, afternoon and night? What about time zones and do we really need to consider about that?</p>

                        <ol>
                            <li>3)Make simple prediction about popularity of a streamer in the near future:</li>
                        </ol>

                        <p>&#39;Prediction&#39; could be the most tricky part in our project. First of all, we actually lack useful data to conduct predictions. Twitch does not have any information about users: age, nationality, education level, and so on. Furthermore, how could we make prediction for a future object, when we actually do not know the value of a feature for that object in the future? For example, we want to use number of followers of channel as a part of feature vector, but number of followers is a variable that could change along the time. To make a prediction, we need the number of follower for that channel in the future. And that is impossible to know.</p>

                        <p>The limitation of useful information we collect from twitch becomes a challenge for us to dig deep into the data. If we want to conduct reasonable investigation on the data in depth, we have to make full use of existing information.</p>

                        <ol>
                            <li>Methodology</li>
                        </ol>

                        <ul>
                            <li>ETL:</li>
                        </ul>

                        <p>ETL work took a lot of effort because the data we download using twitch api and giantbomb api was dirty. First made advantage of python regular expression operation package to clean the collected json files, such as removing the tail comma, so that they could be read by pyspark. Afterwards, mainly use pyspark to convert json strings into featurized dataframes.</p>

                        <p>Dataframe is suitable with our project, because it provides well-structured table frame, to which data with multiple features well fits. Furthermore, Dataframe is managed by using sql like functions. It also provides users with API that enables hardcoded sql queries. This sql-user-friendly feature makes it easy to handle complex data.</p>

                        <p>The original data was splitted into three tables: stream table, which contains information about the stream, including stream id, game, created time of the stream and or so; channel table, which was separated from stream data, that describes the channel owner who was broadcasting corresponding stream; game table, which was a joined table from stream data and game details from giantbomb. The reason to separate data in this way, is that it matches the three main topics we want to conduct on the data, namely stream, channel and game.</p>

                        <ul>
                            <li>EDA:</li>
                        </ul>

                        <p>The exploratory data analysis, as explained on wikipedia, is usually a method used to describe the hidden characteristics of the data helping the formulation of the hypothesis regarding various aspects of the data through mainly visualization methods.</p>

                        <p>First of all, we selected a group of results that are more appealing for visualization and teammate responsible building the website puts all of the selected results to our website and used</p>

                        <p>As mentioned earlier, we used different standards for measuring popularities of games, channel, language and so on. The reason behind this is that we were trying to get a sense of for example, popularity, from each possible point of view and hence getting a full depiction of the popularity on each subjects (eg.games, channels).  However, the results on certain topics from each perspective do not vary much and sometimes stays the same. For example, fortinet is the most popular game played on twitch by both view count and number of streamer played. As you can see from one of our graph used on the website, fortnite, red hot as it is, dwarfs all other games, classic or newly released. Therefore, we only selected a few results from data analysis to represent some of the topics for our website.</p>

                        <p>Among all of the analysis of twitch data, not all of the results are suitable for making simple and concise graphs either because it contains so few numbers or because it is a bit too complicated.</p>

                        <p>For example is the one of the results for analyzing the what channels are popular and what languages does each streamer speaks, the resulting table looks like:</p>

                        <p><img src="cid:Image_0.png" /></p>
                        <img height='300px' width='500px' src='../assets/img/sc0.png'
                             alt='Screenshots of sample channel and language analysis result '/>

                        <pre>             Figure 2. sample channel and language analysis result
</pre>

                        <ul>
                            <li>MLLib:</li>
                        </ul>

                        <p>Since we had plenty of data collected, we could make predictions about the popularity of games and categories using Apache Spark Machine Learning Library. We have decided to make prediction on how many viewers will Top-20 games will have and which categories will be most popular on January 1, 2019. We identified it as a regression problem, since it requires the prediction of a continuous value.</p>

                        <p>At first, we selected stream data that can be used as features and split it into training and validation sets, however, the model cannot be trained on textual data. To resolve that we used SQLTransformer to transform the dates using UNIX_TIMESTAMP() to get number value of the date and hash the name of the games and categories. The features to train the model are: date in UNIX format, hashed name of the game or category and day of the week (since it also affects how many people are watching streams), to combine the features VectorAssembler was used. We ran several attempts to train a model using Linear Regressor, General Linear Regressor, but DecisionTreeRegressor has shown best predictions and that&#39;s what we kept in our final implementation. After the pipeline model was trained on the whole dataset, we attempted to make predictions on the popularity of the games and categories. The results are provided on our website.</p>

                        <ol>
                            <li>Problems</li>
                        </ol>

                        <p><strong>ETL</strong> :</p>

                        <ul>
                            <li>After cleaning original data, we found out that it does not readable column names for features. So we make customized schema to solve the issue</li>

                            <li>The original data was messed up. One significant problem was that twitch allows users to manually type in the game name they are broadcasting. This leads to severe problems such as typo, mixed lower and upper cases, or just random names. At very first we tried to use Levenshtein distance algorithm to deal with typo, but at last it was proved to be useless because the algorithm cannot tell whether the name had some typo or merely was another game. At the end, we have to roughly filter out &#39;irregular&#39; names. That is, names of games which had few viewers. And we convert all names to lower cases in order to make a better join with data from giantbomb.</li>

                            <li>In order to analyze data on time frame scale, we need a new column representing what period of day the stream was being broadcast. So we discussed and decided to break a day into six different time pieces.</li>

                            <li>Original time data contains minitues, needed to be converted into simple yyyy-mm-dd format.</li>
                        </ul>

                        <p><strong>Data Analyze</strong> :</p>

                        <ul>
                            <li>Cannot simply count the number of streams, because we collect data every 30 minutes, and the same stream could appear multiples times in our data. Before counting, have to select distinct stream id</li>

                            <li>Cannot simply sum up the number of viewers for a game. The reason is similar to that of number of streams, while this time, number of viewers for one stream could vary. We choose to compute the max or average value for number of viewers for each stream at first, and sum them up to the total number of viewers for each game or category or time frame afterwards</li>

                            <li>Number of games exceeds number of categories that could be handled by StringIndexer. Instead, we hash code the game name</li>
                        </ul>

                        <ol>
                            <li>Results</li>
                        </ol>

                        <p>Brief explaination of the charts</p>

                        <p><strong>Game popularity</strong> :</p>

                        <p>Table shows the top 20 most popular games played on twitch with corresponding total number of streams(videos) in the duration from 2018-11-13 to 2018-11-26. The bar chart on the right shows that Fortnite is by far the most popular game played on twitch (about 4.6 times more than the 2nd game).</p>

                        <p><strong>Category popularity</strong></p>

                        <p>All of the web pages for this topic follows the same layout style of table on the left and chart(s) on the right.</p>

                        <p>Each game can have more than 1 categories (tags). For example, a game like Fortnite falls in both shooter and MMORPG categories.</p>

                        <ol>
                            <li>1)<em>*By stream count</em>*</li>
                    </ol>

                    <p>The table listed top 20 most popular game genre/category by total stream count for each genre. Top 3 categories are Shooter, First-Person-Shooter and Action, they consumed more than half of the total streams played on twitch.</p>

                    <p>In other words, there is 1 in every 2 streamers on twitch streamed themselves playing games in these 3 categories.</p>

                    <p>The &#39;half-pie&#39; chart provides a more focused view on rest of the categories by minimize the visual effects of the most popular category.</p>

                    <ol>
                        <li>2)<em>*By viewers</em>*</li>
                </ol>

                <p>Same idea but using total view count as basis of measuring category popularity.</p>

                <p>Top 3 categories are the same. They still takes half of the pie chart means that half of the people who watched videos on twitch are watching games in these 3 categories.</p>

                <ol>
                    <li>3)<em>*By followers</em>*</li>
            </ol>

            <p>Using total followers count, the top 3 categories are the same, but only takes one third of the entire fan base. The fan base stood strong for other less popular categories.</p>

            <ol>
                <li>4)<em>*>By languages</em>*</li>
        </ol>

    <p>This time, bar charts shows the total number of viewers for each languages used on twitch. People watch streams in english predominantly since most of the streams are in english. The table on the left shows the most popular categories for each popular languages by viewers count.</p>

    <p><strong>Channel popularity</strong></p>

    <p>Table on the left shows the top 20 most popular channels on twitch by total follower counts with additional information of if the streamer&#39;s channel is labelled &#39;mature&#39; and if this channel is a officially registered partner of twitch.</p>

    <p>Ninja, the most popular streamer, has the largest fan base, counting almost 25% of the entire fan population.</p>

    <p><strong>Time frame popularity</strong></p>

    <p>All time used PST, first graph shows that the number of streams and number of viewers has a nice little phase difference which represents the accumulation of the audiences while the stream is playing.</p>

    <p>Another interesting observation is that the total number of streams and audiences drops a little in late-night since only the true-hard-core streamers and viewers will stay up super late for the games they love.</p>

    <p>The charts below are showing the distributions of total number of streams and viewers for each time frame throughout the duration of the period of data collection.</p>

    <p>The diagram at the bottom shows the distribution of total viewers count through each days of the week. Tuesday seems to be the ramadan day for most of the gamers and streamers.</p>

    <p><strong>Language popularity</strong></p>

    <p>The line chart shows the most popular languages used for broadcasting on twitch by total number of channels.</p>

    <p>As discussed earlier, majority of streamers on twitch use English but German, French, and Spanish twitch streamer also formed their own gaming community on twitch.</p>

    <p><strong>Predictions</strong></p>

    <p>The top table and bar chart illustrate the predicted number of viewers for the most popular games on January 1, 2019. As expected, Fortnite is topping the rating, followed by Call of Duty and Overwatch.</p>

    <p>The bottom chart demonstrate top 20 categories that will be popular on January 1, 2019. As seen in the results, Shooter, First-Person Shooter and Action games will continue to be among the top categories in the future.</p>

    <ol>
        <li><strong>Project Summary</strong></li>
    </ol>

    <ul>
        <li>Getting the data: Acquiring/gathering/downloading: 3.0


            <ul>
                <li>We collect data from twitch and giantbomb, in total 50 gigabytes</li></ul>
        </li>

        <li>ETL: Extract-Transform-Load work and cleaning the data set: 3.0


            <ul>
                <li>The data was noisy and huge so that ETL took much effort</li></ul>
        </li>

        <li>Problem: Work on defining problem itself and motivation for the analysis: 2.0


            <ul>
                <li>We held couple of meetings to discuss our target and topics</li></ul>
        </li>

        <li>Algorithmic work: Work on the algorithms needed to work with the data, including integrating data mining and machine learning techniques: 2.5


            <ul>
                <li>We mainly used agg functions to calculate our results. We used Spark ML toolkits to predict future viewers</li></ul>
        </li>

        <li>Bigness/parallelization: Efficiency of the analysis on a cluster, and scalability to larger data sets: 2.0


            <ul>
                <li>We conducted analysis work on 50 gigabytes&#39; data. We used repartition, cache and broadcast join to ensure the efficiency of computation</li></ul>
        </li>

        <li>UI: User interface to the results, possibly including web or data exploration frontends: 3.5


            <ul>
                <li>We used react.js to develop our front-end and spent a decent amount of time implementing it. Check readme for more detailed tech stack about our frontend.</li></ul>
        </li>

        <li>Visualization: Visualization of analysis results: 3.5


            <ul>
                <li>Though one of our teammate has some prior experience in front-end development, none of us has experience visualizing data analysis before. We also spent time reformatting our json output in order to fit those framework.</li></ul>
        </li>

        <li>Technologies: New technologies learned as part of doing the project: 0.5


            <ul>
                <li>We use open-sourced frameworks like Charts.js and ReChart.js</li></ul>
        </li>
    </ul>

                    </div></div></div>
        </main>
    )
}

export default Reports
