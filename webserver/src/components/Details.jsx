import React from 'react';
import { Link } from 'react-router';
import { observer, inject } from 'mobx-react';

const Details = (props) => {
  const nodeLists = {
    employee: [],
    competence: [],
  };

  for (let i = 0; i < props.viewStore.selectedNodes.length; i += 1) {
    nodeLists[props.viewStore.selectedNodes[i].data.type]
      .push(props.viewStore.selectedNodes[i].data);
  }

  return (<div id="details">
    <h2>Selection details</h2>
    <h3>Employees</h3>
    <ul>
      {nodeLists.employee.map(e => <li key={e.id}>{`${e.details.first_name} ${e.details.last_name}`} - <Link to={`/employee/${e.id}`}>go to</Link></li>)}
    </ul>
    <h3>Competences</h3>
    <ul>
      {nodeLists.competence.map(c => <li key={c.id}>{c.details.name} - <Link to={`/competence/${c.id}`}>go to</Link></li>)}
    </ul>
  </div>);
};

export default inject('viewStore')(observer(Details));
