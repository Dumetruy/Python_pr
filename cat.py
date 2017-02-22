'''This func should work like as cat'''
S = raw_input()

try:
    my_file = open(S)
    for line in my_file:
        print line

except IOError:
    print 'Sorry we could\'t find your file :' + my_file+'. Try again.'
