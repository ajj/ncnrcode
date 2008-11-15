#!/usr/bin/python

from bt5reader import *




if __name__ == '__main__':
	import sys
	numfiles = len(sys.argv)
	if (numfiles > 3):
		#print "Input files:"
		#for filename in sys.argv[1:numfiles-1]:
		#	print filename
		#print "Output file:"
		#print sys.argv[numfiles]
		addBT5Data(sys.argv[1:numfiles-1])
	elif (numfiles > 2):
		#print "Input files:"
		#for filename in sys.argv[1:numfiles]:
		#	print filename	
		#print "Output to stdout"
		(outh,outs,outdet) = addBT5Data(sys.argv[1:numfiles])
		printBT5FormatData(outh,outs,outdet)
	else:
		print "You must specify more than 1 filename"
