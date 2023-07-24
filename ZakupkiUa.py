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

    soup = BeautifulSoup(r.content, 'html.parser')
    pag_list = []
    pagination = soup.find('ul', class_='pagination').find_all('li')

    for i in pagination:
        i = i.text
        pag_list.append(i)
    pagination = int(pag_list[-2])
    pag_links = []
    for j in range(1, pagination + 1):
        pag_link = f'{url}?page={j}'
        print(pag_link)
        pag_links.append(pag_link)

    return pag_links


def get_links(pag_links, session):
    all_links = []
    for url in pag_links:
        r = session.get(url, headers=HEADERS, stream=True)
        soup = BeautifulSoup(r.content, 'html.parser')

        tender_links = soup.find_all('a', class_='tender-name')

        for link in tender_links:
            link = link.get('href')
            print(link)
            all_links.append(link)

    return all_links


def get_titles(all_links, session):
    with open('output.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Назва Тендера', 'Ціна', 'Статус', 'Кількість продукції',
                         'Організація', 'Поштовий індекс', 'Регіон', 'Нас. Пункт', 'Адреса', "Ім'я",
                         'Телефон',
                         'Email', 'Компанія (П)', 'Ціна (П)', 'Код ЄДРПОУ (П)', 'Адреса (П)',
                         'Імя (П)', 'Телефон (П)', 'Email (П)'])

        for url in all_links:
            r = session.get(url, headers=HEADERS, stream=True)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                h1 = soup.find('h1', class_='Tender-name ukr_version').text.strip().lower()
            except AttributeError:
                h1 = 'ERROR'
            try:
                result_tender_price = soup.find('span', class_='result-tender-content-price').text.strip().lower()
                result_tender_price = re.sub('\s+', ' ', result_tender_price).strip()
            except AttributeError:
                result_tender_price = 'ERROR'
            try:
                status = soup.find('span', class_='allowed-status').text.strip().lower().replace(',', '; ')
            except AttributeError:
                status = 'ERROR'
            try:
                count_of_production = soup.find('p', class_='quantity-items').text.strip().lower().replace(',', '; ')
            except AttributeError:
                count_of_production = 'ERROR'
            try:
                oranization_name = soup.find('td', class_='item-procuringEntity.name').text.strip().replace(',', '; ')
            except AttributeError:
                oranization_name = 'ERROR'
            try:
                postal_code = soup.find('span', class_='postal_code').text.strip().lower().replace(',', '; ')
            except AttributeError:
                postal_code = 'ERROR'
            try:
                country = soup.find('span', class_='country').text.strip().replace(',', '; ')
            except AttributeError:
                country = 'ERROR'
            try:
                region = soup.find('span', class_='region').text.strip().replace(',', '; ')
            except AttributeError:
                region = 'ERROR'
            try:
                locality = soup.find('span', class_='locality').text.strip().replace(',', '; ')
            except AttributeError:
                locality = 'ERROR'
            try:
                street = soup.find('span', class_='street').text.strip().replace(',', '; ')
            except AttributeError:
                street = 'ERROR'
            try:
                name = soup.find('span', class_='ukr_version').text.strip().replace(',', '; ')
            except AttributeError:
                name = 'ERROR'
            try:
                phone = soup.find('div',
                                  class_='Panel-block'
                                         ' secondPanelBlock').find('span',
                                                                   class_='contactPhone').text.replace(',', '; ')
            except AttributeError:
                phone = 'ERROR'

            try:
                winner_company_name = soup.find('h3', class_='TOV-name').text.strip()
            except AttributeError:
                winner_company_name = 'ERROR'
            try:
                winner_price = soup.find('span', class_='result-tender-content-price').text.replace('UAH', '').strip()
            except AttributeError:
                winner_price = 'ERROR'
            try:
                winner_info_table = soup.find('table', class_='contact-info-container clean-table tender-generalInfo')
                if winner_info_table:
                    w_edrpu_code = winner_info_table.find('th', string='Код ЄДРПОУ').find_next('td').text.strip()
                    w_postal_adress = winner_info_table.find('th', string='Поштова адреса').find_next('td').text.strip()
                    w_name = winner_info_table.find('th', string="Ім'я").find_next('td').text.strip()
                    w_phone = winner_info_table.find('th', string='Телефон').find_next('td').text.strip()
                    w_email = winner_info_table.find('th', string='Ел. пошта').find_next('td').text.strip()
                else:
                    w_edrpu_code = 'ERROR'
                    w_postal_adress = 'ERROR'
                    w_name = 'ERROR'
                    w_phone = 'ERROR'
                    w_email = 'ERROR'
            except AttributeError:
                winner_info_table = 'ERROR'

            # try:
            #     phone_numbers = [a.text.strip() for a in
            #                      company_block.select('.cart-company-lg__list li:nth-of-type(2) a')]
            # except AttributeError:
            #     phone_numbers = [error]
            # if len(phone_numbers) < 3:
            #     phone_numbers += [error] * (3 - len(phone_numbers))

            try:
                emails = soup.find('div', class_='Panel-block secondPanelBlock').find_all('td')

                email = emails[-1].text
                if '@' not in email:
                    email = 'ERROR'

            except AttributeError:
                email = 'ERROR'

            print(phone)

            writer.writerow([url, h1, result_tender_price, status, count_of_production, oranization_name, postal_code,
                             region, locality, street, name, phone, email, winner_company_name,
                              winner_price, w_edrpu_code, w_postal_adress, w_name, w_phone, w_email])




            print(url)
    print('Done')


url = 'https://zakupki.com.ua/ryba-ta-moreprodukty'
session = requests.Session()

pag_links = get_pagination_links(url, session)
all_links = get_links(pag_links, session)
get_titles(all_links, session)
