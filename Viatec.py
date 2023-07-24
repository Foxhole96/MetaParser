import requests
from bs4 import BeautifulSoup
import csv

CSV = 'links.csv'

HOST = 'https://viatec.ua/'
HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 '
                  'Safari/537.36 '
}
URL = []


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def open_list():
    with open('new_links.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])


def get_items():
    open_list()
    iter = 0
    metas = []

    for i in URL:

        get_html(i)
        html = get_html(i)
        iter += 1

        def get_meta(html):
            soup = BeautifulSoup(html, 'lxml')
            loc = soup.find('span', class_='html-tag').get_text()
            items = [{
                'LOC': loc

            }]

            return items

        print('Сторінка №', iter)
        metas.extend(get_meta(html.text))

    return metas


get_items = get_items()


def save_doc(get_items, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='^')
        writer.writerow(
            ['URL'])
        for item in get_items:
            writer.writerow([item['LOC']])


try:
    save_doc(get_items, CSV)

except Exception as ex:
    print(ex)
finally:
    print('Завершено')
