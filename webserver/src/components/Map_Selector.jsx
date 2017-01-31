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
      style={{ width: '100%' }}
      placeholder="Select granularity"
      onChange={(selected) => { 
        viewStore.setGranularity(selected)
        dataStore.load(selected, viewStore.searches)
      }}
    >
      <Option value="Restaurant">Restaurant</Option>
      <Option value="Departement/Canton">Departement/Canton</Option>
      <Option value="Region/Canton">Region/Canton</Option>
    </Select>
    <br />
    <br />
    <h2>Nutriments</h2>
    <p>Nutriments for comparaison:</p>
    <Select
      multiple
      key="nutriments_filters"
      style={{ width: '100%' }}
      placeholder="Select the nutriments to shows"
      onChange={(selected) => { viewStore.filters = { type: 'research_group', selected }; }}
    >
      {dataStore.nutriments.map(
        r => <Option key={r.id} value={r.id.toString()}>{r.name}</Option>
      )}
    </Select>
  </div>;
};

export default inject('dataStore', 'viewStore')(observer(Map_Selector));
