// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {Doughnut} from 'react-chartjs-2'
import randomColor from 'randomcolor'
import {topCategoryByStreamData} from '../data/data.js'
import {Table} from 'reactstrap'
import {Cell, RadialBar, RadialBarChart, Tooltip} from 'recharts'


const TopCategoryByStream = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label = [], data = []
    let bgColor = [], hoverBgColor = []
    let tr = []
    let cnt = 0
    for (let col of topCategoryByStreamData) {
        label.push(col.genre)
        data.push(col.total_counts)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
        cnt++
        tr.push(
            <tr>
                <td>{cnt}</td>
                <td>{col.genre}</td>
                <td>{col.total_counts}</td>
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
                <div className={styles.title}>Top 20 game categories by total stream counts</div>
                <div className={styles.notes}>
                   Twitch data from Nov 13, 2018 and Nov 26, 2018.
                    <br/>
                    <span>Check how we implemented this on &nbsp;
                        <a target='_blank'
                           href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/popular_categories_time_frames.py'>
                                    Github &nbsp;
                            <img src='https://www.devxia.com/Lil-Data/assets/img/github.png' alt='github' width='15' height='15'/>
                                </a>
                            </span>
                </div>
                <div className={styles.tableAndBar}>
                    <div className={styles.tableRight}>
                        <Table borderless className={styles.gameName}>
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Genre</th>
                                <th>Count</th>
                            </tr>
                            </thead>
                            <tbody>
                            {tr}
                            </tbody>
                        </Table>
                    </div>
                    <div className={styles.barLeft}>
                        <div>
                            <Doughnut data={dataCollection} height={300} width={300}/>
                        </div>
                        <div className={styles.notes}>
                            The pie chart on the top and the radial bar chart on the bottom shared the same color schemes.<br/>
                            Each colored area represents the corresponding categories' relative popularity.
                        </div>
                        <RadialBarChart width={600} height={600} innerRadius="1%" outerRadius="100%"
                                        data={topCategoryByStreamData} startAngle={180} endAngle={0}>
                            <RadialBar minAngle={100} background clockWise={true} dataKey='total_counts'>
                                {
                                    data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={bgColor[index]}/>
                                    ))
                                }
                            </RadialBar>
                            <Tooltip label='genre'/>
                        </RadialBarChart>
                    </div>


                </div>
            </div>

        </main>
    )
}

export default TopCategoryByStream
