// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import randomColor from 'randomcolor'
import {
    languageNumberOfChannels,
    timeframePopularGenres,
} from '../data/data.js'
import {
    CartesianGrid,
    Legend,
    Line,
    LineChart,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts'
import {Table} from 'reactstrap'


const Language = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label = [], data = []
    let bgColor = [], hoverBgColor = []

    for (let col of languageNumberOfChannels) {
        label.push(col.language)
        data.push(col.numberOfChannels)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
    }
    let tr = []
    for (let a in timeframePopularGenres) {
        console.log(timeframePopularGenres[a])
        tr.push(<tr>
            <td>{timeframePopularGenres[a].time_frame}</td>
            <td>{timeframePopularGenres[a].genres}</td>
            <td>{timeframePopularGenres[a].viewers}</td>
        </tr>)
    }

    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>
            <div className={styles.mainContainer}>

                <div className={styles.charts}>

                    <div className={styles.title}>Popular language by number of channels</div>
                    <span className={styles.pageHeader}>
                            </span>
                    <br/>
                    <span className={styles.pageDescription}>
                            <br/>
                        </span>

                    <div>
                        <LineChart width={600} height={300} data={languageNumberOfChannels}
                                   margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                            <XAxis dataKey="language"/>
                            <YAxis/>
                            <CartesianGrid strokeDasharray="3 3"/>
                            <Tooltip/>
                            <Legend/>
                            <Line type="monotone" dataKey="numberOfChannels" stroke="#8884d8" activeDot={{r: 8}}/>
                        </LineChart>
                    </div>

                    <div>
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
                    </div>

                </div>
            </div>

        </main>
    )
}

export default Language
