# 0 Mining

For our project we needed a lot of data to be statistically significant as we knew there would be a lot of noise going from restaurants to nutriments.

## Restaurants

We started with LaFourchette.com which is a very well known restaurant reservation / recommendation website both in France and Switzerland.
We used scrapy to scrap as many of the restaurants we could get from the website. 
We got a total of 11'567 restaurants (9'997 in France, 1'570 in switzerland) with the complete list of the meals they propose. 
We thought this was enough as it gave us more than 100'000 meals.

## Recipes

For recipes we needed a lot more data to be able to correctly link them to the restaurants meals.
Since there is not **one** big French recipes website, we decided to scrap a few of them : 
750g, cuisineAZ, journaldesfemmes, ricardocuisine and marmiton.
The one which gave us the most difficulties is marmiton, you can see why in the README file in the marmiton folder.
With this we had a total of more than 170'595 recipes.

## nutriments

For nutrition facts, we scrapped the FDDB database to complement our original dataset from OpenFood, a database of products sold in Switzerland (from the Coop and Migros stores).
This website had a total of 450 products with their nutriment composition which we used later in our analysis.
