import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import json
import codecs

CSV = 'links.csv'
HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
URL = []


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_html_2(url):
    r = requests.get(url, headers=HEADERS)
    return r

def open_list():
    with open(CSV, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])


count = 0


def get_items(url):
    html = get_html(url)
    metas = []

    soup = BeautifulSoup(html, 'lxml')

    try:
        h1 = soup.find('h1').text
        h1 = h1.strip()
    except AttributeError:
        h1 = 'ERROR'

    try:
        price = soup.find('p', class_='product-price__big').text

    except (AttributeError):
        price = 'ERROR'

    try:
        if soup.find('button', class_='buy-button button button--with-icon button--green button--medium'
                                      ' buy-button--tile ng-star-inserted'):
            aviability = 'InStock'
        else:
            aviability = 'OutOfStock'
    except AttributeError:
        aviability = 'OutOfStock'


    metas.append({
        'url': url,
        'h1': h1,
        'price': price,
        'aviability': aviability

    })

    print(url)
    return metas


def main():
    open_list()

    metas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_items, url) for url in URL]

        for future in concurrent.futures.as_completed(futures):
            metas.extend(future.result())

    with open('output.csv', 'w',  encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['url', 'h1', 'price', 'aviability'])
        writer.writeheader()
        for meta in metas:
            writer.writerow(meta)


if __name__ == '__main__':
    main()
