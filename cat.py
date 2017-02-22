'''This func should work like as cat'''
import sys
param = sys.argv[1:]

def cat_like(param):
    for x in param:
        try:
            with open( x, 'r') as f:
                print f.read()
        except IOError:
            print "Try again"
cat_like(param)
