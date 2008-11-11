#!/usr/bin/python

#import Tkinter as Tk

def numeric_compare(x, y):
    x = float(x)
    y = float(y)    

    if x < y:
        return - 1
    elif x == y:
        return 0
    else: # x>y
        return 1 

def getBT5DataFromFile(fileName):
    '''
    Takes a filename and returns a dictionary of the detector values
    keyed by varying value (ususally A2 or A5)
    '''
    detdata = {}
    metadata = {}

    inputfile = open(fileName, "r")

    inputdata = inputfile.readlines()

    mdtmp = inputdata[0].split(' ')
    
    print mdtmp

    for index in range(13, len(inputdata), 2):
        detdata[inputdata[index].split()[0]] = inputdata[index + 1].split(',')    

    for key in detdata.keys():
        for val in range(0, len(detdata[key])):
            detdata[key][val] = int(detdata[key][val])

    inputfile.close()
    return detdata

def printBT5DetData(detdata):
    '''
    Print the contents of the file in a formatted fashion

    Takes a dictionary of data as provided by getBT5DataFromFile() and prints out the contents
    in a formatted fashion
    '''
    motorvals = detdata.keys()
    motorvals.sort(cmp=numeric_compare)

    for motorval in motorvals:
        str = motorval + ":"
        str += "\tMon: " + repr(detdata[motorval][0])
        str += "\tDet 1-5: " + repr(detdata[motorval][2])
        str += "\t" + repr(detdata[motorval][1])
        str += "\t" + repr(detdata[motorval][4])
        str += "\t" + repr(detdata[motorval][5])
        str += "\t" + repr(detdata[motorval][6])
        str += "\tTrans: " + repr(detdata[motorval][3])
        print str

    return 0

def getAlignVals(data, motorval):
    '''
    Return the values we record in the logbook for a given motor position

    Takes a dictionary as provided by getBT5DataFromFile and returns a dictionary with 
    keys Central, Trans and Sum
    '''
    alignvals = {}

    alignvals['Central'] = data[motorval][1]
    alignvals['Trans'] = data[motorval][3]
    alignvals['Sum'] = data[motorval][1] + data[motorval][2] + data[motorval][4] + data[motorval][5] + data[motorval][6]     
    return alignvals

def maxDetCount(data, detector):
    '''
    Return the maximum value and corresponding motor position for a given detector
    
    Takes a dictionary as provided by getBT5DataFromFile() and returns a dictionary with
    keys Position and Value
    '''    
    maxpos = ''
    maxval = 0
    result = {}

    mvals = data.keys()
    det = {'1':2, '2':1, '3':4, '4':5, '5':6}[repr(detector)]

    for mval in mvals:
        if data[mval][det] > maxval:
            maxval = data[mval][det]        
            maxpos = mval
    
    result['Position'] = maxpos
    result['Value'] = maxval

    return result    

    
    

if __name__ == '__main__':
    import sys
    data = getBT5DataFromFile(sys.argv[1])
    printBT5DetData(data)

    maxinfo = maxDetCount(data, 2)
    print maxinfo
    avals = getAlignVals(data, maxinfo['Position'])
    print avals
