# -*- coding: UTF-8 -*-
"""Taking flying info from flyniki.com and combine round-trip tickets"""

import sys
import itertools
import datetime
from lxml import html
import requests


def main():
    """main func"""
    dest, dep, outbound, oneway, return_date = get_usr_data()
    json_resp = post_resp(dep, dest, outbound, return_date, oneway)
    flights_lst, curr = get_fly_list(json_resp, return_date)
    get_sorted(flights_lst)
    print_results(dep, dest, curr, flights_lst)


def get_usr_data():
    """get user data for flight request"""
    try:
        depart, dest, out_date = sys.argv[1:4]
        try:
            return_date = sys.argv[4]
            oneway = 0
            validate_date(return_date)
        except IndexError:
            return_date = ''
            oneway = 1
        validate_iata(depart)
        validate_iata(dest)
        validate_date(out_date)
        return dest, depart, out_date, oneway, return_date
    except ValueError:
        print "Incorrect flight information, data should blanked by a whitespace"
        exit(0)


def validate_iata(iata_code):
    """validating IATA code"""
    if not (iata_code.isalpha() and len(iata_code) == 3 and iata_code.isupper()):
        print "Incorrect iata-code format, should be AAA, case-sensitive"
        exit(0)


def validate_date(date_str):
    """validating date"""
    try:
        datetime.datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print 'Incorrect data format, should be YYYY-MM-DD'
        exit(0)


def post_resp(dep, dest, out, back, onew):
    """getting JSON from post response with flyght details"""
    para = {'departure': dep,
            'destination': dest,
            'outboundDate': out,
            'returnDate': back,
            'oneway': onew,
            'adultCount': '1'}
    user_id = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
        }
    body_data = {'_ajax[templates][]': ['main', 'priceoverview', 'infos', 'flightinfo'],
                 '_ajax[requestParams][departure]': dep,
                 '_ajax[requestParams][destination]': dest,
                 '_ajax[requestParams][returnDeparture]': '',
                 '_ajax[requestParams][returnDestination]': '',
                 '_ajax[requestParams][outboundDate]': out,
                 '_ajax[requestParams][returnDate]': back,
                 '_ajax[requestParams][adultCount]': '1',
                 '_ajax[requestParams][childCount]': '0',
                 '_ajax[requestParams][infantCount]': '0',
                 '_ajax[requestParams][openDateOverview]': '0',
                 '_ajax[requestParams][oneway]': onew}

    session = requests.Session()
    val_sid = get_sid(session.get('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                                  params=para, headers=user_id))
    return session.post('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                        params={'sid': val_sid}, data=body_data).json()


def get_sid(req_url):
    """get valid sid from get request"""
    return req_url.url.replace('=', ' ').split()[1].encode('utf8')


def get_fly_list(json_data, return_date):
    """getting the list of flight infos and the currency"""
    try:
        tree = html.fromstring(json_data[u'templates'][u'main'])
        outbound_lst = get_data(get_table(tree, 'outbound'))
        curr = get_currency(tree).encode('utf8')
        if return_date:
            return get_product(outbound_lst, get_data(get_table(tree, 'return'))), curr
        else:
            return outbound_lst, curr
    except (IndexError, KeyError):
        print "There's now flight with this data, please try with another one!"
        exit(0)


def get_table(tree, flight_table):
    """get specific outbound/return flight table"""
    return tree.xpath('.//*[@class="{} block"]//tr[attribute::role]'.format(flight_table))


def get_data(tree_elem):
    """get information from flight table"""
    fly_lst = []
    for element in tree_elem:
        dur, dep_ar = get_dur_dep(element)
        for elem in element.xpath('td/label/div[1]/span'):
            fly_dict = dict()
            fly_dict['D/A'] = dep_ar
            fly_dict['Dur'] = dur
            fly_dict['Cls'] = ' '.join(elem.xpath('@title')[0].replace(':', '').split(' ')[7:9])
            fly_dict['Cst'] = float_val(elem.xpath('text()')[0])
            fly_lst.append(fly_dict)
    return fly_lst


def get_dur_dep(tree_elem):
    """get duration and dep/arr information"""
    duration = tree_elem.xpath('td[4]/span/text()')[0].replace(' ', '')
    dep = str(tree_elem.xpath('string(td[2]/span)').replace(' ', '').replace(u'\u2013', '-'))
    return duration, dep


def float_val(str_val):
    """convert cost value from str to float"""
    return float(str_val.replace('.', '').replace(',', '.'))


def get_product(dict_there, dict_back):
    """combine round-trip tickets by flight class"""
    product_tuple = itertools.product(dict_there, dict_back)
    variant_list = []
    for variant in product_tuple:
        count_sum = variant[0]['Cst'] + variant[1]['Cst']
        variant_list.append((variant, count_sum))
    return variant_list


def get_currency(tree):
    """get currency of current request"""
    return tree.xpath('.//*[@class="outbound block"]//th[attribute::id]'
                      '[1]/text()')[0].replace(' ', '')


def get_sorted(unsorted_item):
    """sorting flight list"""
    if isinstance(unsorted_item[0], dict):
        unsorted_item.sort(key=lambda k: k['Cst'])
    else:
        unsorted_item.sort(key=lambda (k, v): v)


def print_results(dep, dest, curr, sort_lst):
    """printing results"""
    print 'From: {} To: {} Currency:{}\n'.format(dep, dest, curr).center(40, ' ')
    for idx, item in enumerate(sort_lst):
        print 'Flight #{}'.format(idx).center(35, ' ')
        try:
            print '{} - Depp/Arr - {}'.format(item[0][0]['D/A'], item[0][1]['D/A']).center(40, ' ')
            print '{} - Duration - {}'.format(item[0][0]['Dur'], item[0][1]['Dur']).center(40, ' ')
            print '{} - Cost - {}'.format(item[0][0]['Cst'], item[0][1]['Cst']).center(40, ' ')
            print '{} - Class - {}'.format(item[0][0]['Cls'], item[0][1]['Cls']).center(40, ' ')
            print 'Total: {}\n'.format(item[1]).center(40, ' ')
        except KeyError:
            print 'Depp/Arr - {}'.format(item['D/A'])
            print 'Duration - {}'.format(item['Dur'])
            print 'Cost - {}'.format(item['Cst'])
            print 'Class - {}\n'.format(item['Cls'])


if __name__ == "__main__":
    main()
