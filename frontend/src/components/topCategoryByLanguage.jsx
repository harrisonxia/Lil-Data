// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {
    BarChart,
    CartesianGrid,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    // Doughnut,
    RadialBarChart,
    RadialBar,
    Cell,
} from 'recharts'
import randomColor from 'randomcolor'
import {popularCategoryForLanguage} from '../data/data.js'
import {Table} from 'reactstrap'
import { Bar } from 'react-chartjs-2'

const TopCategoryByLang = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label = [], data = []
    let bgColor = [], hoverBgColor = []
    let tr = []
    let cnt = 0
    for (let col of popularCategoryForLanguage) {
        label.push(col.language)
        data.push(col.viewers)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
        cnt++
        tr.push(
            <tr>
                <td>{col.language}</td>
                <td>{col.genres}</td>
                <td>{col.viewers}</td>
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
                <div className={styles.title}>The most popular category for each language</div>
                <div className={styles.notes}>Viewers counts represent the highest viewers for such category from Nov 13, 2018 to Nov 26, 2018.
                </div>
                <div className={styles.tableAndBar}>
                    <div className={styles.tableRight}>
                        <Table borderless className={styles.gameName}>
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Genre</th>
                                <th className={styles.wholeNum}>Viewers</th>
                            </tr>
                            </thead>
                            <tbody>
                            {tr}
                            </tbody>
                        </Table>
                    </div>
                    <div className={styles.barLeft}>
                        <div>
                            <Bar
                                data={dataCollection}
                                width={650}
                                height={650}
                                label
                                name='checkname'
                            />
                        </div>
                    </div>
                </div>
            </div>

        </main>
    )
}

export default TopCategoryByLang
