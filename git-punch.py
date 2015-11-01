#!/usr/bin/python

import argparse
import subprocess
import json


def get_log_data(author):
	"""
	Function that executes the git commands on a given repository
	and retrieves the git log data
	"""
	command = ['git', 'log',
			   '--no-merges',
			   '--author={}'.format(author),
			   '--pretty=format:%aD']
	try:
		p = subprocess.Popen(command,
		                     stdin=subprocess.PIPE,
		                     stdout=subprocess.PIPE,
		                     stderr=subprocess.PIPE,
		                     universal_newlines=True)
		outdata, errdata = p.communicate()
	except OSError:
		print('Git not installed?')
		exit(-1)

	if outdata == '' and errdata:
		print('Not a git repository?')
		exit(-1)

	return outdata


def write_to_file(data, target):
	"""
	Writes data to target file
	"""
	if data:
		try:
			with open(target, 'w') as outfile:
				json.dump(data, outfile)
				print("Completed writing data to: {}".format(target))
		except IOError:
			print('Could not write data to file')
			exit(-1)


def build_stats(raw_data):
	"""
	Builds statistics table using day of week and hour of day.

	>>> result = build_stats('''Tue, 1 Nov 2015 12:38:23 +0300
	... Tue, 1 Nov 2015 12:32:04 +0300
	... Mon, 1 Nov 2015 02:32:04 +0300''')
	>>> assert result['Tue'][12] == 2
	>>> assert result['Mon'][2] == 1
	"""
	days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

	log = [(x.split(',')[0], x.split(' ')[4].split(':')[0])
		   for x in raw_data.splitlines()]

	# Generates a list of all the days when a commit happened
	# and includes the number of commits at a given hour of the day
	stats = {}
	for day in days:
		stats[day] = {}
		for hour in xrange(0, 24):
			stats[day][hour] = 0

	for day, hour in log:
		stats[day][int(hour)] += 1

	return stats


def build_parser():
	"""
	Builds the argument parser

	usage: git-punch.py [-h] [--author AUTHOR] [--out-file OUTFILE]

	optional arguments:
	  -h, --help			show this help message and exit
	  --author AUTHOR, -a AUTHOR
							filters based on author
	  --out-file OUTFILE, -o OUTFILE
							target output file
	"""
	parser = argparse.ArgumentParser()

	parser.add_argument('--author', '-a',
						dest='author',
						default='',
						help='filters based on author')

	parser.add_argument('--out-file', '-o',
						dest='outfile',
						default='stats.json',
						help='target output file')

	return parser


if __name__ == '__main__':
	args = build_parser().parse_args()
	raw_log = get_log_data(args.author)
	stats = build_stats(raw_log)
	write_to_file(stats, args.outfile)
