#!/usr/bin/python3

import re,json,os
from bs4 import BeautifulSoup as bs

f = open("../data/cuisineAZ.json", "r")
f2 = open("../data/cuisineAZ2.json", "w")

rs = json.load(f)

for r in rs:
    html = bs(r['content'], 'html.parser')
    igs = html.select('span')
    r['content'] = [i.string.strip() if (i.string) else i.string for i in igs]


json.dump(rs, f2, indent=0, ensure_ascii=False)

# Replace original file
os.system("mv ../data/cuisineAZ.json ../data/cuisineAZ_not_parsed.json")
os.system("mv ../data/cuisineAZ2.json ../data/cuisineAZ.json")
