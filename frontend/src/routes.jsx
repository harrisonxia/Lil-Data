import React from 'react'
import { HashRouter, BrowserRouter, Route, Switch } from 'react-router-dom'

import NavBar from './components/nav.jsx'
import MainPage from './components/main.jsx'
import Charts from './components/charts.jsx'

export default function () {
    console.log(process.env.PUBLIC_URL)
    const basePath = '/Lil-Data'
    return (
        <BrowserRouter basename={'/Lil-Data'}>
            <div key="content-wrapper">
                <NavBar/>
                <Switch>
                    <Route exact path="/" component={MainPage}/>
                    <Route exact path="/charts" component={Charts}/>
                </Switch>
            </div>
        </BrowserRouter>
    )
    // return (
    //     // CHECK BASENAME FOR DEPLOYING IN DIFF ENVs
    //     <HashRouter basename={process.env.PUBLIC_URL} hashType='noslash'>
    //         <div key="content-wrapper">
    //             <NavBar/>
    //             <Switch>
    //                 <Route path={'/'} component={MainPage}/>
    //                 <Route path={'/charts'} component={Charts}/>
    //             </Switch>
    //         </div>
    //     </HashRouter>
    // )


}