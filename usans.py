#!/usr/bin/python

import os
import sys

def isBT5Data(fileName):

    inputfile = open(fileName, "r")
    inputdata = inputfile.readlines()
    
    if len(inputdata) < 2:
        inputfile.close()
        return 0
    elif inputdata[1].find('Filename') > 0:
        inputfile.close()
        return 1
    else:
        inputfile.close()
        return 0    
 
def numeric_compare(x, y):
    x = float(x)
    y = float(y)    

    if x < y:
        return - 1
    elif x == y:
        return 0
    else: # x>y
        return 1     

def GetBT5DirList():
    """Function to parse the directory listing of the current working directory
         and create a list of filenames that are BT5 data files"""
         
    dirlist = os.listdir(os.getcwd())
    
    bt5list = [ x for x in dirlist if (x.find('.bt5') > 0 and isBT5Data(x))]
    
    bt5list.sort(key=lambda s: os.path.getmtime(s))
    
    return bt5list

if __name__ == '__main__':
    import sys
    data,metadata = getBT5DataFromFile(sys.argv[1])
    printBT5DetData(data)

    maxinfo = maxDetCount(data, 2)
    print maxinfo
    avals = getAlignVals(data, maxinfo['Position'])
    print avals
