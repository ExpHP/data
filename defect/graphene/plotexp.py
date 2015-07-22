#!/usr/bin/env python3

from pylab import *
from data import Data
from common import clipdomain

fig,ax = subplots(figsize=(5*1.25,5))
ax.set_xscale('linear')
ax.set_yscale('linear')

xlim = (exp(0), exp(0.30))
#xticks = [1,2,5,10,20,50]
ax.set_xlim(*xlim)
#ax.set_xticks(xticks)
#ax.set_xticklabels([str(int(e)) for e in xticks])

ax.set_ylim(0,25)

for path, label in [
	('csv/remove.csv',        'Remove'),
	('csv/multiply-1000.csv', 'R × 1000'),
	('csv/multiply-100.csv',  'R × 100'),
	('csv/multiply-10.csv',   'R × 10'),
	('csv/multiply-5.csv',    'R × 5'),
]:
	data = Data.from_file(path)
	xs = exp(data.ratio)
	ys = data.resistance
	xs,ys = clipdomain(xlim, xs, ys)
	ax.plot(xs, ys, '-', lw=2, ms=10, label=label)

ax.set_xlabel('exp(defect ratio)')
ax.set_ylabel('Resistance (R0)')
ax.legend(loc='upper left')

tight_layout()
fig.savefig('fig/restance-graphene-exp.pdf')
show()

