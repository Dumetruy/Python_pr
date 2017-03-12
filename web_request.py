"""first 3 link from Google request"""
import sys
import re
import requests
from lxml import html


def main():
    """check file exist, create sets, init other functions"""
    search_args = ' '.join(sys.argv[1:]).decode('cp1251').encode('utf8')
    print search_args
    if not  search_args:
        while not search_args:
            print 'Please enter filenames blanked by a whitespace or' \
                  ' compose with \'+\' if it\'s one query.'
            search_args = raw_input().split(' ')

    for arg in search_args:
        req_data = get_request(arg)
        links_list = get_links_from_tree(req_data)
        req_results(links_list, arg)


def get_request(search_text):
    """get request form Google"""
    try:
        page_data = requests.get('https://www.google.ru/search?q={}'.format(search_text))
        return page_data
    except UnicodeDecodeError:
        get_request(search_text.decode('cp1251'))


def get_links_from_tree(req_data):
    """create tree from str and get links"""
    tree = html.fromstring(req_data.text)
    links = tree.xpath('.//*[@id="ires"]/ol/div/h3/a/@href')
    if links:
        return links
    else:
        print 'Sorry, we don\'t find anything!'
        exit(0)


def req_results(links, request_name):
    """print results from request"""
    val_url = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    print 'Links for request {}'.format(request_name).center(51, '-')
    ind = 0
    for link in links:
        if ind != 3:
            link = link.replace('&sa', ' ').replace('25', '')
            val_link = re.findall(val_url, link)
            if val_link:
                print '{} - {}'.format(ind+1, val_link[0])
                ind += 1
        else:
            break


if __name__ == '__main__':
    main()
