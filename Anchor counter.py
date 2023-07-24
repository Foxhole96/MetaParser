import pandas as pd

df = pd.read_csv('example.csv')
word_phrases = df.iloc[:, 0].tolist()
word_count = {}

for phrase in word_phrases:
    if phrase in word_count:
        word_count[phrase] += 1
    else:
        word_count[phrase] = 1


print("Анкор\tКількість")
for phrase, count in word_count.items():
    print(f"{phrase}\t{count}")