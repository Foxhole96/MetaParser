import csv

CSV ='example.csv'
URL = []

with open(CSV, 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        URL.append(line[0])

for i in URL:
    i = i.capitalize()
    print(i)