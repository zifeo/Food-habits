#!/usr/bin/python3
import re
from scrapy import Spider,Request
from bs4 import BeautifulSoup as bs

class MarmitonNaiveSpider(Spider):
    """
        This spider crawls and scraps all recipes from the marmiton.org website.
        It can use the original website, or the Google webcache (beware some recipes might be missing)
        It is not the best way to scrap since, after ~1000 requests, we got blocked by captcas for having
        too many connections.
        Take a look rather at files marmiton_urls.py and marmiton.py
    """
    name = "marmiton_naive"

    start_urls = [
            "http://www.marmiton.org/recettes/recettes-index.aspx?letter={}".format(letter)
         for letter in  [
             'A','B','C','D','E','F','G','H','I','J','K','L',
             'M','N','O','P','Q','R','S','T','V','W','X','Y']
         ]


    def parse(self, response):
        # Visit all ingredient links
        ingredients = response.css("div#m_page div.m_bloc_cadre div.content li a::attr(href)").extract() # or a::text
        for igrd in ingredients:
            igrd_url = response.urljoin(igrd.strip())
            yield Request(igrd_url, callback=self.parse_ingredient)


    def parse_ingredient(self, response):
        # Retrieve all recipes' links on the page for the given ingredient
        recipes = response.css("div.content ul.m-lsting-recipe li a::attr(href)").extract()
        for recipe in recipes:
            recipe_page = response.urljoin(recipe.strip())
            # Skip recipesonly shown as videos
            if not ("video" in recipe_page):
                yield Request(recipe_page, callback=self.parse_recipe)

        next_page = response.css("div.content a.m-btn-next::attr(href)").extract_first()
        if (next_page):
            next_page = response.urljoin(next_page.strip())
            yield Request(next_page, callback=self.parse_ingredient)


    def parse_recipe(self, response):
        # Scrap the recipe
        ingredients_html = bs(response.css('div.m_content_recette_ingredients').extract_first(), 'html.parser')
        ingredients = re.sub(r"[\r\n]", '', ingredients_html.text).split('-')
        yield {
            'uri': response.url,
            'title': response.css('div.m_bloc_cadre h1.m_title span.fn::text').extract_first(),
            'breadcrumb': response.css('div.m_content_recette_breadcrumb::text').extract_first().split('-')[0].strip(),
            'quantity': re.sub(r"[^\d]", '', response.css('div.m_content_recette_ingredients > span::text').extract_first()),
            'ingredients': [ingredients[i].strip() for i in range(1, len(ingredients))]
        }
