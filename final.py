# -*- coding: UTF-8 -*-
"""Taking flying info from flyniki.com and combine round-trip tickets"""

import sys
import itertools
from datetime import (datetime, date, timedelta)
from lxml import html
import requests


def main():
    """main func"""
    dest, depart, outbound, return_date = get_usr_data()
    json_resp = post_resp(depart, dest, outbound, return_date)
    flights_lst, currency = get_fly_list(json_resp, return_date)
    sort_by_cost(flights_lst)
    print_results(depart, dest, currency, flights_lst)


def get_usr_data():
    """get user data for flight request"""
    try:
        depart, dest, there_date = sys.argv[1:4]
        depart = depart.upper()
        dest = dest.upper()
        try:
            return_date = sys.argv[4]
            if return_date >= there_date:
                validate_date(return_date)
            else:
                print 'The return date must be equal to or greater than the date of departure'
                exit(0)
        except IndexError:
            return_date = ''
        validate_iata(depart)
        validate_iata(dest)
        validate_date(there_date)
        return dest, depart, there_date, return_date
    except ValueError:
        print "Incorrect flight information, data should blanked by a whitespace: AAA AAA YYYY-MM-DD"
        exit(0)


def validate_iata(iata_code):
    """validating IATA code"""
    if not (iata_code.isalpha() and len(iata_code) == 3):
        print "Incorrect iata-code format, should be AAA"
        exit(0)


def validate_date(date_str):
    """validating date"""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        print 'Incorrect data format, should be YYYY-MM-DD'
        exit(0)
    user_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    today_date = date.today()
    end_date = today_date + timedelta(days=365)
    if today_date >= user_date or user_date > end_date:
        print 'Incorrect date, should be between tomorrow and 365 days ahead'
        exit(0)


def post_resp(dep, dest, there, back):
    """getting JSON from post response with flyght details"""
    oneway = 0 if back else 1
    back = (back or there)
    params = {'departure': dep,
              'destination': dest,
              'outboundDate': there,
              'returnDate': back,
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
                 '_ajax[requestParams][outboundDate]': there,
                 '_ajax[requestParams][returnDate]': back,
                 '_ajax[requestParams][adultCount]': '1',
                 '_ajax[requestParams][childCount]': '0',
                 '_ajax[requestParams][infantCount]': '0',
                 '_ajax[requestParams][openDateOverview]': '0',
                 '_ajax[requestParams][oneway]': oneway}

    session = requests.Session()
    sid = get_sid(session.get('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                              params=params, headers=headers))
    return session.post('http://www.flyniki.com/ru/booking/flight/vacancy.php',
                        params={'sid': sid}, data=body_data).json()


def get_sid(req_url):
    """get valid sid from get request"""
    return req_url.url.split('=')[1].encode('utf8')


def get_fly_list(json_data, return_date):
    """getting the list of flight infos and the currency"""
    try:
        tree = html.fromstring(json_data[u'templates'][u'main'])
        outbound_lst = get_data(get_table(tree, 'outbound'))
        curr = get_currency(tree).strip()
        if return_date:
            return_lst = get_data(get_table(tree, 'return'))
            return get_product(outbound_lst, return_lst), curr
        else:
            return outbound_lst, curr
    except KeyError:
        print "There's now flight with this data, please try with another one!"
        exit(0)


def get_table(tree, flight_table):
    """get specific outbound/return flight table rows"""
    return tree.xpath('.//*[@class="{} block"]//tr[attribute::role]'.format(flight_table))


def get_data(tree_elem):
    """get information from flight table"""
    fly_lst = []
    for element in tree_elem:
        for elem in element.xpath('td/label/div[1]/span'):
            fly_dict = dict()
            fly_info_lst = elem.xpath('@title')[0].split(',')
            class_cost_lst = fly_info_lst[3].split(':')
            fly_dict['dep/arv'] = fly_info_lst[1].strip()
            fly_dict['dur'] = fly_info_lst[2].strip()
            fly_dict['class'] = class_cost_lst[0].strip()
            fly_dict['cost'] = float_val(class_cost_lst[1].strip())
            fly_lst.append(fly_dict)
    return fly_lst


def float_val(str_val):
    """convert cost value from str to float"""
    return float(str_val.replace('.', '').replace(',', '.'))


def get_product(dict_there, dict_back):
    """combine round-trip tickets by flight class"""
    product_tuple = itertools.product(dict_there, dict_back)
    variant_list = []
    for variant in product_tuple:
        count_sum = variant[0]['cost'] + variant[1]['cost']
        variant_list.append({'flights': variant, 'cost': count_sum})
    return variant_list


def get_currency(tree):
    """get currency of current request"""
    try:
        return tree.xpath('.//*[@class="outbound block"]//th[attribute::id][1]/text()')[0].encode('utf8')
    except (IndexError, AttributeError):
        print "There's now flights with this data, please try with another one!"
        exit(0)


def sort_by_cost(unsorted_item):
    """sorting flight list"""
    unsorted_item.sort(key=lambda k: k['cost'])


def print_results(depart, dur, curr, sorted_flights):
    """printing results"""
    head_template = 'From: {} To: {} Currency:{}'
    fish_str = 'Depart/Arrive:{dep/arv} Duration:{dur} Cost:{cost} Class:{class}'
    flight = 'Flight #{}'
    for idx, item in enumerate(sorted_flights):
        if len(item) != 4:
            print head_template.format(depart, dur, curr).center(180, ' ')
            print flight.format(idx).center(180, ' ')
            out_fly = item['flights'][0]
            ret_fly = item['flights'][1]
            print fish_str.format(**out_fly), '<<< THERE == BACK >>>', fish_str.format(**ret_fly)
        else:
            print head_template.format(depart, dur, curr).center(75, ' ')
            print flight.format(idx).center(75, ' ')
            print fish_str.format(**item)


if __name__ == "__main__":
    main()
