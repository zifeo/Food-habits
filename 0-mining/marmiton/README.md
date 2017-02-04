# Marmiton Scraping
We first tried to scrap and parse all Marmiton's recipes with the marmiton_naive.py file, but quickly got blocked by reCaptcha.
So we created marmiton_urls.py to gather many recipes' URLs not caring about duplicates which gave us ~500k. Then we sorted them and removed any duplicates, which gaves us the correct number of recipes hosted on Marmiton.
Finally, with the marmiton.py file which uses those URLs, we parsed the data we needed from each recipe by running it as many times as necessary. It only scraps 1000 URLs at a time in order to avoid Marmiton limitations. 

## Usage
### Create folder marmiton_data
mkdir marmiton_data

### Run marmiton_urls for max 10 minutes in order to grab many URLS
timeout 10m scrapy runspider marmiton_urls.py


### Keep only the uniq URLS
sort marmiton_data/urls_all | uniq  > marmiton_data/urls_todo
cp marmiton_data/urls_todo marmiton_data/urls_all


### Run as many times as necessary (by hand to avoid captcha)
### Do not forget to change JSON file name to avoid overwriting
scrapy runspider -o marmiton_data/data.json marmiton.py


### Regroup all scraped data 
for f in marmiton_data/*.json; do cat $f >> scraped_data.json; done


### Keep only uniq recipes in case there are some duplicates
for url in `cat marmiton_data/urls-all`; do grep -m1 -P "$url" marmiton_data/scraped_data.json >> uniq_data.json; done


### Edit so that it is a valid JSON file
# Add mising commas
sed -i.bak 's/}$/},/g' marmiton_data/uniq_data.json

### Remove comma on last line
sed -i '$s/},$/}/' marmiton_data/uniq_data.json


### Add brackets at the beginning and end of the file
sed -i -e '1s/^/[\n/' -e '$s/$/\n]/' marmiton_data/uniq_data.json

### Clean
mv marmiton_data/uniq_data.json ./marmiton.json
rm --ri marmiton_data
