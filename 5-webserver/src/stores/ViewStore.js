import { observable, computed, action } from 'mobx';
import L from 'leaflet';
import markerClusterGroup from 'leaflet.markercluster'

const icons = [
    new L.Icon({
      iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    }),
    new L.Icon({
      iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    }),
    new L.Icon({
      iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    }),
    new L.Icon({
      iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-orange.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    }),
    new L.Icon({
      iconUrl: 'https://cdn.rawgit.com/pointhi/leaflet-color-markers/master/img/marker-icon-yellow.png',
      shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41]
    })
  ]

export default class ViewStore {
  @observable granularity = "Restaurant"
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

  addRestaurantLayer(results, i) {
    var allMarkers = results.map((r) => {
      var marker = L.marker(
        [r.lat, r.lng],  
        {icon: icons[i]}
      );
      marker.bindPopup(r.name)
      return marker
    })

    if (results.length > 1000) {
      var markers = L.markerClusterGroup()
      markers.addLayers(allMarkers)
      markers = markers.addTo(this.mymap)
      this.current_layer.push(markers)
    } else {
      allMarkers.forEach((m) => {
        m.addTo(this.mymap)
      })
      this.current_layer.push(...allMarkers)
    }
  }
}
