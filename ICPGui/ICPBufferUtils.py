#!/usr/bin/env python

#Read and write ICP Buffer files

import sys
import struct

formatstr = '<50sh21f4s4i4f148x'


def readIBufferFile(inputfile):
	
	f = open(inputfile, 'rb')
	data = f.read()
	f.close()
	
	#print struct.calcsize(formatstr)
	lines = {}
	
	for i in range(30):
		lines[i] = struct.unpack(formatstr,data[i*320:(i+1)*320])

		#print line
		
	return lines

if __name__ == "__main__":
	if len(sys.argv) > 1:
		readIBufferFile(sys.argv[1])
	else:
		readIBufferFile("IBUFFER.BUF")
