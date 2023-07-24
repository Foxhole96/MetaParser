import csv

with open('example.txt', 'r', encoding='utf-8') as f:
    text = f.read().lower()

with open('stopwords.csv', 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f)

words = [word.strip(' ,()".\'*#!%+-=:;”“»«?') for word in text.split()]
one_word_counts = {}

for word in words:
    if word and word not in stopwords:
        one_word_counts[word] = one_word_counts.get(word, 0) + 1

with open('one_word.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(one_word_counts.items()):
        writer.writerow([word, count])


two_word_counts = {}


for i in range(len(words) - 1):
    if words[i] not in stopwords and words[i+1] not in stopwords:
        two_word = ' '.join(words[i:i+2])
        two_word_counts[two_word] = two_word_counts.get(two_word, 0) + 1


with open('two_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(two_word_counts.items()):
        writer.writerow([word, count])


three_word_counts = {}


for i in range(len(words) - 2):
    if words[i] not in stopwords and words[i+2] not in stopwords:
        three_word = ' '.join(words[i:i+3])
        three_word_counts[three_word] = three_word_counts.get(three_word, 0) + 1


with open('three_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(three_word_counts.items()):
        writer.writerow([word, count])

four_word_counts = {}


for i in range(len(words) - 3):

    if words[i] not in stopwords and words[i + 3] not in stopwords:
        four_word = ' '.join(words[i:i + 4])
        four_word_counts[four_word] = four_word_counts.get(four_word, 0) + 1

with open('four_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(four_word_counts.items()):
        writer.writerow([word.strip(), count])