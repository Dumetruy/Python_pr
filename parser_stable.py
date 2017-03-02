"""This script read strings from server.log file and print top IP/OS"""
import sys
import re


def main():
    """create 2 dict, check sys.arg[1], init other func"""
    try:
        script_arg = sys.argv[1]
    except IndexError:
        print "Please enter an argument!"
        return

    ip_dict = {}
    systems_dict = {}
    parse_file(ip_dict, systems_dict, script_arg)
    print_result(ip_dict, 10)
    print_result(systems_dict, 5)


def parse_file(dict_adr, dict_sys, log_name):
    """try to open file, recieve lines to parse_string finc"""
    try:
        with open(log_name) as open_file:
            for line in open_file:
                sys_name, addr = parse_string(line)
                update_dict(dict_adr, addr)
                update_dict(dict_sys, sys_name)
            return dict_adr, dict_sys
    except IOError:
        print "Can't open {}".format(log_name)
        exit(1)


def parse_string(line_from_log):
    """takes ip_addr and OS names/bots from lines"""
    os_list = ['Metrika', 'Win', 'CrOS', 'Linux', 'FreeBSD',
               'Mac', 'Slurp', 'Semrush', 'Baiduspider', 'bot', 'coccoc']
    ip_name = line_from_log.split()[0]
    sys_str = re.search(r'\((.+?)\)', line_from_log)
    sys_name = 'Validator'
    if sys_str:
        sys_str = sys_str.group(1)
        for item in os_list:
            os_name = re.search(r'(.*?{}.*?)(\s|/)'.format(item), sys_str, re.I)
            if os_name:
                sys_name = os_name.group(1).split()[-1].replace(';', '').replace('Macintosh', 'Mac')
                break
    return sys_name, ip_name


def update_dict(up_dict, key):
    """Func that update specific dict"""
    if key in up_dict:
        up_dict[key] += 1
    else:
        up_dict[key] = 1
    return up_dict


def print_result(res_dict, count):
    """print results from specific dict"""
    sort_dict = sorted(res_dict.items(), key=lambda (k, v): v, reverse=True)
    print 'Top'.center(23, '-')
    for num, (key, val) in enumerate(sort_dict[:count], start=1):
        print '{}: {} - {}'.format(num, key, val)


if __name__ == '__main__':
    main()
