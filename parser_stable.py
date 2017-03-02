"""This script read strings from server.log file and print top IP/OS"""
import sys
import re


def main(script_arg):
    try:
        file_name = open(script_arg)
        file_name.close()
        addr_dict = {}
        systems_dict = {}
        parse_file(addr_dict, systems_dict, script_arg)
        print_result(addr_dict, 10)
        print_result(systems_dict, 5)
    except IOError:
        print "Make sure the file name or path: {}".format(script_arg)


def parse_file(dict1, dict2, log_name):
    try:
        with open(log_name) as f:
            for line in f:
                os, addr = parse_string(line)
                update_dict(dict1, addr)
                update_dict(dict2, os)
            return dict1, dict2
    except:
        print "Trouble in this file: {}".format(log_name)


def parse_string(line_from_log):
    os_list = ['Metrika', 'Win', 'CrOS', 'Linux', 'FreeBSD', 'Mac OS', 'Slurp', 'Semrush', 'Baiduspider', 'bot', 'coccoc']
    ip_name = line_from_log.split()[0]
    sys_str = re.search(r'\((.+?)\)', line_from_log)
    sys_name = 'Validator'
    if sys_str:
        sys_str = sys_str.group(1)
        for _ in os_list:
            os_name = re.search(r'(.*?{}.*?)(\s|/)'.format(_), sys_str, re.I)
            if os_name:
                sys_name =  os_name.group(1).split()[-1]
                break
    else:
        pass
    return sys_name, ip_name


def update_dict(dict, k):
    if k in dict:
        dict[k] += 1
    else:
        dict[k] = 1
    return dict


def print_result(dict, count):
    sort_dict = sorted(dict.items(), key=lambda (k, v): v, reverse=True)
    print 'Top'.center(23, '-')
    for n, (key, val) in enumerate(sort_dict[:count], start=1):
        print '{}: {} - {}'.format(n, key, val)

if __name__ == '__main__':
    main(sys.argv[1])
