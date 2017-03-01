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
    except IOError:
        print "Make sure the file name or path: {}".format(script_arg)

def parse_file(dict1, dict2, log_name):
    try:
        with open(log_name) as f:
            for line in f:
                addr, os = parse_string(line)
                print addr
                print os
    except IOError:
        print "Make sure the file name or path: {}".format(log_name)


def parse_string(line_from_log):
    sys_pattern = ['Win']
    ip_name = line_from_log.split()[0]
    raw_str = re.search(r'\((.+?)\)', line_from_log)
    my_str = raw_str.group(1)
    for _ in sys_pattern:
        temp_sys = re.search(r'(^|\s)(Win(\s+|\S+))', my_str)
        if temp_sys:
            return ip_name, temp_sys.group(2)

if __name__ == '__main__':
    main(sys.argv[1])