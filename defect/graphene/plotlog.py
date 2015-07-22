#!/usr/bin/env python3

from pylab import *
from data import Data
from common import clipdomain

fig,ax = subplots(figsize=(5*1.25,5))
ax.set_xscale('log')
ax.set_yscale('log')

xlim = (0.5, 55.0)
xticks = [1,2,5,10,20,50]
ax.set_xlim(*xlim)
ax.set_xticks(xticks)
ax.set_xticklabels([str(int(e)) for e in xticks])

for path, label in [
	('csv/remove.csv',        'Remove'),
	('csv/multiply-1000.csv', 'R × 1000'),
	('csv/multiply-100.csv',  'R × 100'),
	('csv/multiply-10.csv',   'R × 10'),
	('csv/multiply-5.csv',    'R × 5'),
]:
	data = Data.from_file(path)
	xs = data.ratio * 100.
	ys = data.resistance
	xs,ys = clipdomain(xlim, xs, ys)
	ax.plot(xs, ys, '-', lw=2, ms=10, label=label)

ax.set_xlabel('Defect %')
ax.set_ylabel('Resistance (R0)')
#ax.legend(loc='upper left')

tight_layout()
fig.savefig('fig/restance-graphene-log.pdf')
show()

