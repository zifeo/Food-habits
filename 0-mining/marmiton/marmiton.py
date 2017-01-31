#!/usr/bin/python3
import re
from scrapy import Spider, Request
from bs4 import BeautifulSoup as bs

class MarmitonSpider(Spider):
    """
        This spider crawls and scraps data from all URLS given in the 'marmiton_data/urls_todo' file.
        It does a 1000 of them each time it is run, and removes the crawled URLs from that file.
        This is in order not to get blocked by captchas
    """
    name = "Marmiton"
    start_urls = ["http://www.marmiton.org/"]

    f_url = None
    urls_todo = set()
    
    def __init__(self):
    # Read the file we the remaining URLs to process
        self.f_url = open("marmiton_data/urls_todo", 'r+')
        for l in self.f_url:
            self.urls_todo.add(l.strip())


    def parse(self, response):
        # Scrap 1000 recipes each run, which is just before getting blocked by captcha
        for i in range(1000):
            url = self.urls_todo.pop()
            if url: # if not at end of file
                yield Request(url, callback=self.parse_recipe)

        return self.save_progress()
    
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
        if not ingredients:
            self.urls_todo.add(response.url)

    def save_progress(self):
    # Edit the file so that only non-processed URLs remain
        self.f_url.seek(0)
        for url in self.urls_todo:
            self.f_url.write(url + '\n')
        self.f_url.truncate()
