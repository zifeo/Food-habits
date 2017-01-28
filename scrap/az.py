import scrapy


class Recipe3Spider(scrapy.Spider):
    name = "recipe3"
    download_delay = 0.5
    start_urls = [
        "http://www.cuisineaz.com/recettes/recherche_v2.aspx?recherche={}".format(r)
        for r in [
            'bases',
            'aperitifs',
            'entrees',
            'plats',
            'desserts',
            'accompagnements',
            'recettes-pas-cheres',
            'viandes',
            'poissons',
            'legumes',
            'fruits',
            'fromages',
            'repas',
            'cher',
            'farine',
            'sucre',
            'facile',
        ]
        ]

    def parse(self, response):
        url = response.css('.pagination-next a::attr(href)').extract_first()
        if url:
            page = response.urljoin(url.strip())
            yield scrapy.Request(page, callback=self.parse)
        recipes = response.css('#titleRecette a::attr(href)').extract()
        for recipe in recipes:
            page = response.urljoin(recipe.strip())
            yield scrapy.Request(page, callback=self.parse_recipe)

    def parse_recipe(self, response):
        yield {
            'uri': response.url,
            'recipe': response.css('.recipe_main h1::text').extract_first(),
            'breadcrumb': [],
            'quantity': response.css('#ctl00_ContentPlaceHolder_LblRecetteNombre::text').extract_first(),
            'content': response.css('.recipe_ingredients ul').extract_first()
        }

