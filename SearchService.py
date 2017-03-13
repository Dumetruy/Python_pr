# -*- coding: UTF-8 -*-

"""first 3 link from Google"""
import sys
import requests
from lxml import html
import urllib


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
        self.get_result(links_list)

    def get_request(self):
        """get request form Google"""
        return requests.get('https://www.google.ru/search', params={'q': self.req_data})

    @staticmethod
    def get_links_from_tree(req_data):
        """create tree from request and get links """
        tree = html.fromstring(req_data.text)
        links = tree.xpath('.//*[@id="ires"]/ol/div/h3[following-sibling::div[@class="s"]]/a/@href')
        return links

    def get_result(self, links_lst):
        """print request result"""
        if not links_lst:
            print 'Sorry, we don\'t find anything!'
        else:
            for link in links_lst[:3]:
                print urllib.unquote(self.garbage_cleaner(link)).decode('utf8')

    @staticmethod
    def garbage_cleaner(link):
        """cleaning links from garb"""
        return link.split('=')[1].replace('&sa', ' ').replace('25', '')


if __name__ == '__main__':
    GS = SearchService()
    GS.find()
