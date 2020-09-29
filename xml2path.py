#!/usr/bin/env python3

import sys
import getopt
import os

import re

import hashlib

import xml.etree.ElementTree as et

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
	
	if ret != 0:
		sys.exit(1)
	
	parser = et.XMLPullParser()
	
	files = []
	
	while 1:
		line = sys.stdin.readline()
		if not line :
			break
		
		parser.feed(line)
		for event, elem in parser.read_events() :
			if elem.tag == 'path' :
				files.append(elem.text)
		
	for filepath in sorted(files) :
		print(filepath)

if __name__ == "__main__":
	main()

