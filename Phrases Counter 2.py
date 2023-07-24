import csv


def check_sentence(sentence):
    punctuation = ['.', ',', '!', '?', ':', ';', '"', '`', ')', '(', '“', '”', '-', '—']
    num_punctuations = 0
    for char in sentence:
        if char in punctuation:
            num_punctuations += 1

    if num_punctuations > 1:
        return None

    if any(char in punctuation for char in sentence):
        if sentence[-1] in punctuation:

            return sentence[:-1]
        else:

            for i, char in enumerate(sentence):
                if char in punctuation:
                    continue
    else:

        return sentence

with open('example.txt', 'r', encoding='utf-8') as f:
    text = f.read().lower()

with open('stopwords.csv', 'r', encoding='utf-8') as f:
    stopwords = set(line.strip() for line in f)

punctuation = ['.', ',', '!', '?', ':', ';', '"', '`', ')', '(', '“', '”']

words = [word.strip(' ') for word in text.split()]
one_word_counts = {}

num_punctuations = 0
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
        checked_sentence = check_sentence(two_word)
        if checked_sentence:
            two_word_counts[checked_sentence] = two_word_counts.get(checked_sentence, 0) + 1

with open('two_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(two_word_counts.items()):
        writer.writerow([word, count])

three_word_counts = {}

for i in range(len(words) - 2):
    if words[i] not in stopwords and words[i+2] not in stopwords:
        three_word = ' '.join(words[i:i+3])
        checked_sentence = check_sentence(three_word)
        if checked_sentence:
            three_word_counts[checked_sentence] = three_word_counts.get(checked_sentence, 0) + 1

with open('three_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(three_word_counts.items()):
        writer.writerow([word, count])

four_word_counts = {}

for i in range(len(words) - 3):

    if words[i] not in stopwords and words[i + 3] not in stopwords:
        four_word = ' '.join(words[i:i + 4])
        checked_sentence = check_sentence(four_word)
        if checked_sentence:
            four_word_counts[checked_sentence] = four_word_counts.get(checked_sentence, 0) + 1

with open('four_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(four_word_counts.items()):
        writer.writerow([word.strip(), count])

five_word_counts = {}

for i in range(len(words) - 4):

    if words[i] not in stopwords and words[i + 4] not in stopwords:
        five_word = ' '.join(words[i:i + 5])
        checked_sentence = check_sentence(five_word)
        if checked_sentence:
            five_word_counts[checked_sentence] = five_word_counts.get(checked_sentence, 0) + 1

with open('five_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(five_word_counts.items()):
        writer.writerow([word.strip(), count])

six_word_counts = {}


for i in range(len(words) - 5):

    if words[i] not in stopwords and words[i + 5] not in stopwords:
        six_word = ' '.join(words[i:i + 6])
        checked_sentence = check_sentence(six_word)
        if checked_sentence:
            six_word_counts[checked_sentence] = six_word_counts.get(checked_sentence, 0) + 1

with open('six_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['word', 'count'])
    for word, count in sorted(five_word_counts.items()):
        writer.writerow([word.strip(), count])

