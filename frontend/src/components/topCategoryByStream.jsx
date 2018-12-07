// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {Bar, Doughnut} from 'react-chartjs-2'
import randomColor from 'randomcolor'
import { topCategoryByStreamData } from '../data/data.js'
import {Table} from 'reactstrap'
import {Cell, RadialBar, RadialBarChart, Tooltip, Legend} from 'recharts'


const TopCategoryByStream = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label=[], data = []
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
        }]
    }

    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>
            <div className={styles.mainContainer}>
                <div className={styles.title}>Top 20 game categories by stream counts</div>

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
                            <Doughnut data={dataCollection} height={450} width={450}/>
                        </div>
                        <RadialBarChart width={600} height={600} innerRadius="10%" outerRadius="80%" data={topCategoryByStreamData} startAngle={180} endAngle={0}>
                            <RadialBar minAngle={100} background clockWise={true} dataKey='total_counts'>
                                {
                                    data.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={bgColor[index]}/>
                                    ))
                                }
                            </RadialBar>
                            {/*<Legend label='genre' iconSize={10} width={120} height={140} layout='vertical' verticalAlign='middle' align="right" />*/}
                            <Tooltip label='genre'/>
                        </RadialBarChart>
                    </div>


                </div>
            </div>

        </main>
    )
}

export default TopCategoryByStream
