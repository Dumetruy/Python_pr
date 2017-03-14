# -*- coding: UTF-8 -*-

"""first 3 link from Yandex with misspell checking"""
import sys
import urllib
import requests
from lxml import html


class SearchService(object):
    """Google searching service class"""
    def __init__(self, usr_input=None):
        """create exemplar for curr req and check input"""
        self.req_data = usr_input or ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
        while not self.req_data:
            print 'Please enter your request blanked by a whitespace.'
            self.req_data = raw_input()

    def find(self):
        """main method"""
        req_data = self.get_request()
        links_list = self.get_links_from_tree(req_data)
        self.get_result(links_list[:3])

    def get_request(self):
        """get request form Yandex"""
        return requests.get('https://yandex.ru/search/', params={'text': self.req_data})

    def get_links_from_tree(self, req_data):
        """create tree from request and get links """
        tree = html.fromstring(req_data.text)
        mis_msg = tree.xpath('.//*[@class="misspell__message"]/a/@href')
        if mis_msg:
            self.get_val_mis(mis_msg[0])
        links = tree.xpath('.//*[@class="link organic__url link link_cropped_no"]/@href')
        return links

    @staticmethod
    def get_result(links_lst):
        """print request result"""
        if not links_lst:
            print 'Sorry, we don\'t find anything!'
        else:
            for link in links_lst:
                print urllib.unquote(link).decode('utf8')

    @staticmethod
    def get_val_mis(link):
        """print user unchanged request link"""
        val_url = urllib.unquote(link).decode('utf8')
        print 'Исправлена опечатка: https://yandex.ru{}'.format(val_url.encode('utf8'))


if __name__ == '__main__':
    GS = SearchService()
    GS.find()
