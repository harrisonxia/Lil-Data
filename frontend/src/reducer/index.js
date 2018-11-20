import { combineReducers, createStore, applyMiddleware, compose } from 'redux'
import reducer from './reducer.js'
import thunk from 'redux-thunk'

let store = null;

export function getStore() {
  if( store === null ) {
    const appReducer = combineReducers({ store: reducer})

    store = createStore(
      appReducer,
      compose(applyMiddleware(thunk),
        window.devToolsExtension ? window.devToolsExtension() : f => f // For Chrome redux dev tool
      ))
  }

  return store
}
