// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'
// import {
//     PieChart,
//     Pie,
// } from 'recharts'
import {Doughnut} from 'react-chartjs-2'
import randomColor from 'randomcolor'

const dataPieChart = [
    {"genre":"Shooter","total_counts":2249537},
    {"genre":"First-Person Shooter","total_counts":1033161},
    {"genre":"Action","total_counts":603394},
    {"genre":"MOBA","total_counts":439132},
    {"genre":"Action-Adventure","total_counts":427543},
    {"genre":"Role-Playing","total_counts":383732},
    {"genre":"MMORPG","total_counts":256919},
    {"genre":"Simulation","total_counts":217854},
    {"genre":"Driving/Racing","total_counts":163476},
    {"genre":"Soccer","total_counts":135251},
    {"genre":"Strategy","total_counts":121246},
    {"genre":"Platformer","total_counts":99666},
    {"genre":"Adventure","total_counts":98679},
    {"genre":"Vehicular Combat","total_counts":90747},
    {"genre":"Card Game","total_counts":81960},
    {"genre":"Fighting","total_counts":62098},
    {"genre":"Music/Rhythm","total_counts":57808},
    {"genre":"Basketball","total_counts":57372},
    {"genre":"Compilation","total_counts":50372},
    {"genre":"Football","total_counts":44449}
]

let label=[], data = [], bgColor = [], hoverBgColor = []
for (let col of dataPieChart) {
    label.push(col.genre)
    data.push(col.total_counts)
    bgColor.push(randomColor())
    hoverBgColor.push(randomColor())
}

console.log(label)
console.log(data)
console.log(randomColor())
const dataCollection = {
    labels: label,
    datasets: [{
        data: data,
        backgroundColor: bgColor,
        hoverBackgroundColor: hoverBgColor,
    }]
}

const PieCharts = () => {
    // <PieChart width={500} height={250}>
    //     <Pie data={dataPieChart} dataKey="total_counts"
    //          nameKey="genre" cx="85%" cy="85%" fill="#8884d8" label={true}
    //          legendType='square' isAnimationActive={true}}
    //     />
    // </PieChart>
    return (
        <div>

            <Doughnut data={dataCollection} height={450} width={450}/>

        </div>
    )
}

export default PieCharts
