def Sq(numb):
    return ([i ** 2 for i in numb])

def Sec(numb):
    return ([i for i in numb[::2]])

def Sq_c(numb):
    return [i for i in numb[1::2] if i % 2 == 0]

L_1 = [1, 3, 5, 6, 4, 11, 13, 14, 3, 8]

print Sq_c(L_1)
