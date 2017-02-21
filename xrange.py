"""Function wich imitate work of xrange"""


def my_own_xrange(start_, stop_=0, step_=1):
    '''Check for stop_ param'''
    if stop_ == 0:
        count = 0
        while count < start_:
            yield count
            count += step_

    else:
        count = start_
        while count < stop_:
            yield count
            count += step_


L_3 = ['o', 4, 12, 6, 8]


print [x for x in my_own_xrange(len(L_3,), 40, 4)]
