// @flow
import * as React from 'react'
import styles from './main.css'
import NavBar from './nav.jsx'

const Main = () => {
    return (
        <main className={styles.main}>
            <NavBar/>
            <br/>
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
                    <p className={styles.stupidFont}>What a surprise</p>
                </div>
                <hr/>
            </div>
        </main>
    )
}

export default Main
