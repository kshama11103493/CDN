# Module to read & partially parse the config file 'proxy.conf'

import os, stat, string, sys


timestamp = 0
config = {}

def reload():
    global timestamp, config
    newstamp = os.stat('proxy.conf')[stat.ST_MTIME]
    if newstamp != timestamp:
	timestamp = newstamp
	section = 'global'
	config = {}
	config[section] = []
	for line in map(string.strip, open('proxy.conf').readlines()):
	    if line[:1] == '[' and line[-1:] == ']':
		# New section
		section = line[1:-1]
		if section not in config.keys(): config[section] = []
	    elif line[:1] == '#':
		# Comment
		pass
	    elif line:
		# Information for this section
		config[section].append(line)

def get(name):
    # Get the options for this section, or empty list if there are none
    return config.get(name, [])

# Load the initial config file, then load the required modules
reload()
_module_names = config.get('modules', [])

