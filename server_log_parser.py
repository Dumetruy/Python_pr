import sys
import re


def str_parser(filename):
    with open(filename) as current_file:
        for line in current_file:
            parsed_str = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.+)(\(.+\))', line)
            ip_adr = parsed_str.group(1)
            os_name = parsed_str.group(3).split(';')[0]
            return ip_adr, os_name


if __name__ == '__main__':
    dict_os = {}
    dict_ip = {}
    str_parser(sys.argv[1])
