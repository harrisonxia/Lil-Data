// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {Doughnut} from 'react-chartjs-2'
import randomColor from 'randomcolor'
import {popularChannelByFollower} from '../data/data.js'
import {Table} from 'reactstrap'
import {Cell, RadialBar, RadialBarChart, Tooltip} from 'recharts'

const boolToStr = (bool: boolean) => {
    return bool ? 'Yes' : 'No'
}
const PopularChannel = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis'

    let label = [], data = []
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
        }],
    }

    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>
            <div className={styles.mainContainer}>
                <div className={styles.title}>Top 10 Twitch Channel by followers</div>

                <div className={styles.tableAndBar}>
                    <div>
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
                        <div className={styles.notes}>
                                <span>Check how we implemented this on &nbsp;
                                    <a target='_blank'
                                       href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/analysis_twitch2018/popular_channel.py'>
                                    Github &nbsp;
                                        <img src='https://www.devxia.com/Lil-Data/assets/img/github.png' alt='github' width='15' height='15'/>
                                </a>
                            </span>
                        </div>
                    </div>
                    <div className={styles.barLeft}>
                        <div>
                            <Doughnut data={dataCollection} height={350} width={350}/>
                        </div>
                        <RadialBarChart width={400} height={400} innerRadius="1%" outerRadius="100%"
                                        data={popularChannelByFollower} startAngle={180} endAngle={0}>
                            <RadialBar minAngle={100} background clockWise={true} dataKey='total_followers'>
                                {
                                    data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={bgColor[index]}/>
                                    ))
                                }
                            </RadialBar>
                            <Tooltip label='name'/>
                        </RadialBarChart>
                    </div>


                </div>
            </div>

        </main>
    )
}

export default PopularChannel
