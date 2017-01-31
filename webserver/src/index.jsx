import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, browserHistory } from 'react-router';
import { Provider } from 'mobx-react';

import DataStore from './stores/DataStore';
import ViewStore from './stores/ViewStore';
import App from './App';

const dataStore = new DataStore();
const viewStore = new ViewStore();

const stores = { dataStore, viewStore };

ReactDOM.render(
  <Provider {...stores} >
    <Router history={browserHistory}>
      <Route path="/" component={App} onLeave={() => viewStore.resetFilters()} />
      <Route path="/:granularity/:filter" component={App} />
    </Router>
  </Provider>,
  document.getElementById('app')
);
