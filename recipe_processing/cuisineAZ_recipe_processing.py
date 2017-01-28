#!/usr/bin/python3

import re,json

f = open("../data/cuisineAZ.json", "r")
f2 = open("../data/cuisineAZ_split_condensed.json", "w")
f3 = open("../data/cuisineAZ_split.json", "w")
recettes = json.load(f)

regex_quantity = r"\s*(?P<quantity>\d+([/\.,]\d+)?)\s?" # Matches a number, a fraction or a float (with a . or a ,)
regex_unit = r"[\s\d,\.]*(?P<unit>m[lL]|c[lL]|d[lL]|l|L|mg|g|kg|c\.\sà\ss\.|c\.\sà\sc\.|verres?|pincées?|poignées?)\s"
regex_remove_stopwords = r"(^|\s)(une?|de|petit[es]*|grand[es]*|gros[se]*|beaux?)\b"

for recette in recettes:
    content = []

    for igd in recette['content']:
        if igd and not ("Pour " in igd):
            # Replace some Unicode characters
            igd = re.sub('\u00a9', '', igd) # "copyright" sign
            igd = re.sub('\u00ae', '', igd) # "registered" sign
            igd = re.sub('\u0153', 'oe', igd)

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

            # Replace unit names by their symbols
            igd = re.sub('millilitres', 'ml', igd)
            igd = re.sub('centilitres', 'cl', igd)
            igd = re.sub('decilitres', 'dl', igd)
            igd = re.sub(r'gramme(s)?', 'g', igd)
            igd = re.sub(r'kilogramme(s)?', 'kg', igd)
            igd = re.sub(r'[lL]itre(s)?', 'l', igd)
            igd = re.sub(r'cuillères?', 'c.', igd)
            igd = re.sub(r'(c\.\s?à thé)|(c\.\s?à café)', 'c. à c.', igd)
            igd = re.sub(r'(c\.\s?à soupe)|(càs)', 'c. à s.', igd)


            igd_split = {}
            quantity = None
            unit = None
            ingredient = None

            # Extract quantity
            match = re.match(regex_quantity, igd)
            if match:
                quantity = match.group('quantity')
                igd_split['quantity'] = float(quantity.replace(',', '.'))

            # Extract unit
            match = re.match(regex_unit, igd)
            if match:
                unit = match.group('unit')
                igd_split['unit'] = unit.lower()
                
            # Convert to g or mL
            if unit and quantity:
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


            # Extract ingredient
            regex_remove_matched = r"({})|(\s?{}\s+)".format(quantity, unit)
            ingredient = re.sub(regex_remove_matched, '', igd).strip()
            ingredient = re.sub(regex_remove_stopwords, '', ingredient).strip()

            igd_split['ingredient'] = ingredient

        if igd_split:
            content.append(igd_split)

    recette['content'] = content

json.dump(recettes, f2, ensure_ascii=False)
json.dump(recettes, f3, indent=0, ensure_ascii=False)
