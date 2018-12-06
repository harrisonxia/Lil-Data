import React from 'react'
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom'

import MainPage from './components/main.jsx'
import Charts from './components/charts.jsx'
import TopCategoryByStream from './components/topCategoryByStream.jsx'
import Channel from './components/channel.jsx'
import DataCollecting from './components/dataCollecting.jsx'
import styles from './components/main.css'
import TopCategoryByFollower from './components/topCategoryByFollower'
import TopCategoryByViewer from './components/topCategoryByViewer'
import TimeFrame from './components/streamByTimeframe'
import Language from './components/language'
const MainMenu = () => {
    return (
        <div>
            <Link to="/">
                <p className={styles.sidenavTitle}>Lil Data</p>
            </Link>
            <hr className={styles.divider}/>
            <Link to="/datacollecting">
                <p>Data Collecting</p>
            </Link>

            <p className={styles.sidenavText}>Top 20 Categories: </p>
            <ul className={styles.sidenavUl}>
                <li><Link to="/topcategorybystream">by streams</Link></li>
                <li><Link to="/topcategorybyviewer">by viewers</Link></li>
                <li><Link to="/topcategorybyfollower">by followers</Link></li>
            </ul>
            <Link to="/timeFrame">
                <p>Time frames </p>
            </Link>
            <Link to="/language">
                <p>Languages</p>
            </Link>
            {/*<ul className={styles.sidenavUl}>*/}
                {/*<li><Link to="/timeFrame">by timeframe</Link></li>*/}
                {/*/!*<li><Link to="/topcategorybyviewer">by viewers</Link></li>*!/*/}
                {/*/!*<li><Link to="/topcategorybyfollower">by followers</Link></li>*!/*/}
            {/*</ul>*/}
            <Link to="/charts">
                <p>Charts</p>
            </Link>
            <Link to="/channel">
                <p>Channel</p>
            </Link>
            <a href='https://github.com/harrisonxia/Lil-Data' target='_blank'>Github</a>
            {/*</Link>*/}
        </div>
    )
}


export default function () {
    // console.log(process.env.PUBLIC_URL)
    const basePath = '/Lil-Data'
    return (
        <BrowserRouter basename={basePath}>
            <div key="content-wrapper">
                {/*<NavBar/>*/}
                <div className={styles.sidenav}>
                    <Route path={'/'} component={MainMenu}/>
                    {/*<Route exact path="/" component={Home}/>*/}
                    {/*<Route exact path="/charts" component={Charts}/>*/}
                    {/*<Route exact path="/code" component={Code}/>*/}
                    {/*<Route exact path="/contact" component={Contact}/>*/}
                </div>

                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route exact path="/datacollecting" component={DataCollecting}/>
                    <Route exact path="/topcategorybystream" component={TopCategoryByStream}/>
                    <Route exact path="/topcategorybyfollower" component={TopCategoryByFollower}/>
                    <Route exact path="/topcategorybyviewer" component={TopCategoryByViewer}/>
                    <Route exact path="/timeFrame" component={TimeFrame}/>
                    <Route exact path="/language" component={Language}/>
                    <Route exact path="/charts" component={Charts}/>
                    <Route exact path="/channel" component={Channel}/>
                </Switch>
            </div>
        </BrowserRouter>
    )


}