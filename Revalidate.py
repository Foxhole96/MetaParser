import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures
import time

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
    resp = get_html_2(url)
    metas = []

    soup = BeautifulSoup(html, 'lxml')
    time.sleep(5)





    print(url)
    return metas


def main():
    open_list()

    metas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(get_items, url) for url in URL]

        for future in concurrent.futures.as_completed(futures):
            metas.extend(future.result())



if __name__ == '__main__':
    main()
