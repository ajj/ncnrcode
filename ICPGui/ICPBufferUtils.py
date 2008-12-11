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
	bufs = {}
	
	for i in range(30):
		bufs[i] = struct.unpack(formatstr,data[i*320:(i+1)*320])

		#print line
		
	return bufs


def writeIBufferFile(bufs,outputfile):

	data = "" 

	for line in bufs:
		data = data+struct.pack(formatstr,bufs[line][0],
					          bufs[line][1],	
					          bufs[line][2],	
					          bufs[line][3],	
					          bufs[line][4],	
					          bufs[line][5],	
					          bufs[line][6],	
					          bufs[line][7],	
					          bufs[line][8],	
					          bufs[line][9],	
					          bufs[line][10],	
					          bufs[line][11],	
					          bufs[line][12],	
					          bufs[line][13],	
					          bufs[line][14],	
					          bufs[line][15],	
					          bufs[line][16],	
					          bufs[line][17],	
					          bufs[line][18],	
					          bufs[line][19],	
					          bufs[line][20],	
					          bufs[line][21],	
					          bufs[line][22],	
					          bufs[line][23],	
					          bufs[line][24],	
					          bufs[line][25],	
					          bufs[line][26],	
					          bufs[line][27],	
					          bufs[line][28],	
					          bufs[line][29],	
					          bufs[line][30],	
					          bufs[line][31])	

	f = open(outputfile, 'wb')
	f.write(data)
	f.close()	


if __name__ == "__main__":
	if len(sys.argv) > 1:
		data = readIBufferFile(sys.argv[1])
	else:
		data = readIBufferFile("IBUFFER.BUF")

	#for line in data:
	#	print data[line]

	writeIBufferFile(data,"TEST.BUF")
