// @flow
import React from 'react'
import { BrowserRouter, Route, Switch } from 'react-router-dom'

// import Header from './components/header'
import MainPage from './components/main'

export default function () {
  return (
    <BrowserRouter basename="/">
      <div key="content-wrapper">
        {/*<Header/>*/}
        <Switch>
          <Route exact path="/" component={MainPage}/>
        </Switch>
      </div>
    </BrowserRouter>)
}