import csv
import requests
from bs4 import BeautifulSoup

CSV = 'links.csv'
HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
URL = []

def get_html(url):
    response = requests.get(url, headers=HEADERS)
    return response.text

def open_list():
    with open(CSV, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])

def get_items():
    open_list()
    metas = []
    for url in URL:
        html = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        try:
            h1 = soup.find('h1').text
        except AttributeError:
            h1 = 'ERROR'

        try:
            title = soup.find('title').text
        except AttributeError:
            title = 'ERROR'

        try:
            description = soup.find("meta", attrs={"name": "description"})["content"]
        except (AttributeError, KeyError):
            description = 'ERROR'

        try:
            product_id = soup.find('div', class_='tm-product-id').text.strip()
        except AttributeError:
            product_id = 'ERROR'

        metas.append({
            'h1': h1,
            'title': title,
            'description': description,
            'product_id': product_id
        })
    return metas


def main():
    metas = get_items()

    with open('output.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=['h1', 'title', 'description', 'product_id'])
        writer.writeheader()
        for meta in metas:
            writer.writerow(meta)

if __name__ == "__main__":
    main()