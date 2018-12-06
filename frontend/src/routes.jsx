import React from 'react'
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom'

import MainPage from './components/main.jsx'
import Charts from './components/charts.jsx'
import Category from './components/category.jsx'
import Channel from './components/channel.jsx'
import DataCollecting from './components/dataCollecting.jsx'
import styles from './components/main.css'

const MainMenu = () => {
    return (<div>
        <Link to="/">
            <p>Lil Data</p>
        </Link>
        <hr className={styles.divider}/>
        <Link to="/datacollecting">
            <p>Data Collecting</p>
        </Link>
        <Link to="/category">
            <p>Category</p>
        </Link>
        <Link to="/charts">
            <p>Charts</p>
        </Link>
        <Link to="/channel">
            <p>Channel</p>
        </Link>
        {/*<Link to="https://github.com/harrisonxia/Lil-Data">*/}
            {/*<p>Github</p>*/}
        <a href='https://github.com/harrisonxia/Lil-Data' target='_blank'>Github</a>
        {/*</Link>*/}
    </div>)
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
                    <Route exact path="/category" component={Category}/>
                    <Route exact path="/charts" component={Charts}/>
                    <Route exact path="/channel" component={Channel}/>
                </Switch>
            </div>
        </BrowserRouter>
    )


}