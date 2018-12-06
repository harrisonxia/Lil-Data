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

const PieCharts = (label: any, data: any) => {

    let bgColor = [], hoverBgColor = []
    for (let col of label) {
        bgColor.push(randomColor())
        hoverBgColor.push(randomColor())
    }
    // console.log(randomColor())
    const dataCollection = {
        labels: label,
        datasets: [{
            data: data,
            backgroundColor: bgColor,
            hoverBackgroundColor: hoverBgColor,
        }]
    }

    return (
        <div>


        </div>
    )
}

export default PieCharts
