#! /usr/bin/python3
import re
import json
import sys
from bs4 import BeautifulSoup

# menu fail
# ratings and review not executed

def parse_html(html, currency):

    def get_name(html):
        parsed_name = None
        name = html.select("summary h1")
        if name:
            parsed_name = name[0].string
        del name
        return parsed_name
    
    def get_address(html):
        parsed_addr = None
        addr = html.select("summary span.restaurantSummary-address")
        if addr:
            labels = ["street", "ZIP", "city", "country"]
            values = [v.strip(" ,") for v in addr[0].string.strip().split('\n')]
            parsed_addr = dict(zip(labels, values))
            del labels
        del addr
        return parsed_addr 
    
    def get_price(html):
        price = html.select("summary div.restaurantSummary-price")
        parsed_price = None
        if price:
            parsed_price = int(re.sub(r"[^\d]", '', price[0].text))
        del price
        return parsed_price
    
    
    def get_summary_ratings(html):
        parsed_ratings = None
        ratings = html.select("summary div#restaurantAvgRating")
        if ratings:
            detailed_ratings = ratings[0].attrs
            detailed_ratings.pop("id")
            parsed_ratings = {}
            for key, value in detailed_ratings.items():
                key = key[:11] # removing useless part
                parsed_ratings[key] = float(value.replace(',', '.'))
            average = float(ratings[0].span.string.strip().replace(',', '.'))
            count = int(ratings[0].div.nextSibling.string.strip("\n avis")) 
            parsed_ratings["average"] = average
            parsed_ratings["review-count"] = count
        del ratings
        return parsed_ratings


    def get_chef_name(html):
        parsed_name = None
        name = html.select("section.menuCard div.chefName")
        if name:
            parsed_name = name[0].string.strip("\nNom du chef:")
        del name
        return parsed_name


    def get_menu(html):
        parsed_menu = None
        menu = html.select("section.menuCard li.cardCategory")
        if menu:
            parsed_menu = {}
            for category in menu:
                name = category.h3.string
                meals = [meal.string for meal in category.select("div.cardCategory-itemTitle")]
                prices = category.select("div.cardCategory-itemPrice")
                if prices:
                    #prices = [price.string for price in prices]
                    prices = [float(re.sub(r"[^\d\.]", '', price.string)) for price in prices]
                else:
                    prices = [None for i in range(len(meals))]
                parsed_menu[name] = dict(zip(meals, prices))
        del menu
        return parsed_menu



    def get_description(html):
        parsed_description = None
        description = html.select("section.restaurantDescription > div")
        if description:
            parsed_description = description[0].text.split("\r\n")
        return parsed_description


    def get_drinks(html):
        parsed_drinks = None
        drinks = html.select("section.restaurantTabContent-section li.cardCategory-item")
        if drinks:
            name_price = []
            for drink in drinks:
                name = drink.find(attrs={"class": "cardCategory-itemTitle"}).string
                price = drink.find(attrs={"class": "cardCategory-itemPrice"})
                if price:
                    price = float(re.sub(r"[^\d]", '', price.string))
                else:
                    price = None
                name_price.append((name, price))
            parsed_drinks = dict(name_price)
        del drinks
        return parsed_drinks
    



    def get_gps(html):
        parsed_gps = None
        gps = html.select("div[data-gps-lat]")
        if gps:
            parsed_gps = {}
            attributes = gps[0].attrs
            parsed_gps['lat'] = float(attributes['data-gps-lat'])
            parsed_gps['lng'] = float(attributes['data-gps-lng'])
        del gps
        return parsed_gps



       
    def get_schedule(html):
        parsed_schedule = None
        schedule = html.select("div#ocAccessInfo div.moreInfo-itemInfo")
        if schedule:
            parsed_schedule = schedule[0].text.split("\r\n")
        del schedule
        return parsed_schedule


    def get_detailed_ratings(html):
        parsed_ratings = None
        ratings = html.select("div.reviewSummary")
        if ratings:
            # Award
            ratings = ratings[0]
            parsed_ratings = {}
            award = ratings.find("div", attrs={"class": "reviewSummary-distinction"})
            parsed_ratings["award"] = award.string.strip() if award else None

            # Rating list
            parsed_ratings_list = None
            ratings_list = ratings.find("ul", attrs={"class": "reviewSummary-ratingList"})
            if ratings_list:
                labels = [label.string.strip() for label in ratings_list.findAll("span", attrs={"class": "reviewSummary-rangelabel"})]
                values = [int(value.string) for value in ratings_list.findAll("span", attrs={"class": "reviewSummary-rangeCount"})]
                parsed_ratings_list = dict(zip(labels, values))
            parsed_ratings["rating-list"] = parsed_ratings_list
            
            # Detailed average ratings
            parsed_avgRatings = None
            avgRatings_labels = ratings.findAll("span", attrs={"class": "reviewSummary-avgRatingLabel"})
            avgRatings_scores = ratings.findAll("span", attrs={"class": "reviewSummary-scoreText"})
            if avgRatings_labels and avgRatings_scores:
                avgRatings_labels = [label.string for label in avgRatings_labels]
                avgRatings_scores = [float(score.string.replace(',', '.')) for score in avgRatings_scores]
                parsed_avgRatings = dict(zip(avgRatings_labels, avgRatings_scores))
            parsed_ratings["avg-ratings"] = parsed_avgRatings
            
            # Review stat
            parsed_stat = None
            stat_labels = ratings.findAll("div", attrs={"class": "reviewSummary-reviewStatLabel"})
            stat_values = ratings.findAll("div", attrs={"class": "reviewSummary-reviewStat"})
            if stat_labels and stat_values:
                stat_labels = [label.string for label in stat_labels]
                stat_values = [value.string for value in stat_values]
                parsed_stat = dict(zip(stat_labels, stat_values))
            parsed_ratings["stats"] = parsed_stat
        del ratings
        return parsed_ratings


    def get_reviews(html):
        parsed_reviews = None
        reviews = html.select("div.reviewItem")
        if reviews:
            parsed_reviews = []
            for review in reviews:
                parsed_review = {}
                
                # Profile
                profile = review.find("div", attrs={"class": "reviewItem-profileInfo"})
                if profile:
                    name = profile.contents[0].strip()
                    rank_count = profile.span.text.split('\n')
                    if len(rank_count) > 1:
                        rank = rank_count[0]
                        count = int(rank_count[1].strip("\n (avis)"))
                    else: # when there is no rank
                        rank = None
                        count = int(rank_count[0].strip("\n (avis)"))
                    parsed_review["name"] = name
                    parsed_review["rank"] = rank
                    parsed_review["count"] = count
                
                # Average rating
                avg = review.find("span", attrs={"class": "rating-ratingValue"})
                if avg:
                    avg = float(avg.string.replace(',', '.'))
                parsed_review["avg"] = avg
                
                # Detailed rating
                parsed_ratings = None
                rating_labels = review.findAll("span", attrs={"class": "reviewItem-avgRatingLabel"})
                rating_scores = review.findAll("span", attrs={"class": "reviewItem-scoreText"})
                if rating_labels and rating_scores:
                    rating_labels = [label.string for label in rating_labels]
                    rating_scores = [int(score.string) for score in rating_scores]
                    parsed_ratings = dict(zip(rating_labels, rating_scores))
                parsed_review["ratings"] = parsed_ratings

                # Date
                date = review.find("li", attrs={"class": "reviewItem-date"})
                if date:
                    date = date.string.strip("\n Datedurepas:")
                parsed_review["date"] = date

                # Comment
                comment = review.find("div", attrs={"class": "reviewItem-customerComment"})
                if comment:
                    comment = comment.string
                parsed_review["comment"] = comment
                parsed_reviews.append(parsed_review)
        del reviews
        return parsed_reviews

    parsed_html = {}
    parsed_html["currency"] = currency
    parsed_html["name"] = get_name(html)
    parsed_html["address"] = get_address(html)
    parsed_html["avg-price"] = get_price(html)
    parsed_html["summary-ratings"] = get_summary_ratings(html)
    parsed_html["chef-name"] = get_chef_name(html)
    parsed_html["menu"] = get_menu(html)
    parsed_html["description"] = get_description(html)
    parsed_html["drinks"] = get_drinks(html)
    parsed_html["gps"] = get_gps(html)
    parsed_html["schedule"] = get_schedule(html)
    parsed_html["ratings"] = get_detailed_ratings(html)
    parsed_html["reviews"] = get_reviews(html)
    return parsed_html


# Parse all restaurants
print("*** Opening file ***")
f = open("data/raw/"+sys.argv[1]+".json", 'r')
restaurants = json.load(f)
parsed_data = {}
currency = "CHF" if "ch" in sys.argv[1] else "EUR"
print("*** Parsing HTML ***")
for restaurant in restaurants:
    uri = restaurant['uri']
    html = BeautifulSoup(restaurant['html'][0], 'html.parser')
    print(uri)
    parsed_data[uri] = parse_html(html, currency)

del restaurants
f.close()

print("*** Writing to JSON file ***")
with open("data/parsed_"+sys.argv[1]+".json", 'w') as fp:
    json.dump(parsed_data, fp, ensure_ascii=False)
f.close()
fp.close()
