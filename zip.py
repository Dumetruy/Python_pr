"""Zip analog"""


def my_zip(one, two):
    """func wich do the same as zip()"""
    less = [len(one) if len(one) < len(two) else len(two)]
    new_l = []
    for i in xrange(less[0]):
        new_l.insert(i, (one[i], two[i]))
    return new_l


L_1 = [1, 2, 3, 4]
L_2 = ['a', [1, 'b'], 6, 8, 'Kraken']

my_zip(L_1, L_2)
