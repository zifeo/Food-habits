## Import openfood

Step from postgres dump to pandas dataframe.

```shell
docker run --rm --name import -it -p 5432:5432 -v (pwd):/work postgres &
docker exec -it xenodochial_montalcini /bin/sh
cd /word/data
psql -U postgres < openfood_20160108.dump
exit
# connect to the db via the notebook 
docker stop import
```
