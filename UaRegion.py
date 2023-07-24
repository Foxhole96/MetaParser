import csv
import requests
from bs4 import BeautifulSoup
import math
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
    pagination = soup.find_all('div', class_='col-md-12 text-center')
    pagination = pagination[-1].text
    count = pagination.split(':')[-1].strip()
    pagination_count = math.ceil(int(count) / 20)

    for link in range(1, pagination_count + 1):
        pag_list.append(f'{url}?start_page={link}')
    print(pag_list)

    return pag_list


def get_links(pag_list, session):
    error = 'ERROR'
    company_links = []

    with open('output.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Назва', 'Адреса', 'Телефон 1', 'Телефон 2', 'Телефон 3', 'Пошта', 'Сайт', 'Опис'])

        for url in pag_list:
            r = session.get(url, headers=HEADERS, stream=True)
            soup = BeautifulSoup(r.content, 'lxml')

            links_blocks = soup.find_all('div', class_='cart-company-lg__title ui-title-inner')

            for links in links_blocks:
                company_link = links.find('a', class_='').get('href')
                company_link = f'{host}{company_link}'
                company_links.append(company_link)

            company_blocks = soup.find_all('div', class_='row p-3 p-md-4')

            for i in range(len(company_links)):
                try:
                    company_link = company_links[i]
                except IndexError:
                    company_link = error
                company_block = company_blocks[i]

                try:
                    company_title = company_block.select_one('.cart-company-lg__title a').text.strip()
                except AttributeError:
                    company_title = error
                try:
                    address = company_block.select_one(
                        '.cart-company-lg__list li:nth-of-type(1) .cart-company-lg__list-link').text.strip()
                except AttributeError:
                    address = error
                try:
                    phone_numbers = [a.text.strip() for a in
                                     company_block.select('.cart-company-lg__list li:nth-of-type(2) a')]
                except AttributeError:
                    phone_numbers = [error]
                if len(phone_numbers) < 3:
                    phone_numbers += [error] * (3 - len(phone_numbers))
                try:
                    email = company_block.select_one('.cart-company-lg__list li:nth-of-type(3) a').text.strip()
                    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                        site = email.strip()
                        email = error
                    else:
                        site = error
                except AttributeError:
                    email = error
                    site = error

                try:
                    company_activity_block = company_block.select_one('.col-12.mt-mb-0')
                    if company_activity_block:
                        company_activity = company_activity_block.find_all(text=True, recursive=False)
                        company_activity = ' '.join(company_activity).replace('Продукція, послуги ', '').strip()
                    else:
                        print('company_activity_block is None')
                        company_activity = 'ERROR'
                except AttributeError:
                    company_activity = 'ERROR'


                writer.writerow([company_title, address, phone_numbers[0], phone_numbers[1], phone_numbers[2], email, site, company_activity])

            company_links.clear()


host = 'https://www.ua-region.com.ua'
url = 'https://www.ua-region.com.ua/te-0/search-full.php/q-%D0%BC%D1%8F%D1%81%D0%BE'
session = requests.Session()

pag_list = get_pagination_links(url, session)
get_links(pag_list, session)