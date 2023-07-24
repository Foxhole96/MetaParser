import csv
import time
import requests
from bs4 import BeautifulSoup
import re
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import winsound

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.binary_location = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
driver = webdriver.Chrome(options=options)

urls = ['https://comfy.ua/ua/tochka-dostupa-mikrotik-rbwapg-5hacd2hnd-be-black.html',
        'https://comfy.ua/ua/noutbuk-igrovoj-acer-nitro-5-an515-45-r94y-nh-qb9eu-007-black.html',
        'https://comfy.ua/ua/noutbuk-acer-aspire-5-a515-56g-35pr-nx-at2eu-00l-pure-silver.html',
        'https://comfy.ua/ua/noutbuk-igrovoj-acer-acer-nitro-5-an515-45-nh-qbaeu-001-black.html']

for url in urls:
    driver.get(url=url)
    wait = WebDriverWait(driver, 10)
    time.sleep(5)



#
# def get_cat_html_ru():
#     data = []
#     all_product_links = []
#     start_time = time.time()
#
#     try:
#
#         with open('links.csv', 'r', encoding='utf-8-sig') as f:
#             reader = csv.reader(f)
#             for line in reader:
#                 all_product_links.append(line[0])
#
#         driver.get(url='https://001.com.ua/')
#         time.sleep(2)
#         driver.find_element(By.XPATH, '/html/body/header/nav/div/div[2]/ul[2]/li[1]/a/span[1]').click()
#         time.sleep(2)
#
#         for i in all_product_links:
#             driver.get(url=i)
#
#             with open('index.html', 'w', encoding='utf-8-sig') as f:
#                 f.write(driver.page_source)
#
#             with open('index.html', encoding='utf-8-sig') as f:
#                 src = f.read()
#             soup = BeautifulSoup(src, 'lxml')
#
#             try:
#                 title = soup.find('h1', class_='product-header').text.strip()
#             except AttributeError:
#                 title = 'ERROR'
#
#             availability_list = []
#             outofstock = 'Нет в наличии'
#
#             try:
#                 av_list = soup.find_all('span', class_='text-danger')
#
#                 for i in av_list:
#                     availability_list.append(i.text.strip())
#                 if outofstock in availability_list:
#                     availability = "outofstock"
#                 else:
#                     availability = 'instock'
#
#             except AttributeError:
#                 availability = 'outofstock'
#
#             print(availability)
#
#             try:
#                 price = soup.find('span', class_='product-price-value').text.strip()
#             except AttributeError:
#                 price = ''
#
#             try:
#                 sku = soup.find('span', attrs={'itemprop': 'mpn'}).text
#             except AttributeError:
#                 sku = 'ERROR'
#
#             data.append({
#
#                 'item_name': title,
#                 'sku': sku,
#                 'stock_status': availability,
#                 'price': price,
#
#             })
#             time.sleep(2)
#
#         with open('001Price.csv', 'w', encoding='utf-8-sig') as f:
#             writer = csv.DictWriter(f, fieldnames=['item_name', 'sku', 'stock_status', 'price'])
#             writer.writeheader()
#             for data in data:
#                 writer.writerow(data)
#         end_time = time.time()
#         total_time = end_time - start_time
#         print("Время работы скрипта: {:.2f} секунд.".format(total_time))
#         print("Точное время окончания работы скрипта:", time.strftime("%Y-%m-%d %H:%M:%S"))
#
#
#     finally:
#         driver.close()
#         driver.quit()
#
#
# def main():
#     product_data = get_cat_html_ru()
#
#
# if __name__ == "__main__":
#     main()
