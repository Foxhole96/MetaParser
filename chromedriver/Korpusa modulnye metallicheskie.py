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

url = 'https://001.com.ua/korpusa-modulnye-metallicheskie'
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
                type_of_shell_td = soup.find('td', string='Тип корпуса').find_next('td')
                type_of_shell_select = type_of_shell_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if type_of_shell_select:
                    type_of_shell = type_of_shell_select['title'].capitalize()
                else:
                    type_of_shell = type_of_shell_td.text.strip().capitalize()
            except AttributeError:
                type_of_shell = ''

            try:
                number_of_modules_td = soup.find('td', string='Количество модулей').find_next('td')
                number_of_modules_select = number_of_modules_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if number_of_modules_select:
                    number_of_modules = number_of_modules_select['title']
                else:
                    number_of_modules = number_of_modules_td.text.strip()
            except AttributeError:
                number_of_modules = ''


            try:
                degree_of_protection_td = soup.find('td', string='Степень защиты').find_next('td')
                degree_of_protection_select = degree_of_protection_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if degree_of_protection_select:
                    degree_of_protection = degree_of_protection_select['title']
                else:
                    degree_of_protection = degree_of_protection_td.text.strip()
            except AttributeError:
                degree_of_protection = ''


            try:
                place_for_counter_td = soup.find('td', string='Место под счетчик').find_next('td')
                place_for_counter_select = place_for_counter_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if place_for_counter_select:
                    place_for_counter = place_for_counter_select['title'].strip().capitalize()
                else:
                    place_for_counter = place_for_counter_td.text.strip().capitalize()
            except AttributeError:
                place_for_counter = ''

            try:
                coating_type_td = soup.find('td', string='Тип покрытия').find_next('td')
                coating_type_select = coating_type_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if coating_type_select:
                    coating_type = coating_type_select['title'].strip()
                else:
                    coating_type = coating_type_td.text.strip()
            except AttributeError:
                coating_type = ''

            try:
                dopolnitelno_td = soup.find('td', string='Наличие замка').find_next('td')
                dopolnitelno_select = dopolnitelno_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if dopolnitelno_select:
                    dopolnitelno = dopolnitelno_select['title'].strip()
                    if dopolnitelno == 'есть':
                        dopolnitelno = 'Замок'
                    else:
                        dopolnitelno = ''
                else:
                    dopolnitelno = dopolnitelno_td.text.strip()
                    if dopolnitelno == 'есть':
                        dopolnitelno = 'Замок'
                    else:
                        dopolnitelno = ''
            except AttributeError:
                dopolnitelno = ''

            try:
                window_td = soup.find('td', string='Наличие окошка').find_next('td')
                window_select = window_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if window_select:
                    window = window_select['title'].strip().capitalize()
                else:
                    window = window_td.text.strip().capitalize()
            except AttributeError:
                window = ''


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
                type_of_shell_ua_td = soup.find('td', string='Тип корпусу').find_next('td')
                type_of_shell_ua_select = type_of_shell_ua_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if type_of_shell_ua_select:
                    type_of_shell_ua = type_of_shell_ua_select['title'].capitalize()
                else:
                    type_of_shell_ua = type_of_shell_ua_td.text.strip().capitalize()
            except AttributeError:
                type_of_shell_ua = ''

            try:
                place_for_counter_ua_td = soup.find('td', string='Місце під лічильник').find_next('td')
                place_for_counter_ua_select = place_for_counter_ua_td.find('select',
                                                                           class_='form-control form-control-auto submit-on-change')
                if place_for_counter_ua_select:
                    place_for_counter_ua = place_for_counter_ua_select['title'].capitalize().strip()
                else:
                    place_for_counter_ua = place_for_counter_ua_td.text.capitalize().strip()
            except AttributeError:
                place_for_counter_ua = ''

            try:
                coating_type_ua_td = soup.find('td', string='Тип покриття').find_next('td')
                coating_type_ua_select = coating_type_ua_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if coating_type_ua_select:
                    coating_type_ua = coating_type_ua_select['title'].strip()
                else:
                    coating_type_ua = coating_type_ua_td.text.strip()
            except AttributeError:
                coating_type_ua = ''

            try:
                window_ua_td = soup.find('td', string='Наявність віконця').find_next('td')
                window_ua_select = window_ua_td.find('select',
                                                                   class_='form-control form-control-auto submit-on-change')
                if window_ua_select:
                    window_ua = window_ua_select['title'].strip().capitalize()
                else:
                    window_ua = window_ua_td.text.strip().capitalize()
            except AttributeError:
                window_ua = ''

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
                'category_name': 'Щитки металлические',
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
                'Способ монтажа': f'Русский ~ {type_of_shell} ;; Украинский ~ {type_of_shell_ua}',
                'Количество модулей': f'Русский ~ {number_of_modules} ;; Украинский ~ {number_of_modules}',
                'Степень защиты': f'Русский ~ {degree_of_protection} ;; Украинский ~ {degree_of_protection}',
                'Место под счетчик': f'Русский ~ {place_for_counter} ;; Украинский ~ {place_for_counter_ua}',
                'Тип покрытия': f'Русский ~ {coating_type} ;; Украинский ~ {coating_type_ua}',
                'Дополнительно': f'Русский ~ {dopolnitelno} ;; Украинский ~ {dopolnitelno}',
                'Наличие окошка': f'Русский ~ {window} ;; Украинский ~ {window_ua}',

            })
            driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul[2]/li[1]/a/span[1]').click()
            time.sleep(2)


        with open('korpusa-modulnye-metallicheskie.csv', 'w', encoding='utf-8-sig') as f:
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
                                                   'Способ монтажа',
                                                   'Количество модулей',
                                                   'Степень защиты',
                                                   'Место под счетчик',
                                                   'Тип покрытия',
                                                   'Дополнительно',
                                                   'Наличие окошка'
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
