// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import randomColor from 'randomcolor'
import {
    numOfStreamAlldays,
    numofviewer_alldays,
    numOfCountsEveryday,
    numOfViewsEveryday,
    totalviewersbyday,
} from '../data/data.js'
import {
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    Tooltip,
    XAxis,
    YAxis,
    AreaChart,
    Area, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, RadarChart,
    Bar, BarChart,
} from 'recharts'
import {Table} from 'reactstrap'
import {timeframePopularGenres, matureVsNot} from '../data/data'


const StreamByTimeFrame = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let bgColor = [], hoverBgColor = []

    for (let i = 0; i < 6; i++) {
        bgColor.push(randomColor({
            luminosity: 'random',
            hue: 'random',
        }))
        hoverBgColor.push(randomColor({
            luminosity: 'random',
            hue: 'random',
        }))
    }
    let tr = []
    for (let a in timeframePopularGenres) {
        tr.push(<tr>
            <td>{timeframePopularGenres[a].time_frame}</td>
            <td>{timeframePopularGenres[a].genres}</td>
            <td>{timeframePopularGenres[a].viewers}</td>
        </tr>)
    }
    let tr0 = []
    for (let a in matureVsNot) {
        tr0.push(<tr>
            <td>{matureVsNot[a].time_frame}</td>
            <td>{matureVsNot[a].mature_viewers}</td>
            <td>{matureVsNot[a].non_mature_viewers}</td>
        </tr>)
    }
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>
            <div className={styles.mainContainer}>

                <div className={styles.charts}>

                    <div className={styles.title}>Number of total streams vs views on Twitch throughout the whole day.
                    </div>
                    <div className={styles.mainPageContainer}>
                        <div className={styles.pageHeader}>
                            <div className={styles.notes}>
                                Early Morning: 3:01 - 7:00 &nbsp;&nbsp;&nbsp;Morning: 7:01 -
                                11:00 &nbsp;&nbsp;&nbsp; Noon: 11:01 - 15:00 <br/>
                                Afternoon: 15:01 - 19:00 &nbsp;&nbsp;&nbsp; Evening: 19:01 -
                                23:00 &nbsp;&nbsp;&nbsp;Late Night: 23:01 - 3:00<br/>
                            </div>
                        </div>
                        <br/>
                        <span className={styles.pageDescription}>
                            <br/>
                            all time in PST
                        </span>

                        <div>
                            <LineChart width={600} height={300} data={numOfStreamAlldays}
                                       margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                                <XAxis dataKey="time_frame"/>
                                <YAxis yAxisId="left"/>
                                <YAxis yAxisId="right" orientation="right"/>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <Tooltip/>
                                <Legend/>
                                <Line yAxisId="left" type="monotone" dataKey="number of streams" stroke="#8884d8"
                                      activeDot={{r: 8}}/>
                                <Line yAxisId="right" type="monotone" dataKey="number of viewers" stroke="#82ca9d"
                                      activeDot={{r: 8}}/>
                            </LineChart>
                        </div>
                        <div className={styles.notes}>
                            An interesting observation is that the total number of streams and audiences drops a little
                            in late-night <br/>
                            since only the true-hard-core streamers and viewers will stay up super late for the games
                            they love
                        </div>
                        <hr className={styles.smallDivider}/>
                        <div className={styles.chartWidth}>
                            <div className={styles.title}>
                                Number of total streams on Twitch throughout the whole day.
                            </div>
                            <AreaChart width={660} height={400} data={numOfCountsEveryday}
                                       margin={{top: 10, right: 30, left: 0, bottom: 0}}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="Day"/>
                                <YAxis/>
                                <Tooltip/>
                                <Legend/>
                                <Area type='monotone' dataKey='Noon' stackId="1" stroke={bgColor[0]} fill={bgColor[0]}/>
                                <Area type='monotone' dataKey='Evening' stackId="1" stroke={bgColor[1]}
                                      fill={bgColor[1]}/>
                                <Area type='monotone' dataKey='Late Night' stackId="1" stroke={bgColor[2]}
                                      fill={bgColor[2]}/>
                                <Area type='monotone' dataKey='Morning' stackId="1" stroke={bgColor[3]}
                                      fill={bgColor[3]}/>
                                <Area type='monotone' dataKey='Afternoon' stackId="1" stroke={bgColor[4]}
                                      fill={bgColor[4]}/>
                                <Area type='monotone' dataKey='Early Morning' stackId="1" stroke={bgColor[5]}
                                      fill={bgColor[5]}/>
                            </AreaChart>
                        </div>
                        <hr className={styles.smallDivider}/>
                        <div className={styles.chartWidth}>
                            <div className={styles.title}>
                                Number of total views on Twitch throughout the whole day.
                            </div>
                            <AreaChart width={660} height={400} data={numOfViewsEveryday}
                                       margin={{top: 10, right: 30, left: 0, bottom: 0}}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="Day"/>
                                <YAxis/>
                                <Tooltip/>
                                <Legend/>
                                <Area type='monotone' dataKey='Noon' stackId="1" stroke={bgColor[0]} fill={bgColor[0]}/>
                                <Area type='monotone' dataKey='Evening' stackId="1" stroke={bgColor[1]}
                                      fill={bgColor[1]}/>
                                <Area type='monotone' dataKey='Late Night' stackId="1" stroke={bgColor[2]}
                                      fill={bgColor[2]}/>
                                <Area type='monotone' dataKey='Morning' stackId="1" stroke={bgColor[3]}
                                      fill={bgColor[3]}/>
                                <Area type='monotone' dataKey='Afternoon' stackId="1" stroke={bgColor[4]}
                                      fill={bgColor[4]}/>
                                <Area type='monotone' dataKey='Early Morning' stackId="1" stroke={bgColor[5]}
                                      fill={bgColor[5]}/>
                            </AreaChart>

                        </div>

                        <hr className={styles.smallDivider}/>
                        <div className={styles.chartWidth}>
                            <div className={styles.title}>Total Viewers By Day Of Week</div>
                            <RadarChart cx={300} cy={250} outerRadius={150} width={600} height={500}
                                        data={totalviewersbyday}>
                                <PolarGrid/>
                                <PolarAngleAxis dataKey="dow_string"/>
                                <PolarRadiusAxis/>
                                <Radar name="Day" dataKey="total_viewers" stroke="#8884d8" fill="#8884d8"
                                       fillOpacity={0.6}/>
                            </RadarChart>
                            <div className={styles.notes}>
                                The diagram above shows the distribution of total viewers count through each days of the
                                week. <br/>
                                Tuesday seems to be the ramadan day for most of the gamers and streamers <br/>
                                <span>Check how we implemented this on &nbsp;
                                    <a target='_blank'
                                       href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/views_in_dow.py'>
                                    Github &nbsp;
                                        <img src='https://www.devxia.com/Lil-Data/assets/img/github.png' alt='github' width='15' height='15'/>
                                </a>
                            </span>
                            </div>
                        </div>

                        <br/>
                        <hr/>
                        <br/>
                        <br/>
                        <div>
                            <div className={styles.title}>Favorite genre of each time frame</div>
                            <Table>
                                <thead>
                                <tr>
                                    <th>Time frame</th>
                                    <th>Genres</th>
                                    <th>Viewers</th>
                                </tr>
                                </thead>
                                <tbody>
                                {tr}
                                </tbody>
                            </Table>
                            <div className={styles.notes}>
                                <span>Check how we implemented this on &nbsp;
                                    <a target='_blank'
                                       href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/popular_categories_time_frames.py'>
                                    Github &nbsp;
                                        <img src='https://www.devxia.com/Lil-Data/assets/img/github.png' alt='github' width='15' height='15'/>
                                </a>
                            </span>
                            </div>
                        </div>
                        <hr className={styles.smallDivider}/>
                        <div className={styles.chartWidth}>

                            <div>
                                <div className={styles.title}>Total Viewers By Day Of Week</div>
                                <BarChart width={730} height={250} data={matureVsNot}>
                                    <CartesianGrid strokeDasharray="3 3"/>
                                    <XAxis dataKey="time_frame"/>
                                    <Tooltip/>
                                    <Legend/>
                                    <Bar dataKey="mature_viewers" fill="#8884d8"/>
                                    <Bar dataKey="non_mature_viewers" fill="#82ca9d"/>
                                </BarChart>
                            </div>
                            <div>
                                <div className={styles.title}>Favorite genre of each time frame</div>
                                <Table>
                                    <thead>
                                    <tr>
                                        <th>Time frame</th>
                                        <th>Mature Content Viewers</th>
                                        <th>Non Mature Content Viewers</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {tr0}
                                    </tbody>
                                </Table>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </main>
    )
}

export default StreamByTimeFrame
