import sys
import re
import requests

from requests.exceptions import ProxyError


def main():
    """check file exist"""
    files = sys.argv[1:]
    while not files:
        print 'Please enter filenames blank by a whitespace.'
        files = raw_input().split()

    ip_for_check = set()
    valid_ip = set()
    for filename in files:
         parse_file(filename, ip_for_check)
    for i in ip_for_check:
        print i
    for addrs in ip_for_check:
        ip_request(addrs, valid_ip)
    # print_result(valid_ip)

def parse_file(name, ip_set):
    try:
        with open(name) as ip_list:
            for line in ip_list:
                parse_string(line, ip_set)
    except:
        print 'Can\'t open!'

def parse_string(line, ip_set):
    ip_val = re.search(r'((\d{1,3}\.){3}\d{1,3}(\s|\S).*\d{1,5})', line)
    if ip_val:
        ip = ''.join(ip_val.group(0).split())
        ip_set.add(ip)


def ip_request(addr, valid_ip_set):
    req_proxy = {
        'http': 'http://{}'.format(addr)
    }
    try:
        test_proxy = requests.get('http://www.microsoft.com/ru-ru/', proxies=req_proxy)
        if test_proxy.ok and 'Microsoft' in test_proxy.text:
            valid_ip_set.add(addr)
        else:
            print 'Nope =('
    except ProxyError:
        pass


if __name__ == '__main__':
    main()