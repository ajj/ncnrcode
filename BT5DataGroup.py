import usans
import math

class BT5DataGroup:
    '''Class containing a group of BT5 data sets to be treated as one data group'''
    def __init__(self, dataSetList=None):
        
        self.isPlotted = False
        self.groupName = None
        if dataSetList != None:
            self.groupName = dataSetList[0].fileName[0:5]    
                
    def addDataSet(self,addList):
        '''Add data sets to the group. Takes a list of data set objects'''
        for dataSet in addList:
            self.dataSetList.append(dataSet)
        
    def removeDataSet(self,dataSetName):
        '''Remove a data set from the group. Takes a data set name'''
        
    def plotDataGroup(self,axes,plottype=None,yerrorbars=True):
        '''Plot the data group. As with BT5DataSet takes matplotlib axes and some options
        
        Pass options to each data set.
        '''
    
    def unplotDataGroup(self):
        '''Remove the data group from the plot.
        
        Calls remove_plot from BT5DataSet
        '''
    
    def calcAlignVals(self,mv):
        '''Return the values we record in the logbook for a given motor position
        
        Determine which data set the motor val belongs to and call function from that class.
        
        '''