#!/usr/bin/python3
import re
from scrapy import Spider,Request
from bs4 import BeautifulSoup as bs

class MarmitonSpider(Spider):
    """
        This spider crawls and scraps all recipes from the marmiton.org website.
        It can use the original website, or the Google webcache (beware some recipes might be missing)
        It is not the best way to scrap since, after ~1000 requests, we got blocked by captcas for having
        too many connections.
        Take a look rather at files marmiton_urls.py and marmiton.py
    """
    name = "Marmiton_all"

    google = False
    google_cache = "https://webcache.googleusercontent.com/search?q=cache:"
    cache_params = "&num=1&strip=0&vwsrc=0"
    
    ## Do letter by letter otherwise blocked too quickly by captchas
    #letter = "C"
    #start_urls = ["http://www.marmiton.org/recettes/recettes-index.aspx?letter=" + letter] 
    #start_urls = [google_cache + "http://www.marmiton.org/recettes/recettes-index.aspx?letter=A" + cache_params]
    start_urls = [
         #(google_cache + "http://www.marmiton.org/recettes/recettes-index.aspx?letter={}" + cache_parameters).format(letter)
            "http://www.marmiton.org/recettes/recettes-index.aspx?letter={}".format(letter)
         for letter in  [
             'A','B','C','D','E','F','G','H','I','J','K','L',
             'M','N','O','P','Q','R','S','T','V','W','X','Y']
         ]

    scraped_urls = set()
    f_url = None
    
    def __init__(self):
        self.f_url = open("marmiton_data/urls", 'r+')
        for l in self.f_url:
            self.scraped_urls.add(l)


    def parse(self, response):
        ## Use this to scrap all recipes for all ingredients starting with a given letter
        ingredients = response.css("div#m_page div.m_bloc_cadre div.content li a::attr(href)").extract() # or a::text
        for igrd in ingredients:
            if self.google:
                igrd_url = self.google_cache + response.urljoin(igrd.strip()) + self.cache_params
            else:
                igrd_url = response.urljoin(igrd.strip())
            yield Request(igrd_url, callback=self.parse_ingredient)

        ## Or use this to scrap all recipes for a given ingredient starting with a given letter
        #igrd = ingredients[1]
        #if self.google:
        #    igrd_url = self.google_cache + response.urljoin(igrd.strip()) + self.cache_params
        #else:
        #    igrd_url = response.urljoin(igrd.strip())
        #yield Request(igrd_url, callback=self.parse_ingredient)
    

    def parse_ingredient(self, response):
        recipes = response.css("div.content ul.m-lsting-recipe li a::attr(href)").extract()
        for recipe in recipes:
            if self.google:
                recipe_page = self.google_cache + response.urljoin(recipe.strip()) + self.cache_params
            else:
                recipe_page = response.urljoin(recipe.strip())
            if not ("video" in recipe_page) and not (recipe_page in self.scraped_urls):
                yield Request(recipe_page, callback=self.parse_recipe)

        next_page = response.css("div.content a.m-btn-next::attr(href)").extract_first()
        if (next_page):
            if self.google:
                next_page = self.google_cache + response.urljoin(next_page.strip()) + self.cache_params
            else:
                next_page = response.urljoin(next_page.strip())
            yield Request(next_page, callback=self.parse_ingredient)


    def parse_recipe(self, response):
        ingredients_html = bs(response.css('div.m_content_recette_ingredients').extract_first(), 'html.parser')
        ingredients = re.sub(r"[\r\n]", '', ingredients_html.text).split('-')
        yield {
            'uri': response.url,
            'title': response.css('div.m_bloc_cadre h1.m_title span.fn::text').extract_first(),
            'breadcrumb': response.css('div.m_content_recette_breadcrumb::text').extract_first().split('-')[0].strip(),
            'quantity': re.sub(r"[^\d]", '', response.css('div.m_content_recette_ingredients > span::text').extract_first()),
            'ingredients': [ingredients[i].strip() for i in range(1, len(ingredients))]
        }
        if ingredients:
            self.scraped_urls.add(response.url)
            self.f_url.write(response.url + '\n')

