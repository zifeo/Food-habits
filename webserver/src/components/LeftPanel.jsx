import React from 'react';
import { Row, Col } from 'antd';

import Map_Selector from './Map_Selector'
import SearchIntf from './SearchIntf'

const LeftPanel = props => <Col xs={24} sm={24} md={4} lg={4} className="padded-col">
  <Row>
    <SearchIntf params={props.params} router={props.router}/>
    <Map_Selector params={props.params} router={props.router}/>
  </Row>
</Col>;

export default LeftPanel;
