#!/usr/bin/env python3

import csv, json, gzip
import numpy as np
import argparse

DESC = '''
Prepare raw data into a form more suitable for plots.

Output is a RFC-4180 compatible CSV file, encoded in UTF-8.
The file will include column headers.
'''

def main():
	parser = argparse.ArgumentParser(description=DESC, formatter_class=argparse.RawDescriptionHelpFormatter)
	parser.add_argument('inpath', help='Path to a structured JSON file or GZ from the defect trial runner')
	parser.add_argument('outpath', help='Path for output file')

	args = parser.parse_args()

	Data.from_raw(args.inpath).to_file(args.outpath)

class Data:
	def __init__(self, count, ratio, resistance):
		self.count = count
		self.ratio = ratio
		self.resistance = resistance

	@classmethod
	def from_raw(cls, path):
		''' Create from raw data. '''
		with gzip_open(path) as f:
			info = json.load(f)
		trials = info['trials']

		count = trialset_defects(trials)
		ratio = count / trialset_num_defects_possible(trials)
		resistance = trialset_resistance(trials)
		return cls(count, ratio, resistance)

	@classmethod
	def from_file(cls, path):
		''' Load from a prepared data file. '''
		with gzip_open(path, encoding='utf-8') as f:
			lines = list(csv.reader(f))
		_ = lines.pop(0) # Headings
		mat = np.array(lines, dtype=float)
		count, ratio, resistance = mat.transpose()
		return cls(count, ratio, resistance)

	def to_file(self, path):
		''' Save to a prepared data file. '''
		cols = [self.count, self.ratio, self.resistance]
		mat = np.vstack(cols).transpose()
		with gzip_open(path, 'w', encoding='utf-8') as f:
			writer = csv.writer(f)
			writer.writerow(['Defect count','Defect ratio','Resistance (R0)'])
			for row in mat.tolist():
				writer.writerow(row)

def gzip_open(path, mode=None, compresslevel=9, buffering=-1, closefd=True, opener=None, **kwargs):
	''' Open a file which may optionally be gzipped (by extension). '''
	# Note we explicitly forward any args that only apply to one of the methods
	if path.lower().endswith('.gz'):
		if mode is None: mode = 'rt' # always default to text
		return gzip.open(path, mode, compresslevel=compresslevel, **kwargs)
	else:
		if mode is None: mode = 'r'
		return open(path, mode, buffering=buffering, closefd=closefd, opener=opener, **kwargs)

def trialset_resistance(trials):
	currents = [x['steps']['current'] for x in trials]
	currents = np.array(currents)
	current_mean = np.array(currents).mean(axis=0)
	return 1./current_mean

def trialset_defects(trials):
	deleteds = [x['steps']['deleted'] for x in trials]
	counts = [list(map(len, x)) for x in deleteds]
	count = smash_equal(*counts)
	total = prefix_sums(count)
	return np.array(list(total))

def trialset_num_defects_possible(trials):
	return trials[0]['graph']['num_vertices']-2

def smash_equal(it, *others):
	''' checks that the input iterables match and returns one. '''
	it = list(it)
	if any(list(o) != it for o in others):
		raise ValueError('Lists not equal')
	return it

def prefix_sums(it):
	s = 0
	for x in it:
		s += x
		yield s

if __name__ == '__main__':
	main()

