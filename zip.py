"""Zip analog"""


def my_zip(one, two):
    """func wich do the same as zip()"""
    return [(one[i], two[i]) for i in xrange(len(min(one, two)))]


L_1 = [1, 2, 3, 4]
L_2 = ['a', [1, 'b'], 6, 8, 'Kraken']

my_zip(L_1, L_2)