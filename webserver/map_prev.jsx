import React from 'react';
import { Menu, Icon } from 'antd';
import { inject } from 'mobx-react';
import cytoscape from 'cytoscape';
import { intersection } from 'lodash';

const SubMenu = Menu.SubMenu;

const colors = {
  blue: '#3498db',
  orange: '#d35400',
  green: '#2ecc71',
  gray: '#7f8c8d',
  white: '#ecf0f1',
  red: '#e74c3c',
  dark: '#2c3e50',
  black: '#000000',
};

@inject('viewStore')
class Map extends React.Component {
  constructor() {
    super();

    this.handleMenuClick = this.handleMenuClick.bind(this);

    this.resetLayout = this.resetLayout.bind(this);
    this.renderGraph = this.renderGraph.bind(this);
    this.constructGraph = this.constructGraph.bind(this);
    this.fetchData = this.fetchData.bind(this);
    this.constructLinkedData = this.constructLinkedData.bind(this);
  }
  componentDidMount() {
    this.renderGraph();
  }
  componentDidUpdate() {
    this.renderGraph();
  }
  cy = null;
  resetLayout() {
    this.cy.layout({
      name: 'breadthfirst',
      circle: true,
      avoidOverlap: true,
      roots: this.cy.$(`#${this.props.params.id}`),
    });
  }
  constructGraph(data) {
    /* START CY INIT */
    this.cy = cytoscape({
      container: document.getElementById('graph-container'),
      userPanningEnabled: false,
      pan: 'center',
      style: cytoscape.stylesheet()
        .selector('node')
        .css({
          height: 40,
          width: 40,
          'background-fit': 'cover',
          'border-color': colors.black,
          'border-width': 2,
          padding: '20px',
          // text style
          content: 'data(label)',
          'text-outline-width': 2,
          'text-outline-color': colors.black,
          color: '#fff',
        })
        .selector('.root')
        .css({
          'border-width': 3,
          height: 60,
          width: 60,
        })
        .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': colors.blue,
          'text-outline-color': colors.blue,
        })
        .selector('.employee')
        .css({
          'background-color': colors.white,
        })
        .selector('.competence')
        .css({
          'background-color': colors.gray,
          'background-image': 'url(/images/brain.svg)',
        })
        .selector('.employee.m')
        .css({
          'background-image': 'url(/images/m.svg)',
        })
        .selector('.employee.f')
        .css({
          'background-image': 'url(/images/f.svg)',
        })
        .selector('edge')
        .css({
          width: 2,
          'line-color': '#000000',
          'curve-style': 'bezier',
          // text style
          content: 'data(label)',
          'text-outline-width': 2,
          'text-outline-color': colors.black,
          'edge-text-rotation': 'autorotate',
          color: '#fff',
        }),
      elements: data,
      motionBlur: true,
    });
    this.cy.$(`#${this.props.params.id}`).addClass('root');
    this.resetLayout();
    /* END CY INIT */

    /* START CY EVENT MANAGER */
    this.cy.on('select', () => {
      this.props.viewStore.selectedNodes = this.cy.$(':selected').jsons().filter(e => e.group === 'nodes');
    });
    this.cy.on('unselect', () => {
      this.props.viewStore.selectedNodes = this.cy.$(':selected').jsons().filter(e => e.group === 'nodes');
    });

    let tappedBefore;
    let tappedTimeout;
    this.cy.on('tap', (event) => {
      // create a doubleTap event
      const tappedNow = event.cyTarget;
      if (tappedTimeout && tappedBefore) {
        clearTimeout(tappedTimeout);
      }
      if (tappedBefore === tappedNow) {
        tappedNow.trigger('doubleTap');
        tappedBefore = null;
      } else {
        tappedTimeout = setTimeout(() => { tappedBefore = null; }, 300);
        tappedBefore = tappedNow;
      }
    });

    this.cy.on('doubleTap', 'node', (event) => {
      const nodeData = event.cyTarget.data();
      const nodeDetails = nodeData.details;
      switch (nodeData.type) {
        case 'employee': {
          const competences = nodeDetails.competences.filter(
            comp => comp.id !== parseInt(this.props.params.id, 10)
          );

          for (let i = 0; i < competences.length; i += 1) {
            this.cy.add([{
              group: 'nodes',
              classes: 'competence',
              data: {
                id: competences[i].id,
                label: `${competences[i].name}`,
                type: 'competence',
                details: competences[i],
              },
            }, {
              group: 'edges',
              data: {
                id: `${nodeData.id}_${competences[i].id}`,
                source: nodeData.id,
                target: competences[i].id,
              },
            }]);
          }
          break;
        }
        case 'competence': {
          const employees = this.props.dataStore.getEmployeesWithCompetence(nodeData.id);

          for (let i = 0; i < employees.length; i += 1) {
            this.cy.add([{
              group: 'nodes',
              classes: `employee ${employees[i].sex}`,
              data: {
                id: employees[i].id,
                label: `${employees[i].first_name} ${employees[i].last_name}`,
                type: 'employee',
                details: employees[i],
              },
            }, {
              group: 'edges',
              data: {
                id: `${nodeData.id}_${employees[i].id}`,
                source: nodeData.id,
                target: employees[i].id,
              },
            }]);
          }
          break;
        }
        default: {
          break;
        }
      }
      this.cy.nodes().removeClass('root');
      event.cyTarget.addClass('root');
      this.resetLayout();
    });

    /* END CY EVENT MANAGER */
  }
  fetchData() {
    switch (this.props.params.type) {
      case 'employee': {
        return this.props.dataStore.getEmployee(this.props.params.id);
      }
      case 'competence': {
        return this.props.dataStore.getCompetence(this.props.params.id);
      }
      default:
        return this.props.dataStore.getEmployees(this.props.filters);
    }
  }
  constructLinkedData(data) {
    const linkedDatas = [];

    switch (this.props.params.type) {
      case 'employee': {
        linkedDatas.push({
          group: 'nodes',
          classes: `employee ${data.sex}`,
          data: {
            id: data.id,
            label: `${data.first_name} ${data.last_name}`,
            type: 'employee',
            details: data,
          },
        });

        // iterate through competences for the given employee and add a node + edge
        for (let i = 0; i < data.competences.length; i += 1) {
          linkedDatas.push({
            group: 'nodes',
            classes: 'competence',
            data: {
              id: data.competences[i].id,
              label: `${data.competences[i].name}`,
              type: 'competence',
              details: data.competences[i],
            },
          });

          linkedDatas.push({
            group: 'edges',
            data: {
              id: `${data.id}_${data.competences[i].id}`,
              source: data.id,
              target: data.competences[i].id,
            },
          });
        }
        break;
      }
      case 'competence': {
        linkedDatas.push({
          group: 'nodes',
          classes: 'competence',
          data: {
            id: data.id,
            label: `${data.name}`,
            type: 'competence',
            details: data,
          },
        });

        const employees = this.props.dataStore.getEmployeesWithCompetence(this.props.params.id);
        // iterate through employees for the given competence and add a node + edge
        for (let i = 0; i < employees.length; i += 1) {
          linkedDatas.push({
            group: 'nodes',
            classes: `employee ${employees[i].sex}`,
            data: {
              id: employees[i].id,
              label: `${employees[i].first_name} ${employees[i].last_name}`,
              type: 'employee',
              details: employees[i],
            },
          });

          linkedDatas.push({
            group: 'edges',
            data: {
              id: `${data.id}_${employees[i].id}`,
              source: data.id,
              target: employees[i].id,
            },
          });
        }
        break;
      }
      // default is for the main map
      // nodes are employees and link are common competences between them
      default: {
        // add all employees in the data as a node
        for (let i = 0; i < data.length; i += 1) {
          linkedDatas.push({
            group: 'nodes',
            classes: `employee ${data[i].sex}`,
            data: {
              id: data[i].id,
              label: `${data[i].first_name} ${data[i].last_name}`,
              type: 'employee',
              details: data[i],
            },
          });
        }
        // for each node
        for (let i = 0; i < data.length; i += 1) {
          // check all other nodes
          for (let j = 0; j < data.length; j += 1) {
            // if this is a different employee (different node than itself)
            if (data[j].id !== data[i].id) {
              // get competences in common
              const inter = intersection(
                data[j].competences.map(c => c.id),
                data[i].competences.map(c => c.id)
              );
              // if these employees have a competence in common
              if (inter.length !== 0) {
                for (let k = 0; k < inter.length; k += 1) {
                  const comp = this.props.dataStore.getCompetence(inter[k]);

                  /*
                  to remove double edges we check if there's already an edge
                  for the same competence between the two employees
                  */
                  const edges = linkedDatas.filter(d => d.group === 'edges');

                  if (edges.filter(
                    edge => (
                      edge.data.id === `${data[i].id}_${data[j].id}_${comp.name}` ||
                      edge.data.id === `${data[j].id}_${data[i].id}_${comp.name}`
                    )
                  ).length === 0) {
                    linkedDatas.push({
                      group: 'edges',
                      data: {
                        id: `${data[i].id}_${data[j].id}_${comp.name}`,
                        label: comp.name,
                        source: data[i].id,
                        target: data[j].id,
                      },
                    });
                  }
                }
              }
            }
          }
        }
        break;
      }
    }

    return linkedDatas;
  }
  handleMenuClick(e) {
    if (this.cy) {
      switch (e.key) {
        case 'export:jpg': {
          // ugly solution due to the fact that HTML5 download tag not widely supported
          const link = document.createElement('a');
          link.href = this.cy.jpg();
          link.download = 'export.jpg';
          link.click();
          break;
        }
        case 'export:png': {
          const link = document.createElement('a');
          link.href = this.cy.png();
          link.download = 'export.png';
          link.click();
          break;
        }
        case 'export:svg': {
          alert('Not implemented yet');
          break;
        }
        case 'zoom:in': {
          this.cy.zoom(this.cy.zoom() * 1.1);
          this.cy.center();
          break;
        }
        case 'zoom:out': {
          this.cy.zoom(this.cy.zoom() / 1.1);
          this.cy.center();
          break;
        }
        case 'recenter': {
          this.cy.fit(10);
          break;
        }
        case 'back': {
          this.props.router.push('/');
          break;
        }
        default:
          break;
      }
    }
  }
  renderGraph() {
    const data = this.constructLinkedData(this.fetchData());
    this.constructGraph(data);
  }
  render() {
    return (<div>
      <Menu mode="horizontal" onClick={this.handleMenuClick}>
        <SubMenu title={<span><Icon type="download" />Export</span>}>
          <Menu.Item key="export:jpg">To JPG</Menu.Item>
          <Menu.Item key="export:png">To PNG</Menu.Item>
          <Menu.Item key="export:svg">To SVG</Menu.Item>
        </SubMenu>
        <Menu.Item key="zoom:in">
          <Icon type="plus-circle-o" /> Zoom in
          </Menu.Item>
        <Menu.Item key="zoom:out">
          <Icon type="minus-circle-o" /> Zoom out
          </Menu.Item>
        <Menu.Item key="recenter">
          <Icon type="select" /> Fit to viewport
          </Menu.Item>
        {this.props.params.type && this.props.params.id &&
          <Menu.Item key="back" style={{ float: 'Right' }}>
            <Icon type="rollback" /> Back to main map
          </Menu.Item>}
      </Menu>
      <div id="graph-container" />
    </div>);
  }
}

export default Map;
