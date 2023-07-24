import csv
import re


def count_characters_without_spaces(text):
    return len(text.replace(" ", "").replace(',', '').replace('.', ''))


with open('example.txt', 'r', encoding='utf-8') as text_file:
    text = text_file.read()


with open('example.csv', 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    keywords = [row[0] for row in csv_reader]


keyword_counts = {}


for keyword in keywords:
    pattern = fr'\b{re.escape(keyword)}\b'
    count = len(re.findall(pattern, text, re.IGNORECASE))
    keyword_counts[keyword] = count


characters_without_spaces = count_characters_without_spaces(text)
print("Количество символов без учета пробелов: ", characters_without_spaces)


for keyword, count in keyword_counts.items():
    if count > 0:
        print(f"{keyword}\t{count}")