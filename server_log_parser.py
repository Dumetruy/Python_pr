import sys
import re


def get_data(raw_data):
    os_name = my_str.group(4).split(';')[0]
    ip_adr = my_str.group(1)
    return ip_adr, os_name


def dict_checker(raw_data):
    if raw_data[0] in ip_dict:
        ip_dict[raw_data[0]] += 1
    else:
        ip_dict[raw_data[0]] = 1
    if  raw_data[1] in os_dict:
        os_dict[raw_data[1]] += 1
    else:
        os_dict[raw_data[1]] = 1
        return ip_dict, os_dict


def dic_parser(raw_dict, top_count):
    for i in xrange(top_count):
        print sorted(raw_dict.items(), key=lambda (k, v): v, reverse=True)[i]


if __name__ == '__main__':
    os_dict = {}
    ip_dict = {}
    try:
        with open(sys.argv[1]) as f:
            for lines in f:
                my_str = re.match(r'((\d{1,3}\.){3}\d{1,3})(.+)(\((.+)\))', lines)
                dict_checker(get_data(my_str))
    except IOError:
        print "Make sure the file name or path: {}".format(sys.argv[1])


    dic_parser(ip_dict, 2)
    dic_parser(os_dict, 1)
