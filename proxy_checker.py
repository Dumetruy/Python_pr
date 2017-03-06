"""script parse files for proxy ip/port & check it"""
import sys
import re
import requests

from requests.exceptions import (ProxyError, ConnectionError, ConnectTimeout,
                                 ReadTimeout, TooManyRedirects, ChunkedEncodingError)


def main():
    """check file exist, create sets, init other func"""
    files = sys.argv[1:]
    while not files:
        print 'Please enter filenames blanked by a whitespace.'
        files = raw_input().split()

    ip_for_check = set()
    valid_ip = set()
    for filename in files:
        parse_file(filename, ip_for_check)
    for addr in ip_for_check:
        response(addr, valid_ip)
    print_result(valid_ip)


def parse_file(file_name, ip_set):
    """trying to open file and takes lines"""
    try:
        with open(file_name) as ip_list:
            for line in ip_list:
                parse_string(line, ip_set)
    except IOError:
        print 'Sorry can\'t open file {}, please check ' \
              'its availability or existence!'.format(file_name)


def parse_string(line, ip_set):
    """parsing string for correct ip:port"""
    ip_val = re.search(r'((\d{1,3}\.){3}\d{1,3}(\s|\S).*\d{1,5})', line)
    if ip_val:
        ip_set.add(''.join(ip_val.group(0).split()))


def response(ip_port, valid_ip_set):
    """requesting proxy from ip_set"""
    req_proxy = {
        'http': 'http://{}'.format(ip_port)
    }
    try:
        test_proxy = requests.get('http://www.microsoft.com/ru-ru/',
                                  proxies=req_proxy, timeout=1)
        if test_proxy.ok and 'Microsoft' in test_proxy.text:
            valid_ip_set.add(ip_port)
    except (ProxyError, ConnectTimeout, ReadTimeout, ConnectionError,
            TooManyRedirects, ChunkedEncodingError):
        pass


def print_result(valid_ip):
    """printing results in file"""
    if valid_ip:
        with open('valid_ip.txt', 'w') as valid_list:
            valid_list.write('\n'.join(valid_ip))
    else:
        print "Sorry, there's no good proxy addresses!"


if __name__ == '__main__':
    main()
