import 'babel-polyfill' // For IE
import React from 'react'
import ReactDOM from 'react-dom'
import { Provider } from 'react-redux'
import { getStore } from './reducer/index.js'
import './index.css'
import Routes from './routes'

const store = getStore()
// In case we need redux..
// store.dispatch()

let app = document.createElement('div')
app.id = 'app'
app.className = 'content-wrapper'
document.body.insertBefore(app, null)

ReactDOM.render(
    <Provider store={store}>
      <Routes/>
    </Provider>,
  document.getElementById('app')
)
