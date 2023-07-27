import requests
from bs4 import BeautifulSoup
import csv
import concurrent.futures

CSV = 'links.csv'
HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}
URL = []


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r.text


def get_html_2(url):
    r = requests.get(url, headers=HEADERS)
    return r


def open_list():
    with open(CSV, 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])


count = 0


def get_items(url):
    html = get_html(url)
    resp = get_html_2(url)
    metas = []

    soup = BeautifulSoup(html, 'lxml')
    try:
        title = soup.find('title').text
    except AttributeError:
        title = 'ERROR'
    try:
        h1 = soup.find('h1').text
    except AttributeError:
        h1 = 'ERROR'


    # Вигрузка ссилок для всіх категорій з меню

#    try:
#        all_cat_links_list = soup.find_all('a', class_='catalog_link__c1eYd catalog_linkLeafs__eHr9S')
#
#        cat_link_list = []
#
#        for cat_link in all_cat_links_list:
#            cat_link = f"https://e-server.com.ua{cat_link.get('href')}"
#            cat_link_list.append(cat_link)
#
#            print(cat_link)
#    except AttributeError:
#        cat_link_list = []

    try:
        atr = soup.find('div', string='Переріз кабелю')
        if atr:
            atr = 'KUUURWAAA'
        else:
            atr = 'ERROR'
    except AttributeError:
        atr = 'ERROR'
    # Вигрузка всіх товарів зі сторінки
    # try:
    #     pr_links = soup.find('div', class_='flex flex-wrap max-w-full mx-3 xl:max-w-max xl:mx-0'
    #                                        ' xl:border-t-2 xl:border-l xl:border-darkBackgroundGray'
    #                                        ' 3xl:border-l-0 3xl:border-t-0').find_all('a')
    #
    #     for i in pr_links:
    #         i = i.get("href")
    #         print(f'https://e-server.com.ua{i}')
    #
    #
    # except AttributeError:
    #     pr_links = "ERROR"
    #

    # Вигрузка всіх статтей блога
    all_article_links = []
    # try:
    #      article_links_blocks = soup.find("div", class_='mt-3'
    #                                              ' xl:grid'
    #                                              ' xl:grid-cols-4'
    #                                              ' xl:gap-25px'
    #                                              ' xl:max-w-max'
    #                                              ' xl:mt-1').find_all('div', class_="truncate2mob3xl"
    #                                                                                 " h-10 xl:h-52px"
    #                                                                                 " font-semibold text-15px leading-5"
    #                                                                                 " xl:font-semibold xl:text-sm"
    #                                                                                 " xl:leading-4.5 3xl:font-semibold"
    #                                                                                 " 3xl:text-lg 3xl:leading-6")
    #      for link in article_links_blocks:
    #          link = link.find('a').get('href')
    #          print(link)
    # except AttributeError:
    #      all_article_links = ''
    # try:
    #     button = soup.find('button', class_='flex items-center justify-center text-white bg-greenEmerald hover:bg-greenEmeraldHover active:bg-greenEmerald active:border-greenEmerald min-w-137px h-11 px-13px xl:min-w-122px xl:h-38px xl:pt-3px xl:px-4 3xl:min-w-124px 3xl:h-44px 3xl:pt-px 3xl:px-4.5 font-bold text-base leading-6 xl:font-bold xl:text-15px xl:leading-5 3xl:font-bold 3xl:text-base 3xl:leading-5.5 rounded focus:outline-none disabled:opacity-50')
    #     if button:
    #         button = 'Yes'
    #     else:
    #         button = 'NO'
    # except AttributeError:
    #     button = 'ERROR'



    # try:
    #     description = soup.find("meta", attrs={"name": "description"})["content"]
    # except (AttributeError, KeyError):
    #     description = 'ERROR'
    #
    # try:
    #     date = soup.find('div', class_='text-lightTextColor font-medium text-15px leading-5 xl:font-normal xl:text-sm xl:leading-4.5').text
    # except AttributeError:
    #     date = 'ERROR'
    # try:
    #     pub_time = soup.find('time', class_='entry-date published updated').text
    # except AttributeError:
    #     pub_time = 'ERROR'

    # try:
    #     id_num = soup.find('span', class_='text-basicDarkTextColor text-13px'
    #                                       ' xl:font-normal xl:text-sm xl:leading-4.5'
    #                                       ' 3xl:font-medium 3xl:text-base'
    #                                       ' 3xl:leading-5.5false').text.split(' ')
    #     id_num = id_num[-1]
    # except AttributeError:
    #     id_num = 'ERROR'

    # Витягнути всі урли і назви категорій з меню
    # try:
    #     cat_names = []
    #     cat_links = []
    #     host = 'https://e-server.com.ua'
    #     cat_names_all = soup.find('div', class_='ROOT fixed inset-0 max-w-full' \
    #                                        ' overflow-x-hidden' \
    #                                        ' overflow-y-auto' \
    #                                        ' bg-white pb-116px' \
    #                                        ' z-30 transform translate-x-0 md:pb-135px xl:transform-none' \
    #                                        ' xl:transition-none xl:relative xl:block xl:inset-auto' \
    #                                        ' xl:overflow-visible xl:pt-1.5 xl:pb-0 xl:bg-lightStrokesGrey' \
    #                                        ' xl:self-start xl:min-w-238px' \
    #                                        ' xl:max-w-238px 3xl:min-w-266px' \
    #                                        ' 3xl:max-w-266px 3xl:-mt-px').find_all('a')
    #     for name in cat_names_all:
    #         name = name.text
    #         print(name)
    #         cat_names.append(name)
    #
    #     for link in cat_names_all:
    #         link = link.get('href')
    #         print(f'{host}{link}')
    # except AttributeError:
    #     cat_names = "ERROR"
    # try:
    #     ua_link = soup.find('div', class_='hg-langs z-10').find('div',
    #                                                             class_='langs_langs__m_3_V langs_mob_header__ruSPE').find('a').get('href')
    # except AttributeError:
    #     ua_link = 'ERROR'

    try:
        product_id = soup.find('span', class_='text-basicDarkTextColor text-13px xl:font-normal xl:text-sm'
                                              ' xl:leading-4.5 3xl:font-medium 3xl:text-base'
                                              ' 3xl:leading-5.5').text.replace('Код товара: ', '').strip()
    except AttributeError:
        product_id = 'ERROR'
    try:
        sku = soup.find('span', class_='mb-13px xl:mb-5px xl:last:mb-0 xl:pl-1 3xl:pl-0undefined').text
        sku = sku.replace('Артикул: ', '').strip()
    except AttributeError:
        sku = 'ERROR'



    # try:
    #     stock_status = soup.find('mark', class_='outofstock').text
    # except AttributeError:
    #     stock_status = "В наличии"

    # try:

    #     count = soup.find('body').text.count(keyword)
    # except AttributeError:
    #     count = 'ERROR'

    # try:
    #     table_check = soup.find('div', class_='es-table-wrapper').text
    #     if table_check:
    #         table_check = 'YES'
    # except AttributeError:
    #     table_check = 'NO'

    metas.append({
        # 'url': url,
        'h1': h1,
        # 'title': title,
        # 'description': description,
        # 'button': button,
        # 'date': date

        # 'iframe_check': iframe_check,
        'product_id': product_id,
        'sku': sku,
        'atr': atr
        # 'stock_status': stock_status,

    })
    print(url)


    return metas


def main():
    open_list()

    metas = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_items, url) for url in URL]

        for future in concurrent.futures.as_completed(futures):
            metas.extend(future.result())

    with open('output.csv', 'w', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['product_id', 'h1', 'sku', 'atr'])
        writer.writeheader()
        for meta in metas:
            writer.writerow(meta)


if __name__ == '__main__':
    main()
