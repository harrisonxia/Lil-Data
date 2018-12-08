import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
import {
    Treemap,
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
import {top20, comparison_games_viewers_1518, viewersCount2018} from '../data/data.js'
import {Table, Alert} from 'reactstrap'

let label = [], data = []
let bgColor = [], hoverBgColor = []

for (let col of top20) {
    label.push(col.gen_name)
    data.push(col.count)
    bgColor.push(randomColor())
    hoverBgColor.push(randomColor())
}
const dataTreeMap = [
    {
        name: 'shooter',
        children: [
            {name: 'fortnite', size: 1815135},
            {name: 'fallout 76', size: 119765},
        ],
    },
    {
        name: 'First-Person Shooter',
        children: [
            {name: 'call of duty®: black ops 4', size: 395587},
            {name: 'overwatch', size: 169708},
            {name: 'counter-strike: global offensive', size: 165703},
            {name: 'playerunknown\'s battlegrounds', size: 142754},
            {name: 'counter-strike: global offensive', size: 165703},
            {name: 'tom clancy\'s rainbow six: siege', size: 111322},
            {name: 'battlefield v', size: 69131},
            {name: 'destiny 2', size: 91309},
        ],
    },
    {
        name: 'MOBA',
        children: [
            {name: 'league of legends', size: 301377},
        ],
    },
    {
        name: 'MMORPG',
        children: [
            {name: 'world of warcraft', size: 99460},
        ],
    },
    {
        name: 'Action',
        children: [
            {name: 'red dead redemption 2', size: 95648},
            {name: 'dead by daylight', size: 66880},
        ],
    },
    {
        name: 'Soccer',
        children: [
            {name: 'fifa 19', size: 72584},
            {name: 'rocket league', size: 54776},
        ],
    },
    {
        name: 'Basketball',
        children: [
            {name: 'nba 2k19', size: 50554},
        ],
    },
    {
        name: 'Action-Adventure',
        children: [
            {name: 'grand theft auto v', size: 54136},
            {name: 'minecraft', size: 48564},
        ],
    },
]

const COLORS = ['#8889DD', '#e43b45', '#8DC77B', '#A5D297', '#E2CF45', '#F8C12D', '#38CD2D', '#13332E']

class CustomizedContent extends React.Component {
    render() {
        const {root, depth, x, y, width, height, index, colors, name} = this.props

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
            ratio={4 / 3}
            stroke="#fff"
            fill="#8884d8"
            content={<CustomizedContent colors={COLORS}/>}
        />
    }
}

class Alert404 extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            visible: true
        };

        this.onDismiss = this.onDismiss.bind(this);
    }

    onDismiss() {
        this.setState({ visible: false });
    }

    render() {
        return (
            <Alert className={styles.alert404}color="info" isOpen={this.state.visible} toggle={this.onDismiss} fade={false}>
                Due to limitation on our hosting site, please <b>don't refresh</b>. If you encounter a 404, just go back to <a href="https://www.devxia.com/Lil-Data" className="alert-link">the front page using direct URL.</a>
            </Alert>
        );
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
                    <td>{viewersCount2018[dat].total_viewers}</td>
                </tr>)
        } else {
            tr0.push(
                <tr>
                    <td>{parseInt(dat) + 1}</td>
                    <td>{comparison_games_viewers_1518[dat].game}</td>
                    <td>{comparison_games_viewers_1518[dat].data_2015}</td>
                    <td>{viewersCount2018[dat].total_viewers}</td>
                </tr>)
        }
    }
    for (let a in top20) {
        tr.push(
            <tr>
                <td>{parseInt(a) + 1}</td>
                <td>{top20[a].gen_name}</td>
                <td>{top20[a].count}</td>
                <td>{top20[a].genre}</td>
            </tr>)
    }
    return (
        <main className={styles.main}>
            <Alert404/>
            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>
                <div className={styles.title}>Top 20 Games in 2018</div>
                <div>
                    <div className={styles.mainPageContainer}>
                        <span className={styles.pageHeader}></span>
                        <div className={styles.notes}>
                            We collected every singles streaming data on Twitch from Nov 13, 2018 and Nov 26, 2018 and received about 50GB of raw data.
                        </div>
                        <br/>
                        <span className={styles.pageDescription}>
                            <br/>
                        </span>
                        <SimpleTreemap className={styles.treemap}/>
                        <div className={styles.notes}>Top 20 games showed in their categories visualized in the TreeMap above, see the table below for detailed statistics.</div>
                        <div className={styles.tableAndBar}>
                            <div className={styles.tableRight}>
                                <Table borderless responsive className={styles.gameName}>
                                    <thead>
                                    <tr>
                                        <th>#</th>
                                        <th>Game</th>
                                        <th>Stream Count</th>
                                        <th>Genre</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    {tr}
                                    </tbody>
                                </Table>
                            </div>
                            <div className={styles.barLeft}>
                                <BarChart width={730} height={730} data={top20}>
                                    <CartesianGrid strokeDasharray="3 3"/>
                                    <XAxis dataKey="gen_name"/>
                                    <YAxis domain={['dataMin', 'dataMax']}/>
                                    <Tooltip/>
                                    <Legend/>
                                    <Bar dataKey="count" fill="#8884d8"> {
                                        data.map((entry, index) => {
                                            const color = bgColor[index]
                                            return <Cell fill={color}/>
                                        })
                                    }</Bar>
                                </BarChart>
                                <div className={styles.notes}>Top 20 games according to total number of <b>streams</b> from Nov 13, 2018 and Nov 26, 2018 </div>
                            </div>
                        </div>

                        <div>
                            <div className={styles.title}><b>2018</b> Top 20 games according total number of <b>views</b> <br/>and their performance in <b>2015</b>.
                            </div>

                            <Table borderless responsive className={styles.gameName2015}>
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
            </div>
        </main>
    )
}

export default Main
