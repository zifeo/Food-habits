import scrapy


class Recipe2Spider(scrapy.Spider):
    name = "recipe2"
    start_urls = [
        'http://cuisine.journaldesfemmes.com/toutes-les-recettes/'
    ]

    def parse(self, response):
        urls = response.css('.bu_cuisine_recette_explo_btn::attr(href)').extract()
        for url in urls:
            page = response.urljoin(url.strip() + '/preferes')
            yield scrapy.Request(page, callback=self.parse_listing)

    def parse_listing(self, response):
        url = response.css('.ccmcss_paginator_next a::attr(href)').extract_first()
        if url:
            page = response.urljoin(url.strip())
            #yield scrapy.Request(page, callback=self.parse_listing)
        recipes = response.css('.bu_cuisine_title_4 a::attr(href)').extract()
        for recipe in recipes:
            page = response.urljoin(recipe.strip())
            yield scrapy.Request(page, callback=self.parse_recipe)
            
    def parse_recipe(self, response):
        yield {
            'uri': response.url,
            'recipe': response.css('.bu_cuisine_title_1 span::text').extract_first(),
            'breadcrumb': response.css('.ccmcss_breadcrumb span::text').extract(),
            'quantity': response.css('p.bu_cuisine_title_3 span::text').extract_first(),
            'content': response.css('.bu_cuisine_ingredients').extract_first(),
        }
