// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import { Bar, Doughnut } from 'react-chartjs-2'
import randomColor from 'randomcolor'
import { topCategoryByViewerData } from '../data/data.js'
import {Table} from 'reactstrap'

const TopCategoryByViewer = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'


    let label=[], data = []
    let bgColor = [], hoverBgColor = []
    let tr = []
    let cnt = 0

    for (let col of topCategoryByViewerData) {
        label.push(col.genre)
        data.push(col.total_viewers)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
        cnt++
        tr.push(
            <tr>
                <td>{cnt}</td>
                <td>{col.genre}</td>
                <td>{col.total_viewers}</td>
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
                <div className={styles.title}>Top 20 game categories by view counts</div>
                <div className={styles.notes}>
                    <span>Check how we implemented this on &nbsp;
                        <a target='_blank'
                           href='https://github.com/harrisonxia/Lil-Data/blob/master/Analysis/popular_categories_time_frames.py'>
                                    Github &nbsp;
                            <img src='../assets/img/github.png' alt='github' width='15' height='15'/>
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
                                <th>Viewers</th>
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
                    </div>
                </div>
            </div>

        </main>
    )
}

export default TopCategoryByViewer
