import React from 'react';
import { inject, observer } from 'mobx-react';
import { Select } from 'antd';

const Option = Select.Option;

const Map_Selector = ({ viewStore, dataStore, params: { id, type } }) => {
  return !dataStore.isLoading && !id && !type && <div>
    <h2>Granularity</h2>
    <p>Choose what type of map you want to see:</p>
    <Select
      key="granularity_filter"
      style={{ width: '100%', "marginTop": "10px" }}
      defaultValue="Restaurant"
      onChange={(selected) => { 
        viewStore.setGranularity(selected)
        dataStore.load(selected, viewStore.searches)
      }}
    >
      <Option value="Restaurant">Restaurant</Option>
    </Select>
  </div>;
};

export default inject('dataStore', 'viewStore')(observer(Map_Selector));
