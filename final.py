# -*- coding: UTF-8 -*-
"""Flight search on flyniki.com"""

import argparse
import itertools
from datetime import datetime, date, timedelta

from lxml import html
import requests


def main():
    """main func"""
    depart, dest, outbound, return_date = get_user_data()
    json_resp = get_json_data(depart, dest, outbound, return_date)
    flights_lst, currency = get_fly_list(json_resp, return_date)
    print_results(depart, dest, currency, flights_lst)


def get_user_data():
    """get user data for flight request"""
    parser = argparse.ArgumentParser(description='Type your data with whitespace in following format')
    parser.add_argument('depart_iata', type=str, help='AAA')
    parser.add_argument('dest_iata', type=str, help='AAA')
    parser.add_argument('depart_date', type=str, help='YYYY-MM-DD')
    parser.add_argument('return_date', nargs='?', default='', help='YYYY-MM-DD - optional')
    args = parser.parse_args()
    validate_iata(args.depart_iata, args.dest_iata)
    validate_date(args.depart_date, args.return_date)
    return args.depart_iata, args.dest_iata, args.depart_date, args.return_date


def validate_iata(*iata_codes):
    """validating IATA code"""
    for code in iata_codes:
        iata_code = code.upper()
        if not (iata_code.isalpha() and len(iata_code) == 3):
            print "Incorrect iata-code format, should be AAA"
            exit(1)
    return iata_codes


def validate_date(depart_date, return_date):
    """validating date"""
    try:
        depart_date = datetime.strptime(depart_date, "%Y-%m-%d").date()
        today_date = date.today()
        end_date = today_date + timedelta(days=365)
        if today_date >= depart_date or depart_date > end_date:
            print 'Incorrect date, should be between tomorrow and 365 days ahead'
            exit(1)
        if return_date:
            return_date = datetime.strptime(return_date, "%Y-%m-%d").date()
            if return_date <= depart_date:
                print 'The return date must be equal or greater than the date of departure'
                exit(1)
            return depart_date, return_date
        return depart_date
    except ValueError:
        print 'Incorrect data format, should be YYYY-MM-DD'
        exit(1)


def get_json_data(dep, dest, depart_date, return_date):
    """getting JSON from post response with flyght details"""
    oneway = 0 if return_date else 1
    return_date = (return_date or depart_date)
    params = {'departure': dep,
              'destination': dest,
              'outboundDate': depart_date,
              'returnDate': return_date,
              'oneway': oneway,
              'adultCount': '1'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    body_data = {'_ajax[templates][]': ['main', 'priceoverview', 'infos', 'flightinfo'],
                 '_ajax[requestParams][departure]': dep,
                 '_ajax[requestParams][destination]': dest,
                 '_ajax[requestParams][returnDeparture]': '',
                 '_ajax[requestParams][returnDestination]': '',
                 '_ajax[requestParams][outboundDate]': depart_date,
                 '_ajax[requestParams][returnDate]': return_date,
                 '_ajax[requestParams][adultCount]': '1',
                 '_ajax[requestParams][childCount]': '0',
                 '_ajax[requestParams][infantCount]': '0',
                 '_ajax[requestParams][openDateOverview]': '0',
                 '_ajax[requestParams][oneway]': oneway}

    session = requests.Session()
    session.headers.update(headers)
    sid = get_sid(session, params)
    return session.post('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                        params={'sid': sid}, data=body_data).json()


def get_sid(session, params):
    """get valid sid from get request"""
    request = session.get('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                          params=params)
    return request.url.split('=')[1].encode('utf8')


def get_fly_list(json_data, return_date):
    """getting the list of flight infos and the currency"""
    try:
        tree = html.fromstring(json_data['templates']['main'])
        outbound_flights = get_data(get_flights_trs(tree, 'outbound'))
        curr = get_currency(tree).strip()
        if return_date:
            return_flights = get_data(get_flights_trs(tree, 'return'))
            return get_flights_variants(outbound_flights, return_flights), curr
        else:
            return outbound_flights, curr
    except KeyError:
        print "There's no flight with this data, please try with another one!"
        exit(1)


def get_flights_trs(tree, flight_table):
    """get specific outbound/return flight table rows"""
    return tree.xpath('.//*[@class="{} block"]//tr[attribute::role]'.format(flight_table))


def get_data(tree_elem):
    """get information from flight table"""
    fly_lst = []
    for element in tree_elem:
        for elem in element.xpath('td/label/div[1]/span'):
            fly_dict = dict()
            fly_info_lst = [item.strip() for item in elem.xpath('@title')[0].split(',')]
            class_cost_lst = fly_info_lst[3].split(':')
            fly_dict['dep/arv'] = fly_info_lst[1]
            fly_dict['dur'] = fly_info_lst[2]
            fly_dict['class'] = class_cost_lst[0]
            fly_dict['cost'] = get_price(class_cost_lst[1])
            fly_lst.append(fly_dict)
    return fly_lst


def get_price(str_val):
    """convert cost value from str to float"""
    return float(str_val.replace('.', '').replace(',', '.'))


def get_flights_variants(outbound_fl_dict, return_fl_dict):
    """combine round-trip tickets by flight class"""
    product_tuple = itertools.product(outbound_fl_dict, return_fl_dict)
    variant_list = []
    for variant in product_tuple:
        total_sum = variant[0]['cost'] + variant[1]['cost']
        variant_list.append({'flights': variant, 'cost': total_sum})
    return variant_list


def get_currency(tree):
    """get currency of current request"""
    try:
        return tree.xpath('.//*[@class="outbound block"]//th[attribute::id][1]/text()')[0].encode('utf8')
    except (IndexError, AttributeError):
        print "There's now flights with this data, please try with another one!"
        exit(1)


def print_results(iata_depart, iata_dest, curr, flights_list):
    """printing results"""
    flights_list.sort(key=lambda k: k['cost'])
    print 'From: {} To: {}'.format(iata_depart, iata_dest)
    banners_str = 'Depart/Arrive   Duration        Class          Cost'
    fish_str = '{dep/arv} | {dur} | {class} | {cost}'
    flight = '#{}'
    for i, item in enumerate(flights_list):
        if 'flights' in item:
            there_fly = item['flights'][0]
            ret_fly = item['flights'][1]
            print flight.format(i), '\n', banners_str
            print fish_str.format(**there_fly), curr, '\n', fish_str.format(**ret_fly), curr
            print 'Total: {}'.format(item['cost']), curr, '\n'
        else:
            print flight.format(i), '\n', banners_str, '\n', fish_str.format(**item), curr, '\n'


if __name__ == "__main__":
    main()
