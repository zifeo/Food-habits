import scrapy,re
from bs4 import BeautifulSoup as bs

class FddbSpider(scrapy.Spider):
    name = "fddb"
    start_urls = [
        "http://fddb.info/db/fr/groupes/{}/index.html".format(group)
        for group in [
            "epice", "boissons", "congelateur", "fromages", 
            "garniture", "international", "legumineuse", "mets", 
            "pomme_de_terre", "viande", "autre", "cereale", 
            "friterie", "fruits", "huiles_et_lipides", "legumes", 
            "laitage", "poisson", "sucreries"]
        ]
    custom_settings =  {
#        "CONCURRENT_REQUESTS": 1,
#        "CONCURRENT_ITEMS": 5,
#        "CONCURRENT_REQUESTS_PER_DOMAIN": 1,
        "DUPEFILTER_DEBUG": True,
            }

    
    def parse(self, response):
        # Parse groups if there are any
        groups_b = response.css('div.leftblock h3:first-child::text').extract_first()
        if groups_b:
            #groups = response.css('div.leftblock div.standardcontent:first-child table td:first-child a::attr(href)').extract()
            groups = response.css('div.leftblock div.standardcontent:first-child table td table td:first-child a::attr(href)').extract()
            print("From",response.url,":\n(groups)\n",groups)
            for group in groups:
                group_page = response.urljoin(group.strip())
                yield scrapy.Request(group_page, callback=self.parse)
        
        # Parse producers if there are any
        producers_b = response.css('div.leftblock h4.grouppreproducthead::text').extract_first()
        if producers_b:
            nb_child = "n + 2" if groups_b else "n"
            query = 'div.leftblock > div:nth-child({}) table a::attr(href)'.format(nb_child)
            products = response.css(query).extract()
            print("From",response.url,":\n(products)\n",products)
            for product in products:
                product_page = response.urljoin(product.strip())
                yield scrapy.Request(product_page, callback=self.parse_product)
    


    def parse_product(self, response):
        nutriments = []
        regex = r"^([\d,]+)\s(\w+)$"
        
        # Extracts all nutriments information
        if response.css("div.leftblock div.itemsec2012:first-child h2::text").extract_first():
            rows = response.css('div.itemsec2012:first-child ~ div > div').extract() # selects all interesting rows
            i = 0
            while i < len(rows)-1:
                nutriment = {}
                html_name = bs(rows[i], 'html.parser')
                html_value = bs(rows[i+1], 'html.parser')
                i += 2

                # Skip vitamins and water content
                name = html_name.span.string
                if "Water" in name:
                    continue
                
                # Use same names as those already in ElasticSearch
                if name == "Valeur énergétique":
                    name = "Énergie"
                elif name == "Calorie":
                    name = "Énergie (kCal)"
                elif name == "Lipides":
                    name = "Matières grasses"
                elif name == "Sucre":
                    name = "Sucres"
            
                # Sperate value and unit
                value, unit = re.match(regex, html_value.text).groups()
                value = float(value.replace(',', '.'))

                if unit == "kcal":
                    unit = "kCal"

                nutriment['name'] = name
                nutriment['unit'] = unit
                nutriment['per_day'] = 0
                nutriment['per_portion'] = 0
                nutriment['per_hundred'] = value
                nutriment['rdi'] = 0
                
                nutriments.append(nutriment)
        
        unit = 'ml' if 'ml' in response.css("div.leftblock div.itemsec2012:first-child h2::text").extract_first() else 'g'
        yield {
                '_index': "products",
                '_type': "FDDB",
                '_source': {
                    'name': response.css("h1#fddb-headline1::text").extract_first(),
                    'unit': unit,
                    'unit_quantity': unit,
                    'unit_portion': 0,
                    'quantity': 100,
                    'nutriments': nutriments
                    }
                }
