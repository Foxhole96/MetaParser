import requests
import json
from bs4 import BeautifulSoup
import concurrent.futures

HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}

with open('links.json', 'r') as f:
    data = json.load(f)

results = []


def parse_page(item):
    item_id = item['id']
    url = item['url']
    url = url.split('?')[0]

    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'lxml')
    title = soup.find('h1')

    try:
        price = soup.find('span', attrs={"itemprop": "price"})["content"]

    except (AttributeError, KeyError):
        price = 'ERROR'

    try:
        if soup.find('a', class_='add btn-add-green'):
            aviability = 'InStock'
        else:
            aviability = 'OutOfStock'
    except AttributeError:
        aviability = 'OutOfStock'


    result = {
        'id': item_id,
        'title': title.get_text(strip=True) if title else None,
        'price': price,
        'aviability': aviability
    }

    print(url)

    return result


with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(parse_page, item) for item in data['items']]

    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            results.append(result)
        except Exception as e:
            print(f'Ошибка при обработке элемента: {e}')

with open('output_brain.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)