// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'

const Reports = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>

                <div className={styles.reports}>
                    <div className={styles.title}>Lil’ Report</div>
                    <div className={styles.reportContainer}>
                        <p><b>Chuangxin Xia, cxa25; Chengxi Li, chengxil; Aisuluu Alymbekova, aalymbek; Risheng Wang, rishengw</b></p>
                    <p>1.</p>
                    <p>The data collected from twitch does not explicitly show how popular one game is, and how time of broadcasting is distributed throughout the day. Further, games that covers a great diversity of genres/categories are played by streamers across all platforms and hence there are no direct means to discover the popularity of a certain game category.</p>
                    <p> </p>
                    <p>Regarding popularity of any game, first we need to evaluate the data structure which twitch uses to store its stream information and then we also need to pick some perspectives that could convey a convincing meaning of 'popularity'. Selecting appropriate features to evaluate popularity is proven to be a challenging task, for example, views of a stream could be used as a standard to measure its popularity but some may argue that only the count of followers could show a game or a stream’s true potential to grow in popularity.</p>
                    <p> </p>
                    <p>Another challenge is to find the implicitly included information in the tremendously huge amount of data, which is of 50 gigabytes' large since the dataset does not contain detailed game information, for example game category is not included in the data we extracted from twitch. Therefore, other sources of data about all the video games played across different platforms are also needed in order to for us to get a better picture about popularities of various game categories.</p>
                    <p> </p>
                    <p>In addition, the limited number of features in this dataset has seriously constrained us from finding more interesting information about games played or streamers since most of the features are technical like ‘signal delayed time’, ‘average frame per second’, and ‘software used for streaming’ and very often the entries in these columns are either blank or have the same values across entire column.</p>
                    <p> </p>
                    <p>Regarding to the habitual pattern of online audiences and therefore streamers, what we have in mind is that we need to make careful definitions about "time frame". For example, it’s common for streamers and their audiences to stay up late, but is 11pm considered late or 3am? Also, how about the number of streams during the day and afternoon? We hope that by analysing the behaviors of streamer and their audiences so we could glance at perhaps the general lifestyles of streamers and their fans.  As mentioned in the previous paragraph, in order to convey a reasonable result, we certainly have to survey the cyclic pattern of streamer from appropriate perspectives such that the most popular time to watch a stream or the best time for a streamer to perform is clear and reasonable.</p>
                    <p> </p>
                    <p>Moreover, in order to exploit the dataset further, we want to find out more about streamers and maybe how they are divided. However, none of the personal information such as  geographical locations, gender, age, and occupation are provided for either streamer or their audiences due to twitch’s privacy policy. Therefore, trying to see some patterns regarding distributions of streamer/channel or their audiences is difficult. However, one of the features is called ‘broadcaster language’ and by no surprise that English is overwhelmingly dominating language spoken among all streamers since twitch is an American company operated mainly in North America. Nonetheless, despite the obvious facts about English speaking streamers, there are also surprisingly many other languages being spoken and by no means lack of either number of streamers nor followers. As a result, new opportunity is unveiled and more can be asked about languages spoken on twitch.</p>
                    <p> </p>
                    <p>Next, as we explore the datasets, we discovered that one of the major portion of the data is about channels/streamers. Although as indicated earlier, many features included for channels are technical and probably not quite related to our purpose of finding the most popular games played on twitch, however, the existing features do have some insights to offer us so that we could to unravel the popular channel/streamers and find out what game do they usually play and perhaps compare if registering as a partner of twitch (hence monetize streamers’ contents) has real impact on popularity of streamers/channels.</p>
                    <p> </p>
                    <p>On the other hand, the depth of some of the analysis is constraint due to the lack of meaningful features in the dataset and alternative credible source of data about twitch channels other than twitch.com is nowhere to be found. The workaround for this challenge is to evaluate the popularity of each streamer from different perspectives so that we do not only tell one side of the story.</p>
                    <p> </p>
                    <p>2. Methodology</p>
                    <p> </p>
                    <p>ETL</p>
                    <p>ETL work took a lot of efforts because the data we download using twitch api and giantbomb api was dirty. First made advantage of python regular expression operation package to clean the collected json files, such as removing the tail comma, so that they could be read by pyspark. Afterwards, mainly use pyspark to convert json strings into featurized dataframes.</p>
                    <p> </p>
                    <p>Dataframe is suitable with our project, because it provides well-structured table frame, to which data with multiple features well fits. Furthermore, Dataframe is managed by using sql like functions. It also provides users with API that enables hardcoded sql queries. This sql-user-friendly feature makes it easy to handle complex data.</p>
                    <p> </p>
                    <p>The original data was splitted into three tables: stream table, which contains information about the stream, including stream id, game, created time of the stream and or so; channel table, which was separated from stream data, that describes the channel owner who was broadcasting corresponding stream; game table, which was a joined table from stream data and game details from giantbomb. The reason to separate data in this way, is that it matches the three main topics we want to conduct on the data, namely stream, channel and game.</p>
                    <p> </p>


                    <p>EDA</p>
                    <p>The exploratory data analysis, as explained on wikipedia, is usually a method used to describe the hidden characteristics of the data helping the formulation of the hypothesis regarding various aspects of the data through mainly visualization methods (<u>https://en.wikipedia.org/wiki/Exploratory_data_analysis</u>).</p>

                    <p>First of all, we selected a group of results that are more appealing for visualization and teammate responsible building the website puts all of the selected results to our website and used (needs input from Harrison)</p>

                    <p>As mentioned earlier, we used different standards for measuring popularities of games, channel, language and so on. The reason behind this is that we were trying to get a sense of for example, popularity, from each possible point of view and hence getting a full depiction of the popularity on each subjects (eg.games, channels).  However, the results on certain topics from each perspective do not vary much and sometimes stays the same. For example, fortinet is the most popular game played on twitch by both view count and number of streamer played. As you can see from one of our graph used on the website, fortnite, red hot as it is, dwarfs all other games, classic or newly released. Therefore, we only selected a few results from data analysis to represent some of the topics for our website.</p>

                    <p>Among all of the analysis of twitch data, not all of the results are suitable for making simple and concise graphs either because it contains so few numbers or because it is a bit too complicated. </p>
                    <p>For example is the one of the results for analyzing the what channels are popular and what languages does each streamer speaks, the resulting table looks like:</p>
                    <p><img src="cid:Image_0.png" /></p>
                    <p>                 Figure 2. sample channel and language analysis result</p>





                    <p> </p>
                    <p>3. Problems</p>
                    <p>ETL:</p>
                    <ul class="small"><li>The original data was messed up. One significant problem was that twitch allows users to manually type in the game name they are broadcasting. This leads to severe problems such as typo, mixed lower and upper cases, or just random names. At very first we tried to use Levenshtein distance algorithm to deal with typo, but at last it was proved to be useless because the algorithm cannot tell whether the name had some typo or merely was another game. At the end, we have to roughly filter out ‘irregular’ names. That is, names of games which had few viewers. And we convert all names to lower cases in order to make a better join with data from giantbomb.</li>
                    <li>In order to analyze data on time frame scale, we need a new column representing what period of day the stream was being broadcast. So we discussed and decided to break a day into six different time pieces.</li>
                    <li>Original time data contains minitues, needed to be converted into simple yyyy-mm-dd format. </li></ul>

                <p>Data Analyze:</p>
                <ul class="small"><li>Cannot simply count the number of streams, because we collect data every 30 minutes, and the same stream could appear multiples times in our data. Before counting, have to select distinct stream id</li>
                <li>Cannot simply sum up the number of viewers for a game. The reason is similar to that of number of streams, while this time, number of viewers for one stream could vary. We choose to compute the max or average value for number of viewers for each stream at first, and sum them up to the total number of viewers for each game or category or time frame afterwards.</li>
                <li></li></ul>
                <img height='300px' width='500px' src='../assets/img/sc0.png' alt='Screenshots of sample channel and language analysis result '/>
        </div>
            </div>
            </div>

        </main>
    )
}

export default Reports
