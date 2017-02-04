# 2 Elastic Search

Now that we had all the data pre-processed we wanted to store it in a database for it to be easily accessible and searchable.
We chose elasticsearch as it is reknown to be very fast and allows us to integrate usefull matching processes such as stopword removal, ascii folding, etc...
We run an instance of it on docker on a remote server and pushed all our data to it.

## Stack with elasticsearch

Once `docker-compose up -d`, you can access elasticsearch through `localhost:23489`. In order to query, you can use Kibana from `localhost:23488` and benefite of query autocompletion. Most importance, you need to setup the right analyzer in the mapping before upload any data onto elasticsearch. This can be done by copy pasting the `mapping.es` file into Kibana.

