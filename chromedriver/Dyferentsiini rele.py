import csv
import time
import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://001.com.ua/differentsialnye-rele-uzo'
options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(HEADERS)

driver = webdriver.Chrome()


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

            try:
                availability = 'outofstock'

                green_span = soup.find('span', class_='text-green')
                primary_span = soup.find('span', class_='text-primary')
                danger_span = soup.find('span', class_='text-danger')

                if green_span and (
                        'Поставка 1-2 рабочих дня' in green_span.text or 'Есть в наличии' in green_span.text):
                    availability = 'instock'
                elif primary_span and (
                        'Под заказ, 2-3 рабочих дня' in primary_span.text or 'Ожидается в наличии' in primary_span.text):
                    availability = 'instock'
                elif danger_span and 'Нет в наличии' in danger_span.text:
                    availability = 'outofstock'
            except AttributeError:
                availability = 'outofstock'

            print(availability)

            try:
                price = soup.find('span', class_='product-price-value').text.strip()
            except AttributeError:
                price = 'ERROR'

            try:
                brand = soup.find('span', attrs={"itemprop": "brand"}).find('span', attrs={"itemprop": "name"}).text
            except AttributeError:
                brand = 'ERROR'

            try:
                sku = soup.find('span', attrs={'itemprop': 'mpn'}).text
            except AttributeError:
                sku = 'ERROR'

            try:
                count_of_poluses_td = soup.find('td', string='Количество полюсов').find_next('td')
                count_of_poluses_select = count_of_poluses_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if count_of_poluses_select:
                    count_of_poluses = count_of_poluses_select['title'].strip()
                else:
                    count_of_poluses = count_of_poluses_td.text.strip()
            except AttributeError:
                count_of_poluses = 'ERROR'

            try:
                nominal_current_td = soup.find('td', string='Номинальный ток, А').find_next('td')
                nominal_current_select = nominal_current_td.find('select',
                                                                 class_='form-control form-control-auto submit-on-change')
                if nominal_current_select:
                    nominal_current = nominal_current_select['title']
                else:
                    nominal_current = nominal_current_td.text.strip()
            except AttributeError:
                nominal_current = 'ERROR'

            try:
                rrbc_td = soup.find('td', string='Номинальный отключающий дифференциальный ток, мА').find_next('td')
                rrbc_select = rrbc_td.find('select',
                                                                                 class_='form-control form-control-auto submit-on-change')
                if rrbc_select:
                    rrbc = rrbc_select['title'].strip()
                else:
                    rrbc = rrbc_td.text.strip()
            except AttributeError:
                rrbc = 'ERROR'

            try:
                type_td = soup.find('td', string='Тип').find_next('td')
                type_select = type_td.find('select', class_='form-control form-control-auto submit-on-change')
                if type_select:
                    type_ru = type_select['title'].strip()
                else:
                    type_ru = type_td.text.strip()
            except AttributeError:
                type_ru = 'ERROR'

            try:
                maximum_breaking_capacity_td = soup.find('td',
                                                         string='Максимальная отключающая способность, кА').find_next(
                    'td')
                maximum_breaking_capacity_select = maximum_breaking_capacity_td.find('select',
                                                                                     class_='form-control form-control-auto submit-on-change')
                if maximum_breaking_capacity_select:
                    maximum_breaking_capacity = maximum_breaking_capacity_select['title'].strip()
                else:
                    maximum_breaking_capacity = maximum_breaking_capacity_td.text.strip()
            except AttributeError:
                maximum_breaking_capacity = 'ERROR'

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
                    descr = 'ERROR'
            except AttributeError:
                descr = 'ERROR'


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
                type_ua_td = soup_ua.find('td', string='Тип').find_next('td')
                type_ua_select = type_ua_td.find('select', class_='form-control form-control-auto submit-on-change')
                if type_ua_select:
                    type_ua = type_ua_select['title']
                else:
                    type_ua = type_ua_td.text.strip()
            except AttributeError:
                type_ua = 'ERROR'

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
                    descr_ua = 'ERROR'
            except AttributeError:
                descr_ua = 'ERROR'

            data.append({
                'URL': product_url,
                'product_id': 'new',
                'Русский slug': '',
                'Украинский slug': '',
                'images': images_str,
                'item_name': title,
                'category_name': 'УЗО',
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
                'Количество полюсов': f'Русский ~ {count_of_poluses} ;; Украинский ~ {count_of_poluses}',
                'Номинальный ток': f'Русский ~ {nominal_current} ;; Украинский ~ {nominal_current}',
                'Номинальный отключающий дифференциальный ток': f'Русский ~ {rrbc} ;; Украинский ~ {rrbc}',
                'Тип': f'Русский ~ {type_ru} ;; Украинский ~ {type_ua}',
                'Максимальная отключающая способность, кА':  f'Русский ~ {maximum_breaking_capacity} ;;'
                                                             f' Украинский ~ {maximum_breaking_capacity}',

            })
            driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul[2]/li[1]/a/span[1]').click()
            time.sleep(2)

        with open('differentsialnye-rele-uzo.csv', 'w', encoding='utf-8-sig') as f:
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
                                                   'Количество полюсов',
                                                   'Номинальный ток',
                                                   'Номинальный отключающий дифференциальный ток',
                                                   'Тип',
                                                   'Максимальная отключающая способность, кА',
                                                   ])
            writer.writeheader()
            for data in data:
                writer.writerow(data)

    finally:
        driver.close()
        driver.quit()




def main():
    product_data = get_cat_html_ru()

if __name__ == "__main__":
    main()
