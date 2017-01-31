#!/usr/bin/python3
import re
from scrapy import Spider, Request
from bs4 import BeautifulSoup as bs

class MarmitonSpider(Spider):
    name = "Marmiton_url"
    start_urls = [
        "http://www.marmiton.org/recettes/recettes-index.aspx?letter={}".format(letter)
        for letter in  [
            'A','B','C','D','E','F','G','H','I','J','K','L',
            'M','N','O','P','Q','R','S','T','V','W','X','Y']
        ]
    f = None
    

    def __init__(self):
        self.f = open("marmiton_data/urls_all", 'w')


    def parse(self, response):
        # Go over each ingredient
        ingredients = response.css("div#m_page div.m_bloc_cadre div.content li a::attr(href)").extract()
        for igrd in ingredients:
            igrd_url = response.urljoin(igrd.strip())
            yield Request(igrd_url, callback=self.get_urls)


    def get_urls(self, response):
        # Gather URLs to all recipes per ingredient category
        recipes = response.css("div.content ul.m-lsting-recipe li a::attr(href)").extract()
        for recipe in recipes:
            url = response.urljoin(recipe.strip())
            if not ("video" in url): # Do not save video recipes
                self.f.write(url + '\n')

        next_page = response.css("div.content a.m-btn-next::attr(href)").extract_first()
        if (next_page):
            next_page = response.urljoin(next_page.strip())
            yield Request(next_page, callback=self.get_urls)
