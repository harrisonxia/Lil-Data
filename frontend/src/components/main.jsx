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
    PolarRadiusAxis, BarChart,
    Bar,
    Cell,
} from 'recharts'
// import {Bar} from 'react-chartjs-2'
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
const dataTreeMap = [
    {
        name: 'shooter',
        children: [
            { name: 'fortnite', size: 1815135 },
            { name: 'fallout 76', size: 119765 },
        ],
    },
    {
        name: 'First-Person Shooter',
        children: [
            { name: 'call of duty®: black ops 4', size: 395587 },
            { name: 'overwatch', size: 169708 },
            { name: 'counter-strike: global offensive', size: 165703 },
            { name: 'playerunknown\'s battlegrounds', size: 142754 },
            { name: 'counter-strike: global offensive', size: 165703 },
            { name: 'tom clancy\'s rainbow six: siege', size: 111322 },
            { name: 'battlefield v', size: 69131 },
            { name: 'destiny 2', size: 91309 },
        ],
    },
    {
        name: 'MOBA',
        children: [
            { name: 'league of legends', size: 301377 },
        ],
    },
    {
        name: 'MMORPG',
        children: [
            { name: 'world of warcraft', size: 99460 },
        ],
    },
    {
        name: 'Action',
        children: [
            { name: 'red dead redemption 2', size: 95648 },
            { name: 'dead by daylight', size: 66880 },
        ],
    },
    {
        name: 'Soccer',
        children: [
            { name: 'fifa 19', size: 72584 },
            { name: 'rocket league', size: 54776 },
        ],
    },
    {
        name: 'Basketball',
        children: [
            { name: 'nba 2k19', size: 50554 },
        ],
    },
    {
        name: 'Action-Adventure',
        children: [
            { name: 'grand theft auto v', size: 54136 },
            { name: 'minecraft', size: 48564 },
        ],
    },
];

const COLORS = ['#8889DD', '#e43b45', '#8DC77B', '#A5D297', '#E2CF45', '#F8C12D', '#38CD2D', '#13332E']
class CustomizedContent extends React.Component {
    render() {
        const { root, depth, x, y, width, height, index, payload, colors, rank, name } = this.props;

        return (
            <g>
                <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    style={{
                        fill: depth < 2 ? colors[Math.floor(index / root.children.length * 8)] : 'none',
                        stroke: '#fff',
                        strokeWidth: 2 / (depth + 1e-10),
                        strokeOpacity: 1 / (depth + 1e-10),
                    }}
                />
                {
                    depth === 1 ?
                        <text
                            x={x + width / 2}
                            y={y + height / 2 + 7}
                            textAnchor="middle"
                            fill="#fff"
                            fontSize={14}
                        >
                            {name}
                        </text>
                        : null
                }
                {
                    depth === 1 ?
                        <text
                            x={x + 4}
                            y={y + 18}
                            fill="#fff"
                            fontSize={16}
                            fillOpacity={0.9}
                        >
                            {index + 1}
                        </text>
                        : null
                }
            </g>
        )
    }
}
class SimpleTreemap extends React.Component {
    render() {
        return <Treemap
            width={900}
            height={500}
            data={dataTreeMap}
            dataKey="size"
            ratio={4/3}
            stroke="#fff"
            fill="#8884d8"
            content={<CustomizedContent colors={COLORS}/>}
        />
    }
}


const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    let tr = [], tr0 = []
    for (let dat in comparison_games_viewers_1518) {
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
                    <SimpleTreemap />
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
                            {/*<Bar*/}
                                {/*data={dataCollection}*/}
                                {/*width={650}*/}
                                {/*height={650}*/}
                                {/*options={{*/}
                                    {/*maintainAspectRatio: false,*/}
                                {/*}}*/}
                            {/*/>*/}

                            <BarChart width={730} height={730} data={top20}>
                                <CartesianGrid strokeDasharray="3 3"/>
                                <XAxis dataKey="gen_name"/>
                                <YAxis domain={['dataMin', 'dataMax']}/>
                                <Tooltip/>
                                {/*<Legend/>*/}
                                <Bar dataKey="count" fill="#8884d8"> {
                                    data.map((entry, index) => {
                                        const color = entry.pv > 4000 ? bgColor[index] : bgColor[index+1];
                                        return <Cell fill={color}/>;
                                    })
                                }</Bar>
                            </BarChart>
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
        </main>
    )
}

export default Main
