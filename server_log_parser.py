"""This script read strings from server.log file and print top IP/OS"""
import sys
import re


def get_data(data_from_re_str):
    """This func extract data from re.obj"""
    os_name = data_from_re_str.group(3).split(';')[0].split()[0]
    ip_adr = data_from_re_str.group(1)
    return ip_adr, os_name


def dict_checker(ip_os_list):
    """This increment oe add specific IP/OS"""
    if ip_os_list[0] in IP_DICT:
        IP_DICT[ip_os_list[0]] += 1
    else:
        IP_DICT[ip_os_list[0]] = 1
    if ip_os_list[1] in OS_DICT:
        OS_DICT[ip_os_list[1]] += 1
    else:
        OS_DICT[ip_os_list[1]] = 1
        return IP_DICT, OS_DICT


def dic_parser(raw_dict, top_count):
    """This func check for len of dict and print sorted one"""
    if top_count <= len(raw_dict):
        for i in xrange(top_count):
            sort_dict = sorted(raw_dict.items(), key=lambda (k, v): v, reverse=True)[i]
            print '{}: {} - {}'.format(i+1, *sort_dict)
    else:
        print 'This dict has only {} records, please enter valid Top number!'.format(len(raw_dict))


if __name__ == '__main__':
    OS_DICT = {}
    IP_DICT = {}
    try:
        with open(sys.argv[1]) as f:
            for lines in f:
                my_str = re.match(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+?(\((.+?)\))', lines)
                if my_str:
                    dict_checker(get_data(my_str))

    except IOError:
        print "Make sure the file name or path: {}".format(sys.argv[1])

    print '------IP Top------'
    dic_parser(IP_DICT, 10)
    print '------OS Top------'
    dic_parser(OS_DICT, 5)
