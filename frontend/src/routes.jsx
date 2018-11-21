// @flow
import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

// import Header from './components/header'
import MainPage from './components/main'

export default function () {
  return (
      // !! esto es importante
      // CHECK BASENAME FOR DEPLOYING IN DIFF ENVs
    <BrowserRouter basename="/Lil-Data/">
      <div key="content-wrapper">
        {/*<Header/>*/}
        <Switch>
          <Route exact path="/" component={MainPage}/>
        </Switch>
      </div>
    </BrowserRouter>)
}