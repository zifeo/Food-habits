## Stack with elasticsearch

Once `docker-compose up -d`, you can access elasticsearch through `localhost:23489`. In order to query, you can use Kibana from `localhost:23488` and benefite of query autocompletion. Most importance, you need to setup the right analyzer in the mapping before upload any data onto elasticsearch. This can be done by copy pasting the `mapping.es` file into Kibana.

