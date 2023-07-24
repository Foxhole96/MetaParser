import csv
import json


with open('links_input.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    items = []
    for row in reader:
        items.append(row)

result = {'items': items}

with open('links.json', 'w') as jsonfile:
    json.dump(result, jsonfile)