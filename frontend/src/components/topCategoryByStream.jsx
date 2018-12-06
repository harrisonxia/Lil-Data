// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import { Doughnut } from 'react-chartjs-2'
import randomColor from 'randomcolor'
import { topCategoryByStreamData } from '../data/data.js'


const TopCategoryByStream = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'

    let label=[], data = []
    let bgColor = [], hoverBgColor = []

    for (let col of topCategoryByStreamData) {
        label.push(col.genre)
        data.push(col.total_counts)
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
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

                <div className={styles.charts}>
                    <div>
                        <Doughnut data={dataCollection} height={450} width={450}/>
                    </div>
                </div>
            </div>

        </main>
    )
}

export default TopCategoryByStream
