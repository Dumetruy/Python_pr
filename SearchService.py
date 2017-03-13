"""first 3 link from Google"""
import sys
import requests
from lxml import html


class SearchService(object):
    """Google searching service class"""
    def __init__(self):
        """create exemplar for curr req and check input"""
        search_str = ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
        self.req_data = search_str
        if not self.req_data:
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
        params_dict = {'q': self.req_data}
        return requests.get('https://www.google.ru/search', params=params_dict)

    @staticmethod
    def get_links_from_tree(req_data):
        """create tree from request and get links """
        tree = html.fromstring(req_data.text)
        links = tree.xpath('.//*[@id="ires"]/ol/div/h3[following-sibling::div[@class="s"]]/a/@href')
        if links:
            return links
        else:
            print 'Sorry, we don\'t find anything!'
            exit(0)

    def get_result(self, links_lst):
        """print request result"""
        for link in links_lst[:3]:
            print self.garbage_cleaner(link)

    @staticmethod
    def garbage_cleaner(link):
        """cleaning links from garb"""
        val_link = link.split('=')[1].replace('&sa', ' ').replace('25', '')
        return val_link


if __name__ == '__main__':
    GS = SearchService()
    GS.find()
