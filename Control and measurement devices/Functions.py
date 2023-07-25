import subprocess
import requests
import time

def test_pars(soup, name):
    try:

        td = soup.find('td', string=name).find_next('td')
        select = td.find('select', class_='form-control form-control-auto submit-on-change')

        if select:
            title = select['title']
        else:
            title = td.text

        if ';' in title:
            title = title.strip().replace('~', '').replace('; ', ' ;; Русский ~ ')
        elif any(x in title for x in ['~', ')', '%', '(', 'cosφ', 'sin']):
            title = title.strip().replace('~', '').split(' ', 1)[0]
        else:
            title = title.strip()

    except AttributeError:
        title = ''

    return title


def test_pars_capitalize(soup, name):
    try:

        td = soup.find('td', string=name).find_next('td')
        select = td.find('select', class_='form-control form-control-auto submit-on-change')

        if select:
            title = select['title']
        else:
            title = td.text

        if ';' in title:
            title = title.strip().capitalize().replace('~', '').replace('; ', ' ;; Русский ~ ')
        else:
            title = title.strip().capitalize()

    except AttributeError:
        title = ''
    return title



def play_sound():
    sound_file = "/usr/share/sounds/gnome/default/alerts/drip.ogg"
play_sound()

def check_internet_connection(host_url):
    while True:
        try:
            response = requests.get(host_url)
            if response.status_code == 200:
                print("Интернет соединение с хостом есть.")
                break
        except requests.ConnectionError:
            print("Интернет соединение с хостом отсутствует. Повторная проверка через 10 секунд...")
            time.sleep(10)
def check_internet_and_continue():
    check_internet_connection("https://001.com.ua/")
    print("Продолжение выполнения скрипта...")
    time.sleep(2)