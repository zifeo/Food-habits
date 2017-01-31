import React from 'react';
import { withRouter } from 'react-router';

import { LocaleProvider, Row } from 'antd';
import antdEn from 'antd/lib/locale-provider/en_US';

import LeftPanel from './components/LeftPanel';
import RightPanel from './components/RightPanel';

const App = props => <LocaleProvider locale={antdEn}>
  <Row>
    <LeftPanel params={props.params} router={props.router} />
    <RightPanel params={props.params} router={props.router} />
  </Row>
</LocaleProvider>;

export default withRouter(App);
