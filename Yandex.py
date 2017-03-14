# -*- coding: UTF-8 -*-

"""Get first 3 link from Yandex and prints if spelling error"""
import sys
import urllib
import requests
from lxml import html


class SearchService(object):
    """Yandex searching service class"""
    def __init__(self, usr_arg=None):
        """create exemplar for curr req and check input"""
        self.req_data = usr_arg or ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
        while not self.req_data:
            print 'Please enter your request blanked by a whitespace.'
            self.req_data = raw_input()

    def main(self):
        """sequentially runs methods"""
        req_data = self.get_request()
        links_list = self.get_links(req_data)
        self.print_results(links_list[:3])

    def get_request(self):
        """get request from Yandex"""
        return requests.get('https://yandex.ru/search/', params={'text': self.req_data})

    @staticmethod
    def get_links(req_data):
        """get links on request from html"""
        tree = html.fromstring(req_data.text)
        if tree.xpath('.//*[@class="misspell__message"]'):
            print tree.xpath('string(.//*[@class="misspell__message"])')
        links = tree.xpath('.//*[@class="link organic__url link link_cropped_no"]/@href')
        return links

    @staticmethod
    def print_results(links):
        """print request results"""
        if not links:
            print 'Sorry, we don\'t find anything!'
        else:
            for link in links:
                print urllib.unquote(link).decode('utf8')


if __name__ == '__main__':
    YS = SearchService()
    YS.main()
