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
    Cell, RadialBar, RadialBarChart,
} from 'recharts'

import randomColor from 'randomcolor'
import {prediction, predictedGenre} from '../data/data.js'
import {Table} from 'reactstrap'


let label = [], data = [], labelGenre = [], dataGenre = []
let bgColor = [], bgColorGenre = []

for (let col of prediction) {
    label.push(col.game)
    data.push(col.prediction)
    labelGenre.push(col.game)
    dataGenre.push(col.prediction)
    bgColor.push(randomColor())
    bgColorGenre.push(randomColor())
}

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    let tr = [], trGenre = []
    for (let a in prediction) {
        tr.push(
            <tr>
                <td>{parseInt(a) + 1}</td>
                <td>{prediction[a].game}</td>
                <td>{prediction[a].prediction.toFixed(2)}</td>
            </tr>)
        trGenre.push(
            <tr>
                <td>{parseInt(a) + 1}</td>
                <td>{predictedGenre[a].genres}</td>
                <td>{predictedGenre[a].prediction.toFixed(1)}</td>
            </tr>)
    }
    return (
        <div className={styles.main}>
            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>
                <div className={styles.title}>This is our prediction of top 20 games on 2019-01-01</div>
                <div className={styles.notes}>
                    How ...
                </div>
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
                                    <th>Prediction</th>
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
                                        const color = bgColor[index]
                                        return <Cell fill={color}/>
                                    })
                                }</Bar>
                            </BarChart>
                        </div>
                    </div>
                </div>
                <div className={styles.title}>This is our prediction of top 20 game genre on 2019-01-01</div>
                <div className={styles.notes}>
                    How ...
                </div>
                <div>
                    <div className={styles.tableAndBar}>
                        <div className={styles.tableRight}>
                            <Table borderless className={styles.gameName}>
                                <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Genre</th>
                                    <th>Prediction</th>
                                </tr>
                                </thead>
                                <tbody>
                                {trGenre}
                                </tbody>
                            </Table>
                        </div>
                        <div className={styles.barLeft}>
                            <div>
                                <BarChart width={730} height={730} data={predictedGenre}>
                                    <CartesianGrid strokeDasharray="3 3"/>
                                    <XAxis dataKey="game"/>
                                    <YAxis/>
                                    <Tooltip/>
                                    <Legend/>
                                    <Bar dataKey="prediction" fill="#8884d8"> {
                                        data.map((entry, index) => {
                                            const color = bgColorGenre[index]
                                            return <Cell fill={color}/>
                                        })
                                    }</Bar>
                                </BarChart>
                            </div>
                            <div className={styles.notes}>
                                The bar chart on the top and the radial bar chart on the bottom shared the same color schemes.<br/>
                                Each colored area represents the predicted corresponding categories' relative popularity on 2019-01-01.
                            </div>
                            <div>
                                <RadialBarChart width={800} height={600} innerRadius="1%" outerRadius="100%"
                                                data={predictedGenre} startAngle={180} endAngle={0}>
                                    <RadialBar minAngle={100} background clockWise={true} dataKey='prediction'>
                                        {
                                            data.map((entry, index) => (
                                                <Cell key={`cell-${index}`} fill={bgColorGenre[index]}/>
                                            ))
                                        }
                                    </RadialBar>
                                    <Tooltip label='name'/>
                                </RadialBarChart>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Main
