import scrapy,re
from bs4 import BeautifulSoup as bs

class FddbSpider(scrapy.Spider):
    """
        Scrapy spider meant to crawl all nutritional information 
        about a product from http://fddb.info
    """
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

    
    def parse(self, response):
        # Parse groups if there are any
        groups_b = response.css('div.leftblock h3:first-child::text').extract_first()
        if groups_b:
            # Follow the "groups" links 
            groups = response.css('div.leftblock div.standardcontent:first-child table td table td:first-child a::attr(href)').extract()
            for group in groups:
                group_page = response.urljoin(group.strip())
                yield scrapy.Request(group_page, callback=self.parse)
        
        # Parse producers if there are any
        producers_b = response.css('div.leftblock h4.grouppreproducthead::text').extract_first()
        if producers_b:
            nb_child = "n + 2" if groups_b else "n"
            query = 'div.leftblock > div:nth-child({}) table a::attr(href)'.format(nb_child)
            products = response.css(query).extract()
            for product in products:
                product_page = response.urljoin(product.strip())
                yield scrapy.Request(product_page, callback=self.parse_product)
    


    def parse_product(self, response):
        nutriments = []
        value_unit_re = r"^([\d,]+)\s(\w+)$"
        
        # Extracts all nutriments information
        if response.css("div.leftblock div.itemsec2012:first-child h2::text").extract_first():
            rows = response.css('div.itemsec2012:first-child ~ div > div').extract() 
            # Even rows are nutriments' names, odd rows are nutriments' values and units
            i = 0
            while i < len(rows)-1:
                nutriment = {}
                html_name = bs(rows[i], 'html.parser')
                html_value = bs(rows[i+1], 'html.parser')
                i += 2

                # Skip "Water content"
                name = html_name.span.string
                if "Water" in name:
                    continue
                
                # Rename nutriments with the names 
                # already present in our ElasticSearch (ES) instance
                if name == "Valeur énergétique":
                    name = "Énergie"
                elif name == "Calorie":
                    name = "Énergie (kCal)"
                elif name == "Lipides":
                    name = "Matières grasses"
                elif name == "Sucre":
                    name = "Sucres"
            
                # Sperate values and units
                value, unit = re.match(value_unit_re, html_value.text).groups()
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
        # Output ready to be sent to ES
        yield {
                '_index': "products",
                '_type': "FDDB",
                '_source': {
                    'name': self.clean_name(response.css("h1#fddb-headline1::text").extract_first()),
                    'unit': unit,
                    'unit_quantity': unit,
                    'unit_portion': 0,
                    'quantity': 100,
                    'nutriments': nutriments
                    }
                }

    def clean_name(self, name):
        # Removes generic words inside product name
        reg = r",\s("\
                "séché[es]*|" \
                "sèches?|" \
                "secs?|" \
                "cuit[es]*|" \
                "grain[es]*|" \
                "frais|" \
                "fra[iî]ches?|" \
                "cru[es]*|" \
                "en moyenne|" \
                "moyen(ne)?" \
                ")$"
        return re.sub(reg, '', name)
