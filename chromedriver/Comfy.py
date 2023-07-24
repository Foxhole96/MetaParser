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

urls = []

CSV = 'links.csv'
with open(CSV, 'r') as f:
    reader = csv.reader(f)
    for line in reader:
        urls.append(line[0])

options = webdriver.ChromeOptions()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(HEADERS['User-Agent'])

driver = webdriver.Chrome(options=options)




def get_cat_html_ru():
    try:

        for url in urls:
            driver.get(url=url)
            time.sleep(3)

    finally:
        driver.quit()


def main():
    get_cat_html_ru()

if __name__ == "__main__":
    main()
