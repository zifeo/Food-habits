import { observable, computed, action } from 'mobx';
import L from 'leaflet';
import markerClusterGroup from 'leaflet.markercluster'

export default class ViewStore {
  @observable granularity = ""
  @observable searches = [""]
  mymap = null
  current_layer = []

  @action setGranularity(newGranurality) {
    console.log(newGranurality)
    this.granularity = newGranurality
  }

  @action setSearches(newSearches) {
    console.log(newSearches)
    this.searches = newSearches
  }

  mapSetup(map_id) {
    this.mymap = L.map('mapid').setView([46.599505, 3.480752], 6)
    L.tileLayer("https://api.mapbox.com/styles/v1/highuptown/ciyj9651g00242spb105v5ae6/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiaGlnaHVwdG93biIsImEiOiJjaXlqOHc3dzcwNWlsMzJvNmJwMWVyYjZoIn0.shBfo0_CPJoo6Pj015ZBwA").addTo(this.mymap)
  }

  resetLayers() {
    this.current_layer.forEach((e) => {
      e.remove()
    })
    this.current_layer = []
  }

  addGeoJsonLayer(results, GeoJSON) {
    var layer = L.geoJSON(GeoJSON, {
      style: function(feature) {
        console.log(feature.properties.code)
      }
    }).addTo(this.mymap)
    this.current_layer.push(layer)
  }

  addRestaurantLayer(results) {
    console.log("markers")
    var markers = L.markerClusterGroup({})
    console.log("allmarkers")
    var allMarkers = results.map((r) => {
      var marker = L.marker([r.lat, r.lng]);
      marker.bindPopup(r.name)
      return marker
    })
    console.log("adding")
    markers.addLayers(allMarkers)
    console.log("addt")
    markers = markers.addTo(this.mymap)
    console.log("push")
    this.current_layer.push(markers)
  }
}
