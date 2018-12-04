// @flow
import * as React from 'react'
import styles from './main.css'
import NavBar from './nav.jsx'
import HeadBar from './head-bar.jsx'

const Main = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>
            <NavBar/>
            <br/>
            <HeadBar name={name} text={text}/>
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
                </div>
                <div className={styles.summaryRow}>
                    <div className={styles.stupidFont}>What a surprise</div>
                </div>
                <hr/>

            </div>
        </main>
    )
}

export default Main
