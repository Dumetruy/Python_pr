import requests
from lxml import html
import sys


def prot1():
    """check file exist, create sets, init other functions"""
    #files = sys.argv[1:]
    #while not files:
        #print 'Please enter filenames blanked by a whitespace.'
        #files = raw_input().split()

    page = requests.get('https://www.google.ru/search?q=how+i+met+your+mother')
    #with open('2.html', 'w') as f:
        #f.write(page.text.encode('utf8'))
    tree = html.fromstring(page.text.encode('utf8'))
    first_link = tree.xpath('.//*[@id="ires"]/ol/div/h3/a/@href')
    for i in first_link:
        print i.encode('utf8')
    #print len(first_link)
    #print first_link


if __name__=='__main__':
    prot1()
