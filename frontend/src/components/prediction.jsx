import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    BarChart,
    Bar,
    Cell,
} from 'recharts'

import randomColor from 'randomcolor'
import {prediction} from '../data/data.js'
import {Table} from 'reactstrap'
import comStyle from './component.css'
let label = [], data = []
let bgColor = [], hoverBgColor = []

for (let col of prediction) {
    label.push(col.game)
    data.push(col.prediction)
    bgColor.push(randomColor())
    hoverBgColor.push(randomColor())
}

const dataCollection = {
    labels: label,
    datasets: [{
        label: 'Prediction: Top games on 2019-1-1',
        data: data,
        borderWidth: 1,
        backgroundColor: bgColor,
        hoverBackgroundColor: hoverBgColor,
    }],
}

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    let tr = []
    for (let a in prediction) {
        tr.push(
            <tr>
                <td>{parseInt(a) + 1}</td>
                <td>{prediction[a].game}</td>
                <td>{prediction[a].prediction.toFixed(2)}</td>
            </tr>)
    }
    return (
        <div className={styles.main}>
            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>
                <div className={styles.title}>This is our list of Top 20 Games in 2018 according streams on Twitch</div>
                <div>
                    <span className={styles.pageHeader}></span>

                    <br/>
                    <span className={styles.pageDescription}>
                        <br/>
                    </span>
                    <div className={styles.tableAndBar}>
                        <div className={styles.tableRight}>
                            <Table borderless className={styles.gameName}>
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Game</th>
                                    <th className={styles.wholeNum}>Prediction</th>
                                </tr>
                                </thead>
                                <tbody>
                                    {tr}
                                </tbody>
                            </Table>
                        </div>
                        <div className={styles.barLeft}>
                            <BarChart width={730} height={730} data={prediction}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="game"/>
                                <YAxis/>
                                <Tooltip/>
                                <Legend/>
                                <Bar dataKey="prediction" fill="#8884d8"> {
                                    data.map((entry, index) => {
                                        const color = entry.prediction > 1000 ? bgColor[index] : bgColor[index+1];
                                        return <Cell fill={color}/>;
                                    })
                                }</Bar>
                            </BarChart>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Main
