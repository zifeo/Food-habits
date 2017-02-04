# 2 Elastic Search

Now that we had all the data pre-processed, we wished to store it in a database so that it could be easily accessible and searchable.
We chose elasticsearch as it is reknown to be very fast, and it allows us to integrate useful matching processes such as stopword removal, ascii folding, etc...
On a remote server, we ran an instance of elasticsearch on Docker and sent all our data to it.

## Stack with elasticsearch

Once `docker-compose up -d` is done executing, you can access elasticsearch via `localhost:23489`. In order to query it, you can use Kibana via `localhost:23488` and benefit from the query auto-completion. Most importantly, you need to setup the right analyzer in the mapping before uploading any data onto elasticsearch. This can be done by copy-pasting the `mapping.es` file into Kibana.

