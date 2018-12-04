// @flow
import * as React from 'react'
import styles from './main.css'
import NavBar from './nav.jsx'
import { Treemap } from 'recharts'
import HeadBar from './head-bar'

const data = [
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
const COLORS = ['#8889DD', '#9597E4', '#8DC77B', '#A5D297', '#E2CF45', '#F8C12D']

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>
            <NavBar/>
            <br/>
            <HeadBar name={name} text={text}/>

            <div className={styles.charts}>
                {/* <h2>This is a <s>doughnut</s> donut chart</h2> */}
            </div>
            <div className={styles.mainContainer}>
                <Treemap
                    width={730}
                    height={250}
                    data={data}
                    dataKey="size"
                    ratio={4 / 3}
                    stroke="#fff"
                    fill="#8884d8"
                />
            </div>
        </main>
    )
}

export default Main
