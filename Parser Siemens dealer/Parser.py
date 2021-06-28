import requests
from bs4 import BeautifulSoup

URL = 'https://sbtpro.ru/datchiki_temperaturi_vodi_pogrugnie_qae/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://sbtpro.ru'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('li', class_='numpages_li')
    print(pagination)

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr', class_='')
    #print(items)
    instr = []
    i = 0
    for item in items:
        if item.find_parent(class_='itemProductList') and not item.find(class_="heiListPr"):
            #print(item, i)
            instr.append({
                'title': item.find('a', class_='nameListProd').get_text(),
                'link': HOST + item.find('a', class_='nameListProd').get('href'),
                'artikul': item.find('div', class_='listArticul').get_text(),
                'price': item.find('div', class_='listPrice').get_text()

        }
        )
            i += 1
    print(instr)
    #print(i)


def pars():
    html = get_html(URL)
    if html.status_code == 200:
        pages_count = get_pages_count(html.text)
        get_content(html.text)
    else:
        print("Error Get")


pars()
