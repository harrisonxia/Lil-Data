// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import randomColor from 'randomcolor'
import {
    languageNumberOfChannels,
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
                        <div className={styles.notes}>
                            <span>Check how we implemented this on &nbsp;
                                <a target='_blank'
                                   href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/popular_language.py'>
                                    Github &nbsp;
                                    <img src='../assets/img/github.png' alt='github' width='15' height='15'/>
                                </a>
                            </span>
                        </div>
                    </div>



                </div>
            </div>

        </main>
    )
}

export default Language
