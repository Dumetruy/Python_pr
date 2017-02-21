"""Few little-func wich do smth"""

def square_each(numb):
    """Func wich get square of each element from the list"""
    return [i ** 2 for i in numb]


def only_even_elem(numb):
    """Func wich get each element from even position in the list"""
    return [i for i in numb[::2]]


def square_odd_even(numb):
    """Func wich get square of each even element from odd position in the list"""
    return [i**2 for i in numb[1::2] if i % 2 == 0]

L_1 = [1, 3, 5, 6, 4, 11, 13, 14, 3, 8]

print square_each(L_1)
