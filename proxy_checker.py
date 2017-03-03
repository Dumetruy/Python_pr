import sys

def main():
    """check file exist"""
    files = sys.argv[1:]
    while not files:
        print 'Please enter filenames blank by a whitespace.'
        files = raw_input().split()

    ip_for_check = set()
    valid_ip = set()
    for filename in files:
        addr = parse_file(filename, ip_for_check)
        if addr:
            ip_for_check.add(addr)

    ip_request(ip_for_check, valid_ip)
    print_result(valid_ip)


if __name__ == '__main__':
    main()