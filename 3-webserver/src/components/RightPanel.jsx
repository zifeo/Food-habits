import React from 'react';
import { observer, inject } from 'mobx-react';

import { Col } from 'antd';

import Map from './Map';

const RightPanel = (props) => {
  const { dataStore, viewStore } = props;

  return (<div>
    <Col xs={24} sm={24} md={20} lg={20}>
      {<Map
          dataStore={dataStore}
          viewStore={viewStore}
          params={props.params}
          router={props.router}
          />}
    </Col>
  </div>);
};

export default inject('dataStore', 'viewStore')(observer(RightPanel));
