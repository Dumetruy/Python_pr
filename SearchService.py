"""first 3 link from diff Searching Services"""
import sys
import re
import requests
from lxml import html


class SearchService(object):
    """diff searching service class"""
    def __init__(self):
        """create exemplar for curr searching service"""
        self.search_args = ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
        if not self.search_args:
            while not self.search_args:
                print 'Please enter your request blanked by a whitespace.'
                self.search_args = raw_input()
        self.find()


    def find(self):
        """main method"""
        req_data = self.get_request(self.search_args)
        links_list = self.get_links_from_tree(req_data)
        self.get_result(links_list, self.search_args)

    def get_request(self, search_text):
        """get request form searching service"""
        page_data = requests.get('{}{}'.format('https://www.google.ru/search?q=', search_text))
        return page_data

    def get_links_from_tree(self, req_data):
        """create tree from request and get links """
        tree = html.fromstring(req_data.text)
        links = tree.xpath('.//*[@id="ires"]/ol/div/h3/a/@href')
        if links:
            return links
        else:
            print 'Sorry, we don\'t find anything!'
            exit(0)

    def get_result(self, links_lst, request):
        """print request result"""
        print 'Links for request {}'.format(request).center(51, '-')
        ind = 0
        for link in links_lst:
            val_link = self.garb_cleaner(link)
            if ind != 3 and val_link:
                print '{} - {}'.format(ind+1, val_link)
                ind += 1

    @staticmethod
    def garb_cleaner(link):
        """cleaning links from garb"""
        val_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                             r'|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        link = link.replace('&sa', ' ').replace('25', '')
        val_link = re.findall(val_url, link)
        if val_link:
            return val_link[0]


if __name__ == '__main__':
    search_service = SearchService()
