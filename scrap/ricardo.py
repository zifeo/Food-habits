import scrapy


class RicardoSpider(scrapy.Spider):
    name = "ricardo"
    start_urls = [
        "https://www.ricardocuisine.com/recettes/{}".format(cat)
        for cat in  ["plats-principaux", "entrees", "desserts"]
        ]

    
    def parse(self, response):
        subcats = response.css('li.item div.desc a::attr(href)').extract()
        for subcat in subcats:
            subcat_page = response.urljoin(subcat.strip())
            yield scrapy.Request(subcat_page, callback=self.parse_subcat)
    

    def parse_subcat(self, response):
        next_page = response.css("div.pagination li.nextPage a::attr(href)").extract_first()
        recipes = response.css("ul.item-list li.item div.desc a.parent::attr(href)").extract()
        for recipe in recipes:
            recipe_page = response.urljoin(recipe.strip())
            yield scrapy.Request(recipe_page, callback=self.parse_recipe)

        if (next_page):
            next_page = response.urljoin(next_page.strip())
            yield scrapy.Request(next_page, callback=self.parse_subcat)


    def parse_recipe(self, response):
        yield {
            'uri': response.url,
            'title': response.css('div.recipe-content h1::text').extract_first(),
            'breadcrumb': [b.strip() for b in response.css('div.tags a::text').extract() if len(b.strip())],
            'quantity': response.css('div.recipe-content dd:last-child::text').extract_first(),
            'ingredients': response.css('form#formIngredients li span::text').extract()
        }

