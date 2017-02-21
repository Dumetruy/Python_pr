"""Zip analog"""


def my_zip(*args):
    """func wich do the same as zip()"""
    return [tuple(list(arg)[i] for arg in args) for i in xrange(min(map(len, args)))]


L_1 = [1, 2, 3, 4]
L_2 = ['a', [1, 'b'], 6, 8, 'Kraken']
L_3 = ['o', 4, 12, 6, 8]
L_4 = set('Apple')

assert zip(L_1, L_2, L_3, L_4) == my_zip(L_1, L_2, L_3, L_4)

print my_zip(L_1, L_2, L_3, L_4)
