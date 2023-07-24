import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

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
            if line:
                URL.append(line[0])


count = 0


def get_items(url):
    html = get_html(url)
    resp = get_html_2(url)
    metas = []

    soup = BeautifulSoup(html, 'lxml')
    try:
        title = soup.find('title').text
    except AttributeError:
        title = 'ERROR'
    try:
        h1 = soup.find('h1').text
    except AttributeError:
        h1 = 'ERROR'

    try:
        product_id = soup.find('span', class_="text-basicDarkTextColor"
                                              " text-13px md:font-normal"
                                              " md:text-sm md:leading-4.5"
                                              " xl:font-normal xl:text-sm"
                                              " xl:leading-4.5 3xl:font-medium"
                                              " 3xl:text-base 3xl:leading-5.5undefined").text.replace('Код товара: ', '').strip()
    except AttributeError:
        product_id = 'ERROR'

    try:
        sku = soup.find('div', class_='mb-13px xl:mb-5px xl:last:mb-0 xl:pl-1 3xl:pl-0undefined').text
        sku = sku.replace('Артикул: ', '').strip()
    except AttributeError:
        sku = 'ERROR'

    metas.append({
        'h1': h1,
        'product_id': product_id,
        'sku': sku,
    })

    print(url, product_id, sku)
    return metas


def main():
    open_list()

    metas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = [executor.submit(get_items, url) for url in URL]

        for future in concurrent.futures.as_completed(futures):
            metas.extend(future.result())

    with open('output.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'h1', 'sku'])
        writer.writeheader()
        for meta in metas:
            writer.writerow(meta)


if __name__ == '__main__':
    main()
