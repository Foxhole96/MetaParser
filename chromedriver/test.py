import csv

all_product_links = []

with open('links.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)

    for line in reader:
        all_product_links.append(line[0])

print(all_product_links)