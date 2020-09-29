#!/usr/bin/env python3

import sys
import getopt
import os

import re

import hashlib

def get_command_outputs(cmd):
	proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	while True:
		line = proc.stdout.readline()
		if line:
			yield line

		if not line and proc.poll() is not None:
			break

def get_digest(algo, filepath) :
	
	h = hashlib.new(algo)
	
	length = hashlib.new(algo).block_size * 0x800
	
	with open(filepath, 'rb') as fp :
		while 1 :
			data = fp.read(length)
			if not data :
				break
			h.update(data)
	
	return h.hexdigest()
	
def main():
	ret = 0
	
	try:
		opts, args = getopt.getopt(
			sys.argv[1:],
			"hvo:",
			[
				"help",
				"version",
				"output="
			]
		)
	except getopt.GetoptError as err:
		print(str(err))
		sys.exit(2)
	
	output = ''
	
	for o, a in opts:
		if o == "-v":
			usage()
			sys.exit(0)
		elif o in ("-h", "--help"):
			usage()
			sys.exit(0)
		elif o in ("-o", "--output"):
			output = a
	
#	if output == '' :
#		print("no output option")
#		ret += 1
	
	algo = 'md5'
	
	if ret != 0:
		sys.exit(1)
	
	files = []
	
	while 1:
		line = sys.stdin.readline()
		if not line :
			break
		
		line = re.sub(r'\r?\n?$', '', line)
		
		if os.path.isfile(line) :
			files.append(line)

	for filepath in sorted(files) :
		digest = get_digest(algo, filepath)
		print('{0} {1}'.format(digest, filepath))

if __name__ == "__main__":
	main()

