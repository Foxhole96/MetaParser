import csv
import requests
from bs4 import BeautifulSoup
import re

CSV = 'links.csv'
URL = []
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}


def get_pagination_links(url, session):
    if not CSV:
        print('CSV file name not specified.')
        return []

    with open(CSV, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])


    r = session.get(url, headers=HEADERS, stream=True)

    soup = BeautifulSoup(r.content, 'lxml')
    pag_list = []
    pagination = soup.find('div', class_='pagination-sunshine').find('ul').find_all('li')

    for i in pagination:
        i = i.text
        pag_list.append(i)
    pagination = int(pag_list[-1])
    pag_links = []
    for j in range(1, pagination + 1):
        pag_link = f'{url}/page/{j}'
        print(pag_link)
        pag_links.append(pag_link)


    return pag_links


def get_titles(pag_links, session):
    with open('output.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Назва', 'Телефон', 'Пошта', 'Адреса'])

        for url in pag_links:
            r = session.get(url, headers=HEADERS, stream=True)
            soup = BeautifulSoup(r.content, 'html.parser')

            full_items = soup.find_all('div', class_='item-search row js-load-business-container')

            for item in full_items:
                title = item.find('h2', class_='item-search__title mobile-hide').text.strip()
                try:
                    phone = item.find('a', attrs={"data-action": "search_page_phone_number_clicked"})['data-adtext']
                except AttributeError:
                    phone = 'NO PHONE'
                try:
                    mail = item.find('a', class_='color-black item-search__company-link').text.strip()
                except AttributeError:
                    mail = 'NO MAIL'
                try:
                    address = item.find('div', class_='item-search__text company-address icon icon-map-new').text.strip('\n ')
                    address = re.sub('\s+', ' ', address).strip()
                except AttributeError:
                    address = 'NO ADRESS'



                writer.writerow([title, phone, mail, address])

    print('Done')

url = 'https://list.in.ua/%D0%91%D1%83%D0%BA%D0%BE%D0%B2%D0%B5%D0%BB%D1%8C/%D0%A0%D0%B5%D1%81%D1%82%D0%BE%D1%80%D0%B0%D0%BD%D0%B8'
session = requests.Session()
pag_links = get_pagination_links(url, session)
get_titles(pag_links, session)
