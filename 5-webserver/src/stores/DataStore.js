import { observable, action, computed, whyRun } from 'mobx';
import { flatten, uniqBy } from 'lodash';
import axios from 'axios';
import elasticsearch from 'elasticsearch'

export default class DataStore {
  @observable restaurantsResult = []

  client = new elasticsearch.Client({
    host: 'http://51.15.135.251:23489',
    apiVersion: '5.x',
    log: 'info'
  });

  @computed get restaurantsQueryLoaded() {
    return this.restaurantsResult.length != 0;
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
      case 'Restaurant' : 
        this.loadRestaurantsQuery(searches)
        break
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

  getResults() {
    let ret = [...this.results];
    return ret
  }

}