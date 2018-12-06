// @flow
import * as React from 'react'
import styles from './main.css'
import HeadBar from './head-bar.jsx'

const Channel = () => {
    let name = 'Lil Data'
    let text = 'Gaming Trend Analysis from 2015 to 2018'
    return (
        <main className={styles.main}>

            <HeadBar name={name} text={text}/>

            <div className={styles.mainContainer}>

                <div className={styles.charts}>
                    <p>
                        some text here
                    </p>
                </div>
            </div>

        </main>
    )
}

export default Channel
