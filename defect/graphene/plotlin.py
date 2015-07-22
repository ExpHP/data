#!/usr/bin/env python3

from pylab import *
from data import Data
from common import clipdomain

fig,ax = subplots(figsize=(5,4.))
ax.set_xscale('linear')
ax.set_yscale('linear')

xlim = (0, 5)
xticks = list(range(6))
ax.set_xlim(*xlim)
ax.set_xticks(xticks)
ax.set_xticklabels([str(int(e)) for e in xticks])

ylim = (1.5, 1.9)
yticks = [1.5,1.6,1.7,1.8,1.9]
ax.set_ylim(*ylim)
ax.set_yticks(yticks)
ax.set_yticklabels(['{:3.1f}'.format(e) for e in yticks])

for path, label in [
	('csv/remove.csv',        'Remove'),
	('csv/multiply-1000.csv', 'R × 1000'),
	('csv/multiply-100.csv',  'R × 100'),
	('csv/multiply-10.csv',   'R × 10'),
	('csv/multiply-5.csv',    'R × 5'),
]:
	data = Data.from_file(path)
	xs = data.ratio * 100
	ys = data.resistance
	xs,ys = clipdomain(xlim, xs, ys)
	ax.plot(xs, ys, '-', lw=2, ms=10, label=label)

ax.set_xlabel('Defect %')
ax.set_ylabel('Resistance (R0)')
ax.legend(loc='upper left')

tight_layout()
fig.savefig('fig/restance-graphene-lin.pdf')
show()

