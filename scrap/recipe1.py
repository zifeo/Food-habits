import scrapy


class Recipe1Spider(scrapy.Spider):
    name = "recipe1"
    start_urls = [
        'http://www.750g.com/recettes_aperitifs.htm',
        'http://www.750g.com/recettes_entrees.htm',
        'http://www.750g.com/recettes_plats.htm',
        'http://www.750g.com/recettes_soupes_et_potages.htm',
        'http://www.750g.com/recettes_gateaux.htm',
        'http://www.750g.com/recettes_desserts.htm'
    ]

    def parse(self, response):
        urls = response.css('a.c-pagination__link::attr(href)').extract()
        for url in urls:
            page = response.urljoin(url.strip())
            yield scrapy.Request(page, callback=self.parse)

        recipes = response.css('a.u-link-wrapper::attr(href)').extract()
        for recipe in recipes:
            page = response.urljoin(recipe.strip())
            yield scrapy.Request(page, callback=self.parse_recipe)
            
    def parse_recipe(self, response):
        yield {
            'uri': response.url,
            'recipe': response.css('h1.c-article__title::text').extract_first(),
            'breadcrumb': [b.strip() for b in response.css('.c-breadcrumb span::text').extract() if len(b.strip())],
            'quantity': response.css('h2.u-title-arvo-20-uppercase .yield::text').extract_first(),
            'content': response.css('.c-recipe-ingredients').extract_first(),
            'recipe2': response.css('h1.c-page-article__title::text').extract_first(),
            'content2': response.css('.c-diapo__text').extract_first(),
        }

