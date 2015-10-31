#!/usr/bin/python

import sys
import subprocess
import json

# Default config variables
author = ''
output_file_name = 'tmp/data.json'

# Function that executes the git
# commands on a given repository
# and retrieves the git log data
def get_log_data():
	try:
		gitcommand = ['git', 'log', '--no-merges', '--author='+author,  '--pretty=format: %aD']
		p = subprocess.Popen(gitcommand,
		                     stdin=subprocess.PIPE,
		                     stdout=subprocess.PIPE,
		                     stderr=subprocess.PIPE)
		outdata, errdata = p.communicate()
	except OSError as e:
		print('Git not installed?')
		sys.exit(-1)
	if outdata == '':
		print('Not a git repository?')
		sys.exit(-1)
	return outdata

def write_to_file(data):
	if data:
		try:
			with open(output_file_name, 'w') as outfile:
				json.dump(data, outfile)
				print("Completed writing data to: %s", output_file_name)
		except:
			print('Could not write data to file')
			sys.exit(-1)

# Days and Hours listing
days = ['Sat', 'Fri', 'Thu', 'Wed', 'Tue', 'Mon', 'Sun']
hours = ['12am'] + [str(x) for x in xrange(1, 12)] + ['12pm'] + [str(x) for x in xrange(1, 12)]

# Cleanup the git log data
temp_log = get_log_data()
data_log = [[x.strip().split(',')[0], x.strip().split(' ')[4].split(':')[0]] for x in temp_log.split('\n')]

# Generates a list of all the
# days when a commit happened
# and includes the number of
# commits at a given hour
# of the day
stats = {}
for d in days:
	stats[d] = {}
	for h in xrange(0, 24):
		stats[d][h] = 0

# Calculates the total sum
# of overall commits for the
# project
total = 0
for line in data_log:
	stats[ line[0] ][ int(line[1]) ] += 1
	total += 1

# Write data to file
write_to_file(stats)