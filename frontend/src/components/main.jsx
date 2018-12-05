// @flow
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

const dataTreeMap = [
    {
        name: 'CategoryA',
        children: [
            { name: 'AA', size: 1302 },
            { name: 'AB', size: 555 },
        ],
    },
    {
        name: 'CategoryB',
        children: [
            { name: 'BA', size: 2138 },
            { name: 'BB', size: 333 },
            { name: 'BC', size: 666 },
        ],
    },
]

const dataLineChart = [
    {name: '8:30', game1: 4000, game2: 2400, game3: 2400},
    {name: '9:00', game1: 3000, game2: 1398, game3: 2210},
    {name: '9:30', game1: 2000, game2: 9800, game3: 2290},
    {name: '10:00', game1: 2780, game2: 3908, game3: 2000},
]

const dataRadarChart = [
    { subject: 'CategoryA', A: 120, B: 110, fullMark: 150 },
    { subject: 'CategoryB', A: 98, B: 130, fullMark: 150 },
    { subject: 'CategoryC', A: 86, B: 130, fullMark: 150 },
    { subject: 'CategoryD', A: 99, B: 100, fullMark: 150 },
    { subject: 'CategoryE', A: 85, B: 90, fullMark: 150 },
]

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>
            <HeadBar name={name} text={text}/>
            <div className={styles.sidenav}>
                <a href="#">About</a>
                <a href="#">Services</a>
                <a href="#">Clients</a>
                <a href="#">Contact</a>
            </div>
            <div className={styles.mainContainer}>
                <div className={styles.title}>Lil data</div>

                <div>
                    <span className={styles.pageHeader}>Hello World</span>
                    <br/>
                    <span className={styles.pageDescription}>
                        My Code
                        <br/>
                        <span className={styles.stupidFont}>actually works.</span>
                    </span>
                    <PieCharts/>
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

            </div>


        </main>
    )
}

export default Main
