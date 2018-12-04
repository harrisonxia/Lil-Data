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
];
const COLORS = ['#8889DD', '#9597E4', '#8DC77B', '#A5D297', '#E2CF45', '#F8C12D']

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>

            <div className={styles.charts}>
                {/* <h2>This is a <s>doughnut</s> donut chart</h2> */}
            </div>
            <div className={styles.mainContainer}>
                <Treemap
                    width={730}
                    height={250}
                    data={dataTreeMap}
                    dataKey="size"
                    ratio={4 / 3}
                    stroke="#fff"
                    fill="#8884d8"
                />
                <hr/>
                <LineChart width={600} height={300} data={dataLineChart}
                           margin={{top: 5, right: 30, left: 20, bottom: 5}}>
                    <XAxis dataKey="name"/>
                    <YAxis/>
                    <CartesianGrid strokeDasharray="3 3"/>
                    <Tooltip/>
                    <Legend />
                    <Line type="monotone" dataKey="game1" stroke="#8884d8" activeDot={{r: 8}}/>
                    <Line type="monotone" dataKey="game2" stroke="#82ca9d" />
                    <Line type="monotone" dataKey="game3" stroke="#83dd9d" />
                </LineChart>

                <hr/>
                <RadarChart cx={300} cy={250} outerRadius={150} width={600} height={500} data={dataRadarChart}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="subject" />
                    <PolarRadiusAxis/>
                    <Radar name="Mike" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6}/>
                </RadarChart>
            </div>
        </main>
    )
}

export default Main
