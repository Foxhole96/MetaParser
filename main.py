import requests
from bs4 import BeautifulSoup
import csv
from lxml import etree

CSV = 'links.csv'

HEADERS = {
    'accept': 'application/signed-exchange;v=b3;q=0.7,*/*;q=0.8',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 '
                  'Safari/537.36 '
}
URL = []


def get_html(url):
    r = requests.get(url, headers=HEADERS)
    return r


def open_list():
    with open('new_links.csv', 'r') as f:
        reader = csv.reader(f)
        for line in reader:
            URL.append(line[0])


def get_items():
    open_list()
    iter = 0
    metas = []

    for i in URL:

        get_html(i)
        html = get_html(i)
        iter += 1

        def get_meta(html):

            soup = BeautifulSoup(html, 'lxml')
            soup.find_all('meta', attrs={"description"})

            try:

                h1 = soup.find('h1').get_text()

            except AttributeError:
                h1 = 'ERROR'

            # try:
            #     all_page_links = soup.find('div', class_='es-article es-article-body text-basicDarkTextColor xl:mt-8 '
            #                                              'font-medium text-15px leading-5 xl:font-medium xl:text-15px '
            #                                              'xl:leading-5').find_all('a')
            #     page_links = []
            #
            #     for p in all_page_links:
            #         p = p.get('href')
            #         page_links.append(p)
            # except AttributeError:
            #     page_links = 'ERROR'

            try:
                title = soup.find('title').get_text()
            except AttributeError:
                title = 'ERROR'
            try:
                description = soup.find("meta", attrs={"name": "description"}).get("content")
            except AttributeError:
                description = 'ERROR'
            # try:
            #     faq_title = soup.find('h3', class_='mt-8 text-lightBlack xl:mt-41px font-semibold text-base leading-5 '
            #                                        'xl:font-bold xl:text-17px xl:leading-6 3xl:font-semibold '
            #                                        '3xl:text-lg 3xl:leading-6').get_text()
            # except AttributeError:
            #     faq_title = "ERROR"
            # try:
            #     text = soup.find('div', class_="es-article es-article-body text-basicDarkTextColor mt-12 xl:mt-0 "
            #                                    "3xl:min-w-1000px 3xl:max-w-1000px font-medium text-15px leading-5 "
            #                                    "xl:font-medium xl:text-15px xl:leading-5")
            #     # text = soup.find('div', class_='term-description')
            #     if text:
            #         text = 'YES'
            # except AttributeError:
            #     text = 'ERROR'

            # try:
            #     t_links = soup.find_all('a')
            #     test_links = []
            #     for link in t_links:
            #         link = link.get('href')
            #         print(link)
            #     print(test_links)
            # except AttributeError:
            #     t_links = 'ERROR'

            # try:
            #     new_site_text = soup.find('div', id="content-descr").get_text()
            # except AttributeError:
            #     new_site_text = 'ERROR'

            # try:
            #     sku = soup.find('div', class_='mb-13px xl:mb-5px xl:last:mb-0 xl:pl-1 3xl:pl-0').get_text()
            # except AttributeError:
            #     sku = 'ERROR'

            try:
                product_id = soup.find('div', class_='tm-product-id').get_text()
            except AttributeError:
                product_id = 'ERROR'
            product_id = product_id.split()[-1]

            dom = etree.HTML(str(soup))
            try:
                video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[1]/a')[0].get('href'))

            except IndexError as ex:
                video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[2]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[3]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[4]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[5]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[6]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[7]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[8]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[9]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[10]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[11]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[12]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'

            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[14]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[15]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[16]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[17]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[18]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[19]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[20]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'
            if video != 'ERROR' and video.split('/')[2] != 'www.youtube.com':

                try:
                    video = (dom.xpath(f'//*[@id="product-{product_id}"]/div[2]/div[1]/div/figure/div[2]/div/div[21]/a')[
                                 0].get('href'))
                except IndexError:
                    video = 'ERROR'

            items = [{
                'URL': i,
                'VIDEO': video,
                'PRODUCT_ID': product_id,
                'H1': h1,
                # 'TITLE': title,
                # 'SKU': sku,

                # 'TITLE LENGTH': len(title),
                # 'TEXT': text,
                # 'TITLE WORDS': len(title.split(' ')),
                # 'DESCRIPTION': description,
                # 'DESCRIPTION LENGTH': len(description),
                # 'DESCRIPTION WORDS': len(description.split(' ')),
                # 'Status Code': get_html(i),
                # 'DOMAIN': i.split('/')[2],
                # 'H1': h1,
                # 'SKU': sku,
                # 'TEXT': new_site_text
                # 'PAGE_LINKS': page_links,
                # 'H1 LENGTH': len(h1),
                # 'H1 WORDS': len(h1.split(' ')),
                # 'FAQ_TITLE': faq_title,



            }]

            return items

        print('Сторінка №', iter)
        metas.extend(get_meta(html.text))

    return metas


get_items = get_items()


def save_doc(get_items, path):
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f, delimiter='^')
        writer.writerow(
            ['URL', 'PRODUCT_ID', 'H1', 'VIDEO'])
        for item in get_items:
            writer.writerow(
                [item['URL'], item['PRODUCT_ID'], item['H1'], item['VIDEO']])


try:
    save_doc(get_items, CSV)

except Exception as ex:
    print(ex)
finally:
    print('Завершено')
