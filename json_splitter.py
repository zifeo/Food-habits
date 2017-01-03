#!/usr/bin/python3

import json
f = open("com.json", 'r')
rs = json.load(f)

k = 0
for i in range(5):
    r = []
    for j in range(2191):
        if k == 0:
            print(type(rs[k]))
        r.append(rs[k])
        k += 1
    with open("com"+str(i)+".json", 'w') as fp:
        json.dump(r, fp, ensure_ascii=False)

