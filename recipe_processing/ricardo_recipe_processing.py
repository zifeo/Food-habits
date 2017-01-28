#!/usr/bin/python3

import re,json
from elasticsearch import Elasticsearch
from elasticsearch import helpers as eshelper

f = open("../data/ricardo.json", "r")

recipes = json.load(f)

regex_quantity = r"\s*(?P<quantity>\d+([/\.,]\d+)?)\s*?" # Matches a number, a fraction or a float (with a . or a ,)
regex_unit = r"[\s\d,\.]*(?P<unit>m[lL]|c[lL]|d[lL]|l|L|mg|g|kg|c\.\sà\ss\.|c\.\sà\sc\.|verre|pincée|poignée)\s"
regex_remove_stopwords = r"(^|\s)(une?|de|petit[es]*|grand[es]*|gros[se]*|beaux?)\b"

elasticsearch_entries = []
for recipe in recipes:
    ingredients = []
    fmt = {
            '_index': 'recipes',
            '_type': 'ricardo',
            }
    r = {
            'name': recipe['title'].strip(),
            'ingredients': []
            }


    nb_ppl = 1
    if recipe['quantity']:
        m = re.match(r"(^\d)", recipe['quantity'])
        if m:
            nb_ppl = int(m.group(0))


    for igd in recipe['ingredients']:
        if igd and not (igd == "ou"):
            # Replace some unicode symbols
            igd = re.sub('\u0153', 'oe', igd)
            igd = re.sub('\t', ' ', igd) 
            
            # Replace fractions by floats
            igd = re.sub('(\u00bc)|(1/4)', '0.25', igd)
            igd = re.sub('(\u00bd)|(1/2)', '0.5', igd)
            igd = re.sub('(\u00be)|(3/4)', '0.75', igd)
            igd = re.sub('1/3', '0.33', igd)
            igd = re.sub('2/3', '0.66', igd)
            igd = re.sub('1/8', '0.125', igd)
            igd = re.sub('3/8', '0.375', igd)
            igd = re.sub('5/8', '0.625', igd)
            igd = re.sub('1/5', '0.2', igd)
            igd = re.sub('2/5', '0.4', igd)
            igd = re.sub('3/5', '0.6', igd)
            igd = re.sub('4/5', '0.8', igd)
            igd = re.sub('5/6', '0.83', igd)
            igd = re.sub('7/8', '0.875', igd)

            # Replace/remove some patterns
            igd = re.sub(r"\s*\([\s\w\\d\.,/]+\)", '', igd)   # remove parenthesis blocks
            igd = re.sub('millilitres', 'ml', igd)
            igd = re.sub('centilitres', 'cl', igd)
            igd = re.sub('decilitres', 'dl', igd)
            igd = re.sub(r'gramme(s)?', 'g', igd)
            igd = re.sub(r'kilogramme(s)?', 'kg', igd)
            igd = re.sub(r'[lL]itre(s)?', 'l', igd)
            igd = re.sub(r'cuillères?', 'c.', igd)
            igd = re.sub(r'c\.\s?à thé', 'c. à c.', igd)
            igd = re.sub(r'(c\.\s?à soupe)|(càs)', 'c. à s.', igd)
            igd = re.sub(r"[lL]itre(s)?", 'l', igd)
            igd = re.sub(r"\b(verres)\b", 'verre', igd)
            igd = re.sub(r"\b(poignées)\b", 'poignée', igd)
            igd = re.sub(r"\b(pincées)\b", 'pincée', igd)


            igd_split = {}
            quantity = None
            unit = None
            ingredient = None

            # Extract quantity
            match = re.match(regex_quantity, igd)
            if match:
                quantity = match.group('quantity')
                igd_split['quantity'] = float(quantity.replace(',', '.'))
            else:
                continue

            # Extract unit
            match = re.match(regex_unit, igd)
            if match:
                unit = match.group('unit')
                igd_split['unit'] = unit.lower()
            else:
                igd_split['unit'] = unit


            # Convert to g or mL
            if quantity and unit:
                if igd_split['unit'] == "mg":
                    igd_split['quantity'] /= 1000
                    igd_split['unit'] = "g"

                elif igd_split['unit'] == "kg":
                    igd_split['quantity'] *= 1000
                    igd_split['unit'] = "g"

                elif igd_split['unit'] == "cl":
                    igd_split['quantity'] *= 10
                    igd_split['unit'] = "ml"
                
                elif igd_split['unit'] == "dl":
                    igd_split['quantity'] *= 100
                    igd_split['unit'] = "ml"
                
                elif igd_split['unit'] == "l":
                    igd_split['quantity'] *= 1000
                    igd_split['unit'] = "ml"

                elif igd_split['unit'] == "c. à c.":
                    igd_split['quantity'] *= 5
                    igd_split['unit'] = "ml"

                elif igd_split['unit'] == "c. à s.":
                    igd_split['quantity'] *= 15
                    igd_split['unit'] = "ml"

                elif igd_split['unit'] == "verre":
                    igd_split['quantity'] *= 300
                    igd_split['unit'] = "ml"

                elif igd_split['unit'] == "poignée":
                    igd_split['quantity'] *= 50
                    igd_split['unit'] = "g"

                elif igd_split['unit'] == "pincée":
                    igd_split['quantity'] *= 3
                    igd_split['unit'] = "g"


            igd_split['quantity'] /= nb_ppl

            # Extract ingredient
            regex_remove_matched = r"({})|(\s?{}\s+)".format(quantity, unit)
            ingredient = re.sub(regex_remove_matched, '', igd).strip()
            ingredient = re.sub(regex_remove_stopwords, '', ingredient).strip()

            igd_split['content'] = ingredient

            
        if igd_split:
            r['ingredients'].append(igd_split)
    

    fmt['_source'] = r
    elasticsearch_entries.append(fmt)

client = Elasticsearch(hosts='http://')
eshelper.bulk(client, elasticsearch_entries)
