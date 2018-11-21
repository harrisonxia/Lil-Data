// @flow
import * as React from 'react'
import styles from './main.css'

const Main = () => {
    return (
        <main className={styles.main}>
            <div className={styles.mainContainer}>
                <div className={styles.title}>Lil data</div>
                <div>
                    <span className={styles.pageHeader}>Hello World</span>
                    <br/>
                    <span className={styles.pageDescription}>
                        My Code
            <br/>
            actually works.
          </span>
                </div>
                <div className={styles.testResult}>
                </div>
                <div className={styles.summaryRow}>
                    <p>What a surprise</p>
                </div>
                <hr/>
            </div>
        </main>
    )
}

export default Main
