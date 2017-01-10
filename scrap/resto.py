import scrapy


class RestoSpider(scrapy.Spider):
    name = "resto"
    start_urls = [
        'https://www.lafourchette.com/toutes-les-villes',
        'https://www.lafourchette.ch/toutes-les-villes',
        'https://www.thefork.be/toutes-les-villes'
    ]

    def parse(self, response):
        urls = response.css('#content nav a::attr(href)').extract()
        for url in urls:
            page = response.urljoin(url.strip())
            yield scrapy.Request(page, callback=self.parse_city)
    
    def parse_city(self, response):
        urls = response.css('#content ul a::attr(href)').extract()
        for url in urls:
            page = response.urljoin(url.strip())
            yield scrapy.Request(page, callback=self.parse_listing)
            
    def parse_listing(self, response):
        url = response.css('#pagination_results .next a::attr(href)').extract_first()
        if url:
            page = response.urljoin(url.strip())
            yield scrapy.Request(page, callback=self.parse_listing)
        restos = response.css('.resultItem-name a::attr(href)').extract()
        for resto in restos:
            page = response.urljoin(resto.strip())
            yield scrapy.Request(page, callback=self.parse_resto)
            
    def parse_resto(self, response):
        yield {
            'uri': response.url,
            'html': response.css('#content').extract()
        }
