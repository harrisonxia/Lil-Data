import React from 'react'
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom'

import MainPage from './components/main.jsx'
import TopCategoryByStream from './components/topCategoryByStream.jsx'
import DataCollecting from './components/dataCollecting.jsx'
import styles from './components/main.css'
import TopCategoryByFollower from './components/topCategoryByFollower'
import TopCategoryByViewer from './components/topCategoryByViewer'
import TimeFrame from './components/streamByTimeframe'
import Language from './components/language'
import TopCategoryByLang from './components/topCategoryByLanguage'
import PopularChannel from './components/popularChannel'
import Prediction from './components/prediction'
import Reports from './components/reports'
const MainMenu = () => {
    return (
        <div>
            <Link to="/">
                <p className={styles.sidenavTitle}>Lil Data</p>
            </Link>
            <hr className={styles.divider}/>
            <Link to="/reports">
                <p>Lil Report</p>
            </Link>
            <Link to="/datacollecting">
                <p>Data Collecting</p>
            </Link>
            <p className={styles.sidenavText}>Top 20 Categories: </p>
            <ul className={styles.sidenavUl}>
                <li><Link to="/topcategorybystream">by streams</Link></li>
                <li><Link to="/topcategorybyviewer">by viewers</Link></li>
                <li><Link to="/topcategorybyfollower">by followers</Link></li>
                <li><Link to="/topcategorybylang">by languages</Link></li>
            </ul>
            <Link to="/popularchannel">Top 10 Channels</Link>
            <Link to="/prediction">2019-01-01 ML Prediction</Link>
            <Link to="/timeFrame">
                <p>Time frames </p>
            </Link>
            <Link to="/language">
                <p>Languages</p>
            </Link>

            <a href='https://github.com/harrisonxia/Lil-Data' target='_blank'>Github</a>
        </div>
    )
}


export default function () {
    const basePath = '/Lil-Data'
    return (
        <BrowserRouter basename={basePath}>
            <div key="content-wrapper">
                <div className={styles.sidenav}>
                    <Route path={'/'} component={MainMenu}/>
                </div>

                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route exact path="/reports" component={Reports}/>
                    <Route exact path="/datacollecting" component={DataCollecting}/>
                    <Route exact path="/topcategorybystream" component={TopCategoryByStream}/>
                    <Route exact path="/topcategorybyfollower" component={TopCategoryByFollower}/>
                    <Route exact path="/topcategorybyviewer" component={TopCategoryByViewer}/>
                    <Route exact path="/topcategorybylang" component={TopCategoryByLang}/>
                    <Route exact path="/popularchannel" component={PopularChannel}/>
                    <Route exact path="/prediction" component={Prediction}/>
                    <Route exact path="/timeFrame" component={TimeFrame}/>
                    <Route exact path="/language" component={Language}/>
                </Switch>
            </div>
        </BrowserRouter>
    )


}