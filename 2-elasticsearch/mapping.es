PUT recipes
{
   "settings": {
      "analysis": {
         "analyzer": {
            "custom_analyzer": {
               "tokenizer": "standard",
               "filter": [
                    "lowercase",
                    "custom_ascii",
                    "custom_stop",
                    "custom_stemmer",
                    "custom_length",
                    "custom_spacing_removal",
                    "custom_bigram",
                    "trim"
                ]
            }
         },
         "filter": {
            "custom_ascii": {
                "type" : "asciifolding",
                "preserve_original" : false
            },
            "custom_spacing_removal": {
                "type": "pattern_replace",
                "pattern": "( +)",
                "replacement": " "
            },
            "custom_stop": {
                "type": "stop",
                "stopwords": "_french_",
                "ignore_case": true,
                "remove_trailing": true
            },
            "custom_stemmer" : {
                "type": "stemmer",
                "name": "light_french"
            },
            "custom_bigram" : {
                "type" : "shingle",
                "min_shingle_size": 2,
                "max_shingle_size": 2,
                "output_unigrams": true,
                "filler_token": ""
            },
            "custom_length": {
                "type": "length",
                "min": 2
            }
        }
      }
   },
   "mappings": {
        "_default_": {
            "properties": {
                "name": {
                    "type": "text",
                    "term_vector": "yes",
                    "analyzer": "custom_analyzer",
                    "fielddata": true
                },
                "ingredients": {
                  "properties": {
                    "content": {
                      "type": "text",
                      "term_vector": "yes",
                      "analyzer": "custom_analyzer",
                      "fielddata": true
                    }
                  }
                }
            }
        }
   }
}

PUT recipes_nested
{
   "settings": {
      "analysis": {
         "analyzer": {
            "custom_analyzer": {
               "tokenizer": "standard",
               "filter": [
                    "lowercase",
                    "custom_ascii",
                    "custom_stop",
                    "custom_stemmer",
                    "custom_length",
                    "custom_spacing_removal",
                    "custom_bigram",
                    "trim"
                ]
            }
         },
         "filter": {
            "custom_ascii": {
                "type" : "asciifolding",
                "preserve_original" : false
            },
            "custom_spacing_removal": {
                "type": "pattern_replace",
                "pattern": "( +)",
                "replacement": " "
            },
            "custom_stop": {
                "type": "stop",
                "stopwords": "_french_",
                "ignore_case": true,
                "remove_trailing": true
            },
            "custom_stemmer" : {
                "type": "stemmer",
                "name": "light_french"
            },
            "custom_bigram" : {
                "type" : "shingle",
                "min_shingle_size": 2,
                "max_shingle_size": 2,
                "output_unigrams": true,
                "filler_token": ""
            },
            "custom_length": {
                "type": "length",
                "min": 2
            }
        }
      }
   },
   "mappings": {
        "_default_": {
            "properties": {
                "name": {
                    "type": "text",
                    "term_vector": "yes",
                    "analyzer": "custom_analyzer",
                    "fielddata": true
                },
                "ingredients": {
                  "type": "nested",
                  "properties": {
                    "content": {
                      "type": "text",
                      "term_vector": "yes",
                      "analyzer": "custom_analyzer",
                      "fielddata": true
                    }
                  }
                }
            }
        }
   }
}

PUT products1
{
   "settings": {
      "analysis": {
         "analyzer": {
            "custom_analyzer": {
               "tokenizer": "standard",
               "filter": [
                    "lowercase",
                    "custom_ascii",
                    "custom_stop",
                    "custom_stemmer",
                    "custom_length",
                    "custom_spacing_removal",
                    "custom_bigram",
                    "trim"
                ]
            }
         },
         "filter": {
            "custom_ascii": {
                "type" : "asciifolding",
                "preserve_original" : false
            },
            "custom_spacing_removal": {
                "type": "pattern_replace",
                "pattern": "( +)",
                "replacement": " "
            },
            "custom_stop": {
                "type": "stop",
                "stopwords": "_french_",
                "ignore_case": true,
                "remove_trailing": true
            },
            "custom_stemmer" : {
                "type": "stemmer",
                "name": "light_french"
            },
            "custom_bigram" : {
                "type" : "shingle",
                "min_shingle_size": 2,
                "max_shingle_size": 2,
                "output_unigrams": true,
                "filler_token": ""
            },
            "custom_length": {
                "type": "length",
                "min": 2
            }
        }
      }
   },
   "mappings": {
        "_default_": {
            "properties": {
                "name": {
                    "type": "text",
                    "term_vector": "yes",
                    "analyzer": "custom_analyzer",
                    "fielddata": true,
                    "fields": {
                      "length": { 
                        "type": "token_count",
                        "analyzer": "standard"
                      }
                    }
                }
            }
        }
   }
}


