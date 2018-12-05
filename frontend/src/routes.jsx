import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

import NavBar from './components/nav.jsx'
import MainPage from './components/main.jsx'
import Charts from './components/charts.jsx'

export default function () {
    console.log(process.env)
    console.log(process.env)
    return (
    // !! esto es importante
    // CHECK BASENAME FOR DEPLOYING IN DIFF ENVs
        <BrowserRouter basename={process.env.PUBLIC_URL}>
            <div key="content-wrapper">
                <NavBar/>
                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route exact path="/charts" component={Charts}/>
                </Switch>
            </div>
        </BrowserRouter>
    )
}