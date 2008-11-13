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
    motlist = []

    print "File: ",fileName    
    inputfile = open(fileName, "r")

    inputdata = inputfile.readlines()

    if len(inputdata) < 2:
        inputfile.close()
        return 0,0

    if inputdata[1].find('Filename') > 0:

        mdtmp = inputdata[0].replace("'","")
        mdtmp = mdtmp.split()
    
        #Sundry metadata about run settings
        (metadata['filename'], metadata['datetime'],
        metadata['mon'],metadata['prefactor'],
        metadata['base'],metadata['numpnts'],
        metadata['type']) = (mdtmp[0],' '.join(mdtmp[1:5]),float(mdtmp[6]),int(mdtmp[7]),mdtmp[8],int(mdtmp[9]),mdtmp[10])
    
        #Comment string
        metadata['title'] = inputdata[2].strip()
    
        #Start, step and end values for motors 1-6
        motlist.append(inputdata[5].split()[1:])
        motlist.append(inputdata[6].split()[1:])
        motlist.append(inputdata[7].split()[1:])
        motlist.append(inputdata[8].split()[1:])
        motlist.append(inputdata[9].split()[1:])
        motlist.append(inputdata[10].split()[1:]) 
        metadata['motorvals'] = motlist
    
        for index in range(13, len(inputdata), 2):
            detdata[float(inputdata[index].split()[0])] = inputdata[index + 1].split(',')    

        for key in detdata.keys():
            for val in range(0, len(detdata[key])):
                detdata[key][val] = int(detdata[key][val])

        inputfile.close()
        return detdata,metadata

    else:
        inputfile.close()
        return 0,0

def printBT5DetData(detdata):
    '''
    Print the contents of the file in a formatted fashion

    Takes a dictionary of data as provided by getBT5DataFromFile() and prints out the contents
    in a formatted fashion
    '''
    motorvals = detdata.keys()
    motorvals.sort(cmp=numeric_compare)

    for motorval in motorvals:
        str = repr(motorval) + ":"
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
    data,metadata = getBT5DataFromFile(sys.argv[1])
    printBT5DetData(data)

    maxinfo = maxDetCount(data, 2)
    print maxinfo
    avals = getAlignVals(data, maxinfo['Position'])
    print avals
