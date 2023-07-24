import string
from collections import Counter


def count_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.lower().split()
    word_counter = Counter(words)
    print("Слово\tКількість")
    print("=====================")
    for word, count in word_counter.items():
        print(f"{word}\t{count}")


file_path = "example.txt"
count_words(file_path)
