import csv
import time
import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import winsound
from Functions import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://001.com.ua/taymery-sutochnye-nedelnye-godovye-astronomicheskie'
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(HEADERS)

driver = webdriver.Chrome()

def play_sound():
    frequency = 500
    duration = 1000
    winsound.Beep(frequency, duration)


def get_cat_html_ru():
    ua_links_list = []
    data = []
    data_ua = []

    try:
        host = 'https://001.com.ua'
        driver.get(url=url)
        time.sleep(3)
        driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul[2]/li[1]/a/span[1]').click()
        time.sleep(2)
        with open('index.html', 'w', encoding='utf-8-sig') as f:
            f.write(driver.page_source)

        with open('index.html', encoding='utf-8-sig') as f:
            src = f.read()
        soup = BeautifulSoup(src, 'lxml')
        try:
            pagination_links = soup.find('ul', class_='pagination').find_all('li')
            pag_links_count = int(pagination_links[-2].text)
            pag_links = []

            for pag_link in range(1, pag_links_count + 1):
                # for pag_link in range(1):
                pag_links.append(f'{url}?page={pag_link}')

            all_product_links = []

            for link in pag_links:

                driver.get(link)
                time.sleep(3)

                with open('index.html', 'w', encoding='utf-8-sig') as f:
                    f.write(driver.page_source)
                with open('index.html', encoding='utf-8-sig') as f:
                    src = f.read()
                soup = BeautifulSoup(src, 'lxml')
                product_links = soup.find_all('div', class_='product-tile')

                product_urls = []
                for pr_link in product_links:
                    pr_link = pr_link.find('a').get('href')
                    product_urls.append(f'{host}{pr_link}')
                all_product_links.extend(product_urls)
        except AttributeError:
            all_product_links = []
            product_links = soup.find_all('div', class_='product-tile')

            product_urls = []
            for pr_link in product_links:
                pr_link = pr_link.find('a').get('href')
                product_urls.append(f'{host}{pr_link}')
            all_product_links.extend(product_urls)
        #  Збір даних про товари
        for product_url in all_product_links:
            images = []
            driver.get(url=product_url)
            time.sleep(3)
            with open('index.html', 'w', encoding='utf-8-sig') as f:
                f.write(driver.page_source)
            with open('index.html', encoding='utf-8-sig') as f:
                src = f.read()
            soup = BeautifulSoup(src, 'lxml')

            try:
                ua_link = soup.find('ul', class_='nav navbar-nav navbar-right').find('li').find('a').get('href')
            except AttributeError:
                ua_link = 'ERROR'

            ua_links_list.append(ua_link)

            try:
                title = soup.find('h1', class_='product-header').text.strip()
            except AttributeError:
                title = 'ERROR'

            try:
                all_images = soup.find_all('figure', class_='image-additional')
                main_image = soup.find('meta', attrs={'itemprop': 'image'})['content']
                images.append(main_image)

                for i in all_images:
                    image = i.find('a', class_='thumbnail').get('href')
                    images.append(f'https://001.com.ua{image}')
            except AttributeError:
                all_images = ''
                images = ''

            images = list(dict.fromkeys(images))
            images_str = " ;; ".join(images)

            print(images_str)

            availability_list = []
            outofstock = 'Нет в наличии'
            try:
                av_list = soup.find_all('span', class_='text-danger')

                for i in av_list:
                    availability_list.append(i.text.strip())
                if outofstock in availability_list:
                    availability = "outofstock"
                else:
                    availability = 'instock'

            except AttributeError:
                availability = 'outofstock'

            print(availability)

            try:
                price = soup.find('span', class_='product-price-value').text.strip()
            except AttributeError:
                price = ''

            try:
                brand = soup.find('span', attrs={"itemprop": "brand"}).find('span', attrs={"itemprop": "name"}).text
            except AttributeError:
                brand = 'ERROR'

            try:
                sku = soup.find('span', attrs={'itemprop': 'mpn'}).text
            except AttributeError:
                sku = 'ERROR'

            try:
                device_type_td = soup.find('td', string='Тип таймера').find_next('td')
                device_type_select = device_type_td.find('select',
                                                         class_='form-control form-control-auto submit-on-change')
                if device_type_select:
                    device_type = device_type_select['title'].strip().capitalize()
                    device_type = f'{device_type} таймер'
                else:
                    device_type = device_type_td.text.strip().capitalize()
                    device_type = f'{device_type} таймер'
            except AttributeError:
                device_type = ''

            max_current = test_pars(soup=soup, name='Максимальный ток нагрузки, А')
            num_of_channels = test_pars(soup=soup, name='Количество каналов')
            rated_voltage = test_pars(soup=soup, name='Номинальное напряжение питания, В')
            num_and_type_of_contacts = test_pars(soup=soup, name='Количество и вид контактов')
            max_program_operations = test_pars(soup=soup, name='Максимальное число программных операций')
            min_time_interval = test_pars(soup=soup, name='Минимальный интервал времени')

            try:
                montazh_td = soup.find('td', string='Монтаж').find_next(
                    'td')
                montazh_select = montazh_td.find('select', class_='form-control form-control-auto submit-on-change')
                if montazh_select:
                    montazh = montazh_select['title']
                    if montazh == 'на DIN-рейку':
                        montazh = 'DIN-рейка'
                    elif montazh == 'в розетку':
                        montazh = 'В розетку'
                else:
                    montazh = montazh_td.text.strip()
                    if montazh == 'на DIN-рейку':
                        montazh = 'DIN-рейка'
                    elif montazh == 'в розетку':
                        montazh = 'В розетку'
            except AttributeError:
                montazh = ''

            try:
                dopolnitelno_td = soup.find('td', string='Резерв хода').find_next('td')
                dopolnitelno_select = dopolnitelno_td.find('select',
                                                           class_='form-control form-control-auto submit-on-change')
                if dopolnitelno_select:
                    dopolnitelno = dopolnitelno_select['title'].strip()
                    if dopolnitelno == 'есть':
                        dopolnitelno = 'Резерв хода'
                    else:
                        dopolnitelno = ''
                else:
                    dopolnitelno = dopolnitelno_td.text.strip()
                    if dopolnitelno == 'есть':
                        dopolnitelno = 'Резерв хода'
                    else:
                        dopolnitelno = ''
            except AttributeError:
                dopolnitelno = ''

            #         Опис товару

            try:
                descr = soup.find('div', class_='product-description copyright')
                if descr:
                    descr.extract()
                    descr = str(descr)
                    descr = ''.join(descr.splitlines())
                    descr = descr.replace('<div id="chars">', '').replace(' class="header"', '').replace(
                        '<div itemprop="description">', '').replace('<div class="product-description copyright">',
                                                                    '').replace(
                        '</div>', '').replace('<div>', '')
                else:
                    descr = ''
            except AttributeError:
                descr = ''

            driver.get(ua_link)
            time.sleep(2)

            with open('index.html', 'w', encoding='utf-8-sig') as f:
                f.write(driver.page_source)
            with open('index.html', encoding='utf-8-sig') as f:
                src = f.read()

            soup_ua = BeautifulSoup(src, 'lxml')

            try:
                title_ua = soup_ua.find('h1', class_='product-header').text.strip()
            except AttributeError:
                title_ua = 'ERROR'

            try:
                descr_ua = soup_ua.find('div', class_='product-description copyright')
                if descr_ua:
                    descr_ua.extract()
                    descr_ua = str(descr_ua)
                    descr_ua = ''.join(descr_ua.splitlines())
                    descr_ua = descr_ua.replace('<div id="chars">', '').replace(' class="header"', '').replace(
                        '<div itemprop="description">', '').replace('<div class="product-description copyright">',
                                                                    '').replace(
                        '</div>', '').replace('<div>', '')
                else:
                    descr_ua = ''
            except AttributeError:
                descr_ua = ''

            data.append({
                'URL': product_url,
                'product_id': 'new',
                'Русский slug': '',
                'Украинский slug': '',
                'images': images_str,
                'item_name': title,
                'category_name': 'Таймеры',
                'manufacturer_name': brand,
                'sku': sku,
                'model': sku,
                'stock_status': availability,
                'is_active': 1,
                'warranty': 12,
                'price': price,
                'Русский title': title,
                'Русский description': descr,
                'Украинский title': title_ua,
                'Украинский description': descr_ua,
                'Тип устройства': f'Русский ~ {device_type}',
                'Максимальный ток': f'Русский ~ {max_current}',
                'Способ монтажа': f'Русский ~ {montazh}',
                'Количество каналов': f'Русский ~ {num_of_channels}',
                'Дополнительно': f'Русский ~ {dopolnitelno}',
                'Номинальное напряжение питания': f'Русский ~ {rated_voltage}',
                'Количество и вид контактов': f'Русский ~ {num_and_type_of_contacts}',
                'Максимальное число программных операций': f'Русский ~ {max_program_operations}',
                'Минимальный интервал времени': f'Русский ~ {min_time_interval}',

            })
            driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul[2]/li[1]/a/span[1]').click()
            time.sleep(2)

        with open('taymery-sutochnye-nedelnye-godovye-astronomicheskie.csv', 'w', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['URL',
                                                   'product_id',
                                                   'Русский slug',
                                                   'Украинский slug',
                                                   'images',
                                                   'item_name',
                                                   'category_name',
                                                   'manufacturer_name',
                                                   'sku',
                                                   'model',
                                                   'stock_status',
                                                   'is_active',
                                                   'warranty',
                                                   'price',
                                                   'Русский title',
                                                   'Русский description',
                                                   'Украинский title',
                                                   'Украинский description',
                                                   'Тип устройства',
                                                   'Максимальный ток',
                                                   'Способ монтажа',
                                                   'Количество каналов',
                                                   'Дополнительно',
                                                   'Номинальное напряжение питания',
                                                   'Количество и вид контактов',
                                                   'Максимальное число программных операций',
                                                   'Минимальный интервал времени',
                                                   ])
            writer.writeheader()
            for data in data:
                writer.writerow(data)

    finally:
        driver.close()
        driver.quit()


def main():
    product_data = get_cat_html_ru()
    play_sound()


if __name__ == "__main__":
    main()
