"""first 3 link from Google request"""
import sys
import re
import requests
from lxml import html


def main():
    """get args and choose search eng"""
    search_args = ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
    if not search_args:
        while not search_args:
            print 'Please enter your request blanked by a whitespace.'
            search_args = raw_input()

    print 'Please choose the engine: 1 - Google | 2 - Yandex'
    choice = raw_input()
    try:
        eng = {1: ['https://www.google.ru/search?q=', './/*[@id="ires"]/ol/div/h3/a/@href'],
               2: ['https://www.google.ru/search?q=', './/*[@id="ires"]/ol/div/h3/a/@href']}
        search_service = SearchService(eng[int(choice)][0], eng[int(choice)][1])
        search_service.find(search_args)
    except (KeyError, ValueError):
        print "Wrong engine!"
        main()


class SearchService(object):
    """searching in diff search engines"""
    def __init__(self, req_engine, xpath):
        """get engine"""
        self.req_engine = req_engine
        self.xpath = xpath

    def find(self, request):
        """main method"""
        req_data = self.get_request(request)
        links_list = self.get_links_from_tree(req_data)
        self.get_result(links_list, request)

    def get_request(self, search_text):
        """get request form Google"""
        page_data = requests.get('{}{}'.format(self.req_engine, search_text))
        return page_data

    def get_links_from_tree(self, req_data):
        """create tree from str and get links"""
        tree = html.fromstring(req_data.text)
        links = tree.xpath('{}'.format(self.xpath))
        if links:
            return links
        else:
            print 'Sorry, we don\'t find anything!'
            exit(0)

    def get_result(self, links, request_name):
        """print request result"""
        print 'Links for request {}'.format(request_name).center(51, '-')
        ind = 0
        for link in links:
            val_link = self.get_val_url(link)
            if ind != 3 and val_link:
                print '{} - {}'.format(ind+1, val_link)
                ind += 1

    @staticmethod
    def get_val_url(link):
        """get valid link from str"""
        val_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]'
                             r'|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        link = link.replace('&sa', ' ').replace('25', '')
        val_link = re.findall(val_url, link)
        if val_link:
            return val_link[0]


if __name__ == '__main__':
    main()
