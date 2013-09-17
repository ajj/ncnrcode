import usans
import math


class BT5DataSet:
    
    def __init__(self, fn=None):

        self.fileName = fn
        self.plot = None
        self.detdata = {}
        self.metadata = {}
        self.alignvals = {}
        self.alignvalstring = ''
        self.scanmot = ''

        if (self.fileName != None):
            self.getBT5DataFromFile(self.fileName)
        
        
    def getBT5DataFromFile(self,fileName):
        '''
        Takes a filename and returns a dictionary of the detector values
        keyed by varying value (usually A2 or A5)
        '''
    
        if usans.isBT5Data(fileName) == 1:
    
            motlist = []
    
            #print "File: ",fileName    
            inputfile = open(fileName, "r")
    
            inputdata = inputfile.readlines()
    
            mdtmp = inputdata[0].replace("'", "")
            mdtmp = mdtmp.split()
        
            #Sundry metadata about run settings
            (self.metadata['filename'], self.metadata['datetime'],
             self.metadata['mon'], self.metadata['prefactor'],
             self.metadata['base'], self.metadata['numpnts'],
             self.metadata['type']) = (mdtmp[0], ' '.join(mdtmp[1:5]), float(mdtmp[6]), int(mdtmp[7]), mdtmp[8], int(mdtmp[9]), mdtmp[10])
        
            #Comment string
            self.metadata['title'] = inputdata[2].strip()
        
            #Start, step and end values for motors 1-6
            motlist.append(inputdata[5].split()[1:])
            motlist.append(inputdata[6].split()[1:])
            motlist.append(inputdata[7].split()[1:])
            motlist.append(inputdata[8].split()[1:])
            motlist.append(inputdata[9].split()[1:])
            motlist.append(inputdata[10].split()[1:]) 
            self.metadata['motorvals'] = motlist
        
            self.scanmot = inputdata[12].split()[0]
        
            for index in range(13, len(inputdata), 2):
                self.detdata[float(inputdata[index].split()[0])] = inputdata[index + 1].split(',')    
    
            for key in self.detdata.keys():
                for val in range(0, len(self.detdata[key])):
                    self.detdata[key][val] = int(self.detdata[key][val])
    
            inputfile.close()
                    
    
    
    def printDetectorData(self):
        '''
        Print the contents of the file in a formatted fashion
    
        Takes a dictionary of data as provided by getBT5DataFromFile() and prints out the contents
        in a formatted fashion
        '''
        motorvals = self.detdata.keys()
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
    
    def calcAlignVals(self,mv):
        '''
        Return the values we record in the logbook for a given motor position
    
        Takes a dictionary as provided by getBT5DataFromFile and returns a dictionary with 
        keys Central, Trans and Sum
        '''
        motorval = float(mv)
        
        self.alignvals['Central'] = self.detdata[motorval][1]
        self.alignvals['Trans'] = self.detdata[motorval][3]
        self.alignvals['Sum'] = self.detdata[motorval][1] + self.detdata[motorval][2] + self.detdata[motorval][4] + self.detdata[motorval][5] + self.detdata[motorval][6]     
        self.alignvals['Monitor'] = self.detdata[motorval][0]
        self.alignvals['Sum/Monitor'] = float(self.alignvals['Sum'])/float(self.alignvals['Monitor'])
        
        self.alignvalstring = self.scanmot+": %5.2f" % motorval  
        self.alignvalstring += "   #4: "+repr(self.alignvals['Central'])
        self.alignvalstring += "   Trans: "+repr(self.alignvals['Trans'])
        self.alignvalstring += "\nSum: "+repr(self.alignvals['Sum'])
        self.alignvalstring += "   MCR: "+repr(self.alignvals['Monitor'])
        self.alignvalstring += "   Sum/MCR: %5.3f" % self.alignvals['Sum/Monitor']
    
    def maxDetCount(self, detector):
        '''
        Return the maximum value and corresponding motor position for a given detector
        
        Takes a dictionary as provided by getBT5DataFromFile() and returns a dictionary with
        keys Position and Value
        '''    
        maxpos = ''
        maxval = 0
        result = {}
    
        mvals = self.detdata.keys()
        det = {'1':2, '2':1, '3':4, '4':5, '5':6}[repr(detector)]
    
        for mval in mvals:
            if self.detdata[mval][det] > maxval:
                maxval = data[mval][det]        
                maxpos = mval
        
        result['Position'] = maxpos
        result['Value'] = maxval
    
        return result 
    
    def plot_dataset(self,axes,plottype=None,yerrorbars=True):
        '''
        Takes a matplotlib axes object and plots bt5 dataset on it.
        '''
        data = self.detdata
        metadata = self.metadata

        if type is None:
            plottype = 'rate'
                                       
        if plottype == 'total':
            #generate totals
            xdata = []
            ydata = [] 
            yerror = []    
             
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
                ydata.append(data[mval][1] + data[mval][2] + data[mval][4] + data[mval][5] + data[mval][6])
		if (ydata[len(ydata)-1] == 0):
		    yerror.append(0)
                else:
                    yerror.append(math.sqrt(ydata[len(ydata)-1]))
            
            axes.set_ylabel("Counts")
            if yerrorbars == True:
                self.plot = axes.errorbar(xdata,ydata,yerror,None,'bo', picker=5)
            else:
                self.plot = axes.errorbar(xdata,ydata,None,None,'bo', picker=5)
                
        elif plottype == 'rate':
            # generate countrate
            xdata = []
            ydata = []
            yerror = []
            
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
             
            if metadata['base'] == 'TIME':
                #Counting in TIME base, so normalize by seconds
                cnttime = metadata['mon']
                for mval in mvals:
                    ydata.append((data[mval][1] + data[mval][2] + data[mval][4] + data[mval][5] + data[mval][6]) / cnttime)
                    if (ydata[len(ydata)-1] == 0):
                        yerror.append(0)
                    else:
                        yerror.append(math.sqrt(ydata[len(ydata)-1])/math.sqrt(cnttime))
                    axes.set_ylabel("Counts/second")
            else:
                #Must be counting in monitor base so normalize by monitor
                moncts = metadata['mon']
                for mval in mvals:
                    ydata.append((data[mval][1] + data[mval][2] + data[mval][4] + data[mval][5] + data[mval][6]) / cnttime)
                    if (ydata[len(ydata)-1] == 0):
                        yerror.append(0)
                    else:
                        yerror.append(math.sqrt(ydata[len(ydata)-1])/math.sqrt(cnttime))
                    axes.set_ylabel("Counts/Monitor Count")
            
            if yerrorbars == True:
                self.plot = axes.errorbar(xdata,ydata,yerror,None,'bo', picker=5)
            else:
                self.plot = axes.errorbar(xdata,ydata,None,None,'bo', picker=5)

                
        elif plottype == 'trans':
            xdata = []
            ydata = []
            yerror = []
             
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
                ydata.append(data[mval][3])
                if (ydata[len(ydata)-1] == 0):
                    yerror.append(0)
                else:
                    yerror.append(math.sqrt(ydata[len(ydata)-1]))

            axes.set_ylabel("Transmission Detector Counts")
            if yerrorbars == True:
                self.plot = axes.errorbar(xdata,ydata,yerror,None,'bo', picker=5)
            else:
                self.plot = axes.errorbar(xdata,ydata,None,None,'bo', picker=5)
            
         
        elif plottype == 'mon':
            xdata = []
            ydata = []
            yerror = []
            
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
                ydata.append(data[mval][0])
                yerror.append(math.sqrt(ydata[len(ydata)-1]))
                
            axes.set_ylabel("Monitor Counts")
            if yerrorbars == True:
                self.plot = axes.errorbar(xdata,ydata,yerror,None,'bo', picker=5)
            else:
                self.plot = axes.errorbar(xdata,ydata,None,None,'bo', picker=5)
             
        elif plottype == 'split':
            xdata = []
            ydata1 = []
            ydata2 = []
            ydata3 = []
            ydata4 = []
            ydata5 = []
            yerror1 = []
            yerror2 = []
            yerror3 = []
            yerror4 = []
            yerror5 = []
             
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
                ydata1.append(data[mval][1])   
                yerror1.append(math.sqrt(ydata1[len(ydata1)-1]))
                ydata2.append(data[mval][2])   
                yerror2.append(math.sqrt(ydata2[len(ydata2)-1]))
                ydata3.append(data[mval][4])
                yerror3.append(math.sqrt(ydata3[len(ydata3)-1]))
                ydata4.append(data[mval][5])  
                yerror4.append(math.sqrt(ydata4[len(ydata4)-1]))
                ydata5.append(data[mval][6])  
                yerror5.append(math.sqrt(ydata5[len(ydata5)-1]))
            
            axes.set_ylabel("Counts")    
            if yerrorbars == True:
                self.plot = (axes.errorbar(xdata,ydata1,yerror1,None, 'o', label='2', c='b'),
                             axes.errorbar(xdata,ydata2,yerror2,None, '<', label='1', c='r'),
                             axes.errorbar(xdata,ydata3,yerror3,None, '>', label='3', c='g'),
                             axes.errorbar(xdata,ydata4,yerror4,None, '^', label='4', c='c'),
                             axes.errorbar(xdata,ydata5,yerror5,None, 'v', label='5', c='m'))            
            else:
                self.plot = (axes.errorbar(xdata,ydata1,None,None, 'o', label='2', c='b'),
                             axes.errorbar(xdata,ydata2,None,None, '<', label='1', c='r'),
                             axes.errorbar(xdata,ydata3,None,None, '>', label='3', c='g'),
                             axes.errorbar(xdata,ydata4,None,None, '^', label='4', c='c'),
                             axes.errorbar(xdata,ydata5,None,None, 'v', label='5', c='m'))
            
        elif plottype == 'nrate':
            # generate countrate
			# produce monitor normalized  plot
            xdata = []
            ydata = []
            yerror = []
            
            mvals = data.keys()
            mvals.sort(usans.numeric_compare)
            for mval in mvals:
                xdata.append(mval)
             
            #Always normalize by appropriate monitor counts
            for mval in mvals:
                 ydata.append((data[mval][1] + data[mval][2] + data[mval][4] + data[mval][5] + data[mval][6]) / (data[mval][0]/1e6))
                 if (ydata[len(ydata)-1] == 0):
                     yerror.append(0)
                 else:
                     yerror.append(math.sqrt(ydata[len(ydata)-1])/math.sqrt(data[mval][0]/1e6))

            axes.set_ylabel("Counts / (10^6 Monitor Counts)")
            if yerrorbars == True:
                self.plot = axes.errorbar(xdata,ydata,yerror,None,'bo', picker=5)
            else:
                self.plot = axes.errorbar(xdata,ydata,None,None,'bo', picker=5)
 
 

            
    def remove_plot(self):

	#Is it a plot with errorbars?
        if type(self.plot[0]) is tuple:
            #split plot
            for splot in self.plot:
                splot[0].remove()
                for linec in splot[1]:
                    linec.remove()
                for linec in splot[2]:
                    linec.remove()
	else:
            #normal plot
            for line in self.plot[0:1]:
                axes = line.get_axes()
                axes.lines.remove(line)
            for linec in self.plot[1]:
                linec.remove()
            for linec in self.plot[2]:
                linec.remove()
