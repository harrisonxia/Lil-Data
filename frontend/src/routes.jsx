import React from 'react'
import {BrowserRouter, Route, Switch, Link} from 'react-router-dom'

import NavBar from './components/nav.jsx'
import MainPage from './components/main.jsx'
import Charts from './components/charts.jsx'


const MainMenu = () => {
    return (<div>
        <Link to="/">
            <button>home</button>
        </Link>
        <Link to="/about">
            <button>About</button>
        </Link>
        <Link to="/code">
            <button>code</button>
        </Link>
        <Link to="/code">
            <button>contact</button>
        </Link>
        <Link to="/info">
            <button>info</button>
        </Link>
    </div>)
}


const Home = () => (
    <div>
        <MainMenu/>
    </div>
)


const About = () => (
    <div>
        About
    </div>
)

const Code = () => (
    <div>
        Code
    </div>
)

const Contact = () => (
    <div>
        Contact
    </div>
)
const info = () => (
    <div>
        info
    </div>
)
export default function () {
    // console.log(process.env.PUBLIC_URL)
    const basePath = '/Lil-Data'
    return (
        <BrowserRouter basename={basePath}>
            <div key="content-wrapper">
                {/*<NavBar/>*/}
                <div>
                    <Route path={'/'} component={MainMenu}/>
                    {/*<Route exact path="/" component={Home}/>*/}
                    <Route exact path="/about" component={Charts}/>
                    <Route exact path="/code" component={Code}/>
                    <Route exact path="/contact" component={Contact}/>
                </div>
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