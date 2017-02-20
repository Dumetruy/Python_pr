"""Zip analog"""
L_1 = [1, 2, 3, 4]
L_2 = ['a', [1, 'b'], 6, 8, 'Kraken']
S = [len(L_1) if len(L_1) < len(L_2) else len(L_2)]
L_3 = []
for i in xrange(S[0]):
    L_3.insert(i, (L_1[i], L_2[i]))
print L_3