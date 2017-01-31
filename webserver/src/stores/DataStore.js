import { observable, action, computed, whyRun } from 'mobx';
import { flatten, uniqBy } from 'lodash';
import axios from 'axios';
import elasticsearch from 'elasticsearch'

export default class DataStore {
  @observable nutriments = [{name:"test1", id:1}, {name:"test2", id:2}, {name:"test3", id:3}, {name:"test4", id:4}];
  @observable departmentsGeoJSON = null
  @observable cantonsGeoJSON = null
  @observable cantonsResult = []
  @observable departmentsResult = []
  @observable restaurantsResult = []

  client = new elasticsearch.Client({
    host: 'http://51.15.135.251:23489',
    apiVersion: '5.x',
    log: 'info'
  });

  @computed get departementsLoaded() {
    return this.departmentsGeoJSON != null
  }

  @computed get cantonsLoaded() {
    return this.cantonsGeoJSON != null
  }

  @computed get restaurantsQueryLoaded() {
    return this.restaurantsResult.length != 0;
  }

  @computed get nutrimentsLoaded() {
    return this.nutriments.length === 0;
  }

  @action loadDepartementsQuery(searches) {
    this.departmentsResult = []
    var query = []

    /*if (searches.length > 0 && searches[0] != "") {

      searches.forEach((s) => {
        dep_queries = []
        this.departmentsGeoJSON.features.forEach((dep) => {
          var code = dep.properties.code

          dep_queries.push({
            query: {
              index: 'restaurants',
              scroll: '30s',
              body: {
                "query": {
                  "bool": {
                    "must": [
                      {
                        "multi_match": {
                          "query": s,
                          "fields": [
                            "mains.name", 
                            "desserts.name", 
                            "starters.name", 
                            "drinks.name"
                            ] 
                        }
                      },
                      {
                        "prefix": {
                          "zip": {
                            "value": code
                          }
                        }
                      }
                    ]
                  }
                },
                size: 500,
                _source: [
                  "name",
                  "lat",
                  "lng"
                ]
              },
              code: code
            } 
          })
        })

        query.push(dep_queries)
      })

    } else {
      this.departmentsGeoJSON.features.forEach((dep) => {
        var code = dep.properties.code

        query.push({
          query: {
            index: 'restaurants',
            scroll: '30s',
            body: {
              "query": {
                "bool": {
                  "must": [
                    {
                      "prefix": {
                        "zip": {
                          "value": code
                        }
                      }
                    }
                  ]
                }
              },
              size: 500,
              _source: [
                "name",
                "lat",
                "lng"
              ]
            }
          },
          code: code 
        })
      })
    }
    console.log("queries")
    console.log(len(query))
    
    query.forEach((q) => {

      this.queryElasticSearch(
        q.query, 
        (acc) => {
          this.departmentsResult.push([q.code, acc])
        }
      )
    })*/
  }

  @action loadRestaurantsQuery(searches) {
    this.restaurantsResult = []
    var query = []

    if (searches.length > 0 && searches[0] != "") {

      searches.forEach((s) => {
        query.push({
          index: 'restaurants',
          scroll: '30s',
          body: {
            query: {
              multi_match: {
                type: "phrase",
                query: s,
                fields: [
                  "mains.name", 
                  "desserts.name", 
                  "starters.name", 
                  "drinks.name"] 
              }
            },
            size: 500,
            _source: [
              "name",
              "lat",
              "lng"
            ]
          }
        })
      })

    } else {
      query.push({
        index: 'restaurants',
        scroll: '30s',
        body: {
          query: {
            match_all: { }
          },
          size: 500,
          _source: [
            "name",
            "lat",
            "lng"
          ]
        }
      })
    }

    console.log(query)

    query.forEach((q) => {
      this.queryElasticSearch(
        q, 
        (acc) => {
          this.restaurantsResult.push(acc)
        }
      )
    })
  }

  @action load(select, searches) {
    switch(select) {
      case 'Departement/Canton' : 
        this.loadDepartements(searches) 
        this.loadCantons(searches)
        break;
      case 'Restaurant' : 
        this.loadRestaurantsQuery(searches)
        break
    }
  }

  @action loadCantons(searches) {
    if (this.cantonsGeoJSON == null){
      axios.get('/data/cantons.geojson')
        .then((response) => {
          console.log(response.data)
          this.cantonsGeoJSON = response.data
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }

  @action loadDepartements(searches) {
    if (this.departmentsGeoJSON == null){
      axios.get('/data/departements.geojson')
        .then((response) => {
          console.log(response.data)
          this.departmentsGeoJSON = response.data
          this.loadDepartementsQuery(searches)
        })
        .catch((error) => {
          console.log(error);
        });
    }
  }

  @action queryElasticSearch = (query, onDone) => {
    var acc = []
    let getMoreUntilDone = (resp) => {
      resp.hits.hits.forEach((h) => {
        acc.push(h._source)
      })

      if (resp.hits.total > acc.length) {
        console.log("scroll")
        this.client.scroll({
          scrollId: resp._scroll_id,
          scroll: '30s'
        }).then(getMoreUntilDone, function (err) {
          console.trace(err.message);
        })
      } else {
        console.log("finished")
        onDone(acc)
      }
    }

    this.client.search(query)
      .then(getMoreUntilDone , function (err) {
        console.trace(err.message);
      });
  }

  @action loadRestaurants = () => {
    var query = {
      index: 'restaurants',
      scroll: '30s',
      body: {
        query: {
          match_all: { }
        },
        size: 500,
        _source: [
          "name",
          "lat",
          "lng"
        ]
      }
    }
    
    this.queryElasticSearch(
      query, 
      (acc) => this.restaurantsResult = acc
    )
  }

  @action loadRestaurants = () => {
    var query = {
      index: 'restaurants',
      scroll: '30s',
      body: {
        query: {
          match_all: { }
        },
        size: 500,
        _source: [
          "name",
          "lat",
          "lng"
        ]
      }
    }

    this.queryElasticSearch(
      query, 
      (acc) => this.restaurantsResult = acc
    )
  }


  @action loadEmployees() {
    /*
    axios.get('/data/sample.json')
      .then((response) => {
        this.schools = uniqBy(response.data.employees.map(emp => emp.school), 'id');
        this.researchGroups = uniqBy(response.data.employees.map(emp => emp.research_group), 'id');
        this.competences = uniqBy(flatten(response.data.employees.map(emp => emp.competences)), 'id');
        this.employees = response.data.employees;
      })
      .catch((error) => {
        console.log(error);
      });
    */
  }

  getResults() {
    let ret = [...this.results];
    return ret
  }

  getNutriments() {
    let ret = [...this.nutriments]; // Copy an array like this.employees.slice()
    return ret;
  }

  getNutriment(nutrimentId) {
    return this.nutriments.find(e => e.id === parseInt(nutrimentId, 10));
  }

}
