import React from 'react';
import { inject, observer } from 'mobx-react';
import mobx from 'mobx'

@observer
class Map extends React.Component {

  constructor() {
    super()
  }

  componentDidMount() {
    this.props.viewStore.mapSetup('mapid')
  }

  componentDidUpdate() {

  }

  render() {
    
    switch(this.props.viewStore.granularity) {
      case 'Departement/Canton' : 
        this.props.viewStore.resetLayers()
        if (this.props.dataStore.departementsLoaded) {
          this.props.viewStore.addGeoJsonLayer(
            this.props.dataStore.departmentsResult, 
            this.props.dataStore.departmentsGeoJSON
          )
        }
        if (this.props.dataStore.cantonsLoaded) {
          this.props.viewStore.addGeoJsonLayer(
            this.props.dataStore.cantonsResult, 
            this.props.dataStore.cantonsGeoJSON
          )
        }
        break
      case 'Restaurant' :
        console.log("showing restaurants")
        if (this.props.dataStore.restaurantsQueryLoaded) {
          console.log("show")
          console.log(this.props.dataStore.restaurantsResult)
          this.props.viewStore.resetLayers()
          this.props.dataStore.restaurantsResult.forEach((res, i) => {
            console.log(i)
            this.props.viewStore.addRestaurantLayer(res, i)
          })
          
        }
        break
    }

    return (<div id="mapid"></div>);
  }
}

export default Map;
