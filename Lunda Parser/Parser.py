"""На основе руководства из: https://www.youtube.com/watch?v=UQlUAmCnbzQ"""

import logging
import collections
import requests
import lxml
import csv

from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('ld')

ParserResult = collections.namedtuple(
    'ParserResult',
    (

    )
)

HEADERS = (
)

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': '*/*'}
        self.chars_title_result = []
        self.chars_result = []


    def load_page(self):
        url = 'https://lunda.ru/catalog/category/c6002.html'
        res = self.session.get(url=url)
        res.raise_for_status()
        return res.text

    def pars_page(self, text: str):
        soup = BeautifulSoup(text, 'lxml')
        container = soup.select('a.js-product.product')
        for block in container:
            url = self.url_block(block=block)
            text = self.load_product_page(url=url)
            self.pars_product_page(text=text)

    def url_block(self, block):

        """if not url_block:
            logger.error('no url block')
            return"""

        short_url = block.get('href')
        if not short_url:
            logger.error('no href')

        url = 'https://lunda.ru' + short_url

        logger.info('%s', url)
        return url

    def load_product_page(self, url):
        product_url = url
        res = self.session.get(url=product_url)
        res.raise_for_status()
        return res.text

    def pars_product_page(self, text):
        soup_product_page = BeautifulSoup(text, 'lxml')
        product_table = soup_product_page.select('table.js-products-table.products-table')
        for product_row in product_table:
            self.pars_product_table(product_row=product_row)

    def pars_product_table(self, product_row):
        product_items = product_row.select('tr')
        if not product_items:
            logger.error('no items')
        for product_item in product_items:
            self.pars_product_items(product_item=product_item)

    def pars_product_items(self, product_item):
        product_chars_titles = product_item.select('span.products-table__header-text')
        product_chars = product_item.select('td.products-table__item')
        titles = []
        chars = []
        if not product_chars_titles:
            logger.error('no chars title')
        if not product_chars:
            logger.error('no chars')
        for product_chars_title in product_chars_titles:
            title = self.char_title(product_chars_title=product_chars_title)
            title = " ".join(title.split())
            chars_title = title
            titles.append(chars_title)
        for product_char in product_chars:
            name = self.char_name(product_char=product_char)
            name = " ".join(name.split())
            char = name
            chars.append(char)
        if titles != []:
            self.chars_result.append(titles)

        if chars != []:
            self.chars_result.append(chars)
        #self.chars_title_result.append(titles)

        #print(self.chars_title_result)
        #print(self.chars_result)

        return chars

    def char_title(self, product_chars_title):
        title = product_chars_title.get_text()
        return title.strip()

    def char_name(self, product_char):
        name = product_char.get_text()
        return name.strip()


    def save_results(self):
        path = 'D:/PythonProg/Parsers/Lunda Parser/test.csv'
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f , delimiter=';')
            x = 0
            for item in self.chars_result:
                if item:
                    print(item)
                    writer.writerow(item)
                    x += 1
                else:
                    pass
            print(x)


    def run(self):
        text = self.load_page()
        self.pars_page(text=text)
        self.save_results()


if __name__ == '__main__':
    parser = Client()
    parser.run()

