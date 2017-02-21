"""Function wich imitate work of xrange"""


def my_own_xrange(start, stop=0, step=1):
    '''Check for stop_ param'''
    count = 0 if stop == 0 else start
    while count < (start if stop == 0 else stop):
        yield count
        count += step

L_3 = ['o', 4, 12, 6, 8]


print [x for x in my_own_xrange(len(L_3,), 40, 4)]
