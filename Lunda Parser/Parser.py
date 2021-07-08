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

class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': '*/*'}

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
        product_chars_titles = product_item.select('th.products-table__header')
        product_chars = product_item.select('td.products-table__item')
        #print(product_chars_titles)
        titles = []
        chars = []
        if not product_chars:
            logger.error('no chars')
        for product_chars_title in product_chars_titles:
            title = self.char_title(product_chars_title=product_chars_title)
            chars_title = title
            titles.append(chars_title)
            print(titles)
        for product_char in product_chars:
            # print(product_char)
            name = self.char_name(product_char=product_char)
            #title = self.char_title(product_char=product_char)
            char = name
            chars.append(char)
            #print(name)
        print(titles)
        print(chars)

        return chars

    def char_title(self, product_chars_title):
        title = product_chars_title.get_text()
        return title

    def char_name(self, product_char):
        name = product_char.get_text()
        r = name.strip()
        return r #title, name.strip()


    def save_results(self):
        path = 'D:/PythonProg/Parsers/Lunda Parser/test.csv'
        with open(path, 'w') as f:
            writer = csv.writer(f)  # , quoting=csv.QUOTE_MINIMAL)
            writer.writerow()
            # for item in self.result:
            # pass

    def run(self):
        text = self.load_page()
        self.pars_page(text=text)
        self.save_results()


if __name__ == '__main__':
    parser = Client()
    parser.run()
