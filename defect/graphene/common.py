from pylab import *

def clipdomain(xlim, x, *others):
	lo,hi = xlim
	mask = logical_or(x < lo, hi < x)
	indices = nonzero(mask)
	return [delete(x, indices)] + [delete(y, indices) for y in others]

