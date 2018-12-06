import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {
    Treemap,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    Radar,
    RadarChart,
    PolarGrid,
    PolarAngleAxis,
    PolarRadiusAxis,
} from 'recharts'
import PieCharts from './pieChart.jsx'
import {Bar} from 'react-chartjs-2'
import randomColor from 'randomcolor'
import {top20, comparison_games_viewers_1518} from '../data/data.js'
import {Table} from 'reactstrap'

let label = [], data = []
let bgColor = [], hoverBgColor = []

for (let col of top20) {
    label.push(col.gen_name)
    data.push(col.count)
    bgColor.push(randomColor())
    hoverBgColor.push(randomColor())
}

const dataCollection = {
    labels: label,
    datasets: [{
        label: 'Top 20 Games By Lil Data',
        data: data,
        borderWidth: 1,
        backgroundColor: bgColor,
        hoverBackgroundColor: hoverBgColor,
    }],
}
// const data = {
//     labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
//     datasets: [
//         {
//             label: 'My First dataset',
//             backgroundColor: 'rgba(255,99,132,0.2)',
//             borderColor: 'rgba(255,99,132,1)',
//             borderWidth: 1,
//             hoverBackgroundColor: 'rgba(255,99,132,0.4)',
//             hoverBorderColor: 'rgba(255,99,132,1)',
//             data: [65, 59, 80, 81, 56, 55, 40]
//         }
//     ]
// };

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    let tr = [], tr0 = []
    for (let dat in comparison_games_viewers_1518) {
        console.log(comparison_games_viewers_1518)
        console.log(comparison_games_viewers_1518[dat].data_2015)
        if (comparison_games_viewers_1518[dat].data_2015 === undefined) {
            tr0.push(
                <tr>
                    <td>{parseInt(dat) + 1}</td>
                    <td>{comparison_games_viewers_1518[dat].game}</td>
                    <td>N/A</td>
                    <td>{comparison_games_viewers_1518[dat].data_2018}</td>
                </tr>)
        } else {
            tr0.push(
                <tr>
                    <td>{parseInt(dat) + 1}</td>
                    <td>{comparison_games_viewers_1518[dat].game}</td>
                    <td>{comparison_games_viewers_1518[dat].data_2015}</td>
                    <td>{comparison_games_viewers_1518[dat].data_2018}</td>
                </tr>)
        }
    }
    for (let a in top20) {

        tr.push(
            <tr>
                <td>{parseInt(a) + 1}</td>
                <td>{top20[a].gen_name}</td>
                <td>{top20[a].count}</td>
            </tr>)
    }
    return (
        <main className={styles.main}>
            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>
                <div className={styles.title}>This is our list of Top 20 Games in 2018 according streams on Twitch</div>
                <div>
                    <span className={styles.pageHeader}></span>
                    We collected data from Nov 13, 2018 to Nov 26, 2018.
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
                                    <th>Stream Count</th>
                                </tr>
                                </thead>
                                <tbody>
                                {tr}
                                </tbody>
                            </Table>
                        </div>
                        <div className={styles.barLeft}>
                            <Bar
                                data={dataCollection}
                                width={650}
                                height={650}
                                options={{
                                    maintainAspectRatio: false,
                                }}
                            />
                        </div>
                    </div>

                    <div>
                        <div className={styles.title}>Top 20 Games in 2015 according number of viewers on Twitch</div>

                        <Table borderless className={styles.gameName}>
                            <thead>
                            <tr>
                                <th>#</th>
                                <th>Game</th>
                                <th>2015 Data</th>
                                <th>2018 Data</th>
                            </tr>
                            </thead>
                            <tbody>
                            {tr0}
                            </tbody>
                        </Table>
                    </div>
                </div>
            </div>

            {/*<Treemap*/}
            {/*width={730}*/}
            {/*height={250}*/}
            {/*data={dataTreeMap}*/}
            {/*dataKey="size"*/}
            {/*ratio={4 / 3}*/}
            {/*stroke="#fff"*/}
            {/*fill="#8884d8"*/}
            {/*/>*/}
            {/*<hr/>*/}
            {/*<LineChart width={600} height={300} data={dataLineChart}*/}
            {/*margin={{top: 5, right: 30, left: 20, bottom: 5}}>*/}
            {/*<XAxis dataKey="name"/>*/}
            {/*<YAxis/>*/}
            {/*<CartesianGrid strokeDasharray="3 3"/>*/}
            {/*<Tooltip/>*/}
            {/*<Legend />*/}
            {/*<Line type="monotone" dataKey="game1" stroke="#8884d8" activeDot={{r: 8}}/>*/}
            {/*<Line type="monotone" dataKey="game2" stroke="#82ca9d" />*/}
            {/*<Line type="monotone" dataKey="game3" stroke="#83dd9d" />*/}
            {/*</LineChart>*/}

            {/*<hr/>*/}
            {/*<div>*/}
            {/*<a id='kkk'>Radar Chart</a>*/}
            {/*<RadarChart cx={300} cy={250} outerRadius={150} width={600} height={500} data={dataRadarChart}>*/}
            {/*<PolarGrid />*/}
            {/*<PolarAngleAxis dataKey="subject" />*/}
            {/*<PolarRadiusAxis/>*/}
            {/*<Radar name="Mike" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6}/>*/}
            {/*</RadarChart>*/}
            {/*</div>*/}
            {/*<hr/>*/}


        </main>
    )
}

export default Main
