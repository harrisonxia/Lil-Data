// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {Bar, Doughnut} from 'react-chartjs-2'
import randomColor from 'randomcolor'
import { popularChannelByFollower } from '../data/data.js'
import {Table} from 'reactstrap'
import {Cell, RadialBar, RadialBarChart, Tooltip, Legend} from 'recharts'

const boolToStr = (bool: boolean) => {
    return bool ? 'Yes': 'No'
}
const PopularChannel = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label=[], data = []
    let bgColor = [], hoverBgColor = []
    let tr = []
    let cnt = 0
    for (let col of popularChannelByFollower) {
        label.push(col.name)
        data.push(col.total_followers)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
        cnt++

        tr.push(
            <tr>
                <td>{cnt}</td>
                <td>{col.name}</td>
                <td>{col.total_followers}</td>
                <td>{boolToStr(col.mature)}</td>
                <td>{boolToStr(col.partner)}</td>
            </tr>)
    }

    const dataCollection = {
        labels: label,
        datasets: [{
            data: data,
            backgroundColor: bgColor,
            hoverBackgroundColor: hoverBgColor,
        }]
    }

    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>
            <div className={styles.mainContainer}>
                <div className={styles.title}>Top 10 Twitch Channel by followers</div>

                <div className={styles.tableAndBar}>
                    <div className={styles.tableRight}>
                        <Table borderless className={styles.gameName}>
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Follower</th>
                                <th>Mature?</th>
                                <th>Partner?</th>
                            </tr>
                            </thead>
                            <tbody>
                                {tr}
                            </tbody>
                        </Table>
                    </div>
                    <div className={styles.barLeft}>
                        <div>
                            <Doughnut data={dataCollection} height={350} width={350}/>
                        </div>
                        <RadialBarChart width={400} height={400} innerRadius="1%" outerRadius="100%" data={popularChannelByFollower} startAngle={180} endAngle={0}>
                            <RadialBar minAngle={100} background clockWise={true} dataKey='total_followers'>
                                {
                                    data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={bgColor[index]}/>
                                    ))
                                }
                            </RadialBar>
                            {/*<Legend label='genre' iconSize={10} width={120} height={140} layout='vertical' verticalAlign='middle' align="right" />*/}
                            <Tooltip label='name'/>
                        </RadialBarChart>
                    </div>


                </div>
            </div>

        </main>
    )
}

export default PopularChannel
