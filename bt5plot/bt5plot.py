#!/usr/bin/env python 

import sys
import os
import re
import matplotlib
import numpy
matplotlib.use('GTK')

from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar

import usans
from BT5DataSet import BT5DataSet
from BT5DataGroup import BT5DataGroup

try:
    import pygtk
    pygtk.require("2.0")
    
except:
    pass

try:
    import gtk
    import gtk.glade
except:
    sys.exit(1)

class appGui:
    
    TARGETS = [('STRING', gtk.TARGET_SAME_APP, 0)]
    
    def __init__(self):

        runpath = os.path.dirname(os.path.realpath(__file__))
        
        gladefile = runpath+"/bt5plot.glade"
        self.windowname = "win_Main"
        self.wTree = gtk.glade.XML(gladefile, self.windowname)

        event_dic = {"on_win_Main_destroy" : gtk.main_quit,
                     "on_quit1_activate" : gtk.main_quit,
                     "on_set_data_dir1_activate" : self.setdatadir,
                     "on_xaxis_loglin_activate" : self.handle_xaxis_loglin,
                     "on_yaxis_loglin_activate" : self.handle_yaxis_loglin,
                     "on_yaxis_errorbars_activate" : self.handle_yaxis_errorbars,
                     "on_plot_type_activate" : self.handle_plot_type_change,
                     "on_btn_ClearPlot_clicked" : self.handle_clearplot,
                     "on_btn_Refresh_clicked" : self.handle_refreshlist,
                     "on_btn_Filter_clicked" : self.handle_filter}
    #                 "on_tv_plotlist_key_press_event" : self.handle_plotlist_keypress}

        #This is a bit clunky, but never mind.
        #Set default plottype to rate. Glade definition sets that as default active button in menu
        self.plottype = 'rate'
        self.yerrorbars = True
        
        self.wTree.signal_autoconnect(event_dic)

        # Set up file list
        self.filelistview = self.wTree.get_widget("tv_filelist")
        
        self.filelist = gtk.TreeStore(str, 'gboolean', object)
        self.filelist.set_sort_column_id(0, gtk.SORT_ASCENDING)

        # Set up filtering of file list
        self.filter_entry = self.wTree.get_widget("ent_filter")
        self.filter_string = []
        self.filter_string.append(self.filter_entry.get_text())
        self.filelistfilter = self.filelist.filter_new()
        self.filelistfilter.set_visible_func(self.filter_filelist, self.filter_string)

        self.filelistview.set_model(self.filelistfilter)

        self.cellrenderertoggle = gtk.CellRendererToggle()
        self.cellrenderertoggle.set_property('activatable', True)
        self.cellrenderertoggle.connect("toggled", self.handle_plot_toggle, self.filelistfilter)
    
        self.AddFileListColumns()

        #fill the file list
	if (len(sys.argv) > 1):
		os.chdir(sys.argv[1])
        self.FillFileList(usans.GetBT5DirList())

        # Set up graphing widget to display data
        self.figure = Figure(figsize=(4, 4), dpi=72)
        self.axis = self.figure.add_subplot(111)
        self.axis.set_yscale('log')
        self.axis.set_aspect('auto')
        self.axis.set_autoscale_on('True')
        self.axis.set_xlabel('Motor position')
        self.axis.set_ylabel('Counts')
        self.axis.grid(True)
        
        self.canvas = FigureCanvasGTK(self.figure)
        self.figure.canvas.mpl_connect('pick_event', self.handle_plot_click)
        self.canvas.show()
        
        self.plotView = self.wTree.get_widget("vbox4")
        self.plotView.pack_start(self.canvas, True, True)    
        
        self.metadataView = self.wTree.get_widget("tv_metadata")
        self.mdlist = gtk.ListStore(str, str)
        
        
    def AddFileListColumns(self):
        """This function adds a column to the list view.
        First it create the gtk.TreeViewColumn and then set
        some needed properties"""
                        
        column = gtk.TreeViewColumn('Filename', gtk.CellRendererText(), text=0)
        column.set_resizable(True)        
        column.set_sort_column_id(0)
        self.filelistview.append_column(column)

        column = gtk.TreeViewColumn('', self.cellrenderertoggle, active=1)
        self.filelistview.append_column(column)
        return
        
    
    def FillFileList(self, filenames):
        self.filelist.clear()
        
        groupList = self.generateDataGroups(filenames)
        
        for group in groupList:
                self.filelist.append(None, [group.groupName, 0, None])
                
        return
            
            
    def generateDataGroups(self,filenames):
        
        datasetList = []
        dataindexList = []
        datagroupList = []
        
        
        #assuming list hsa come in sorted by date...
        for filename in filenames:
            #generate list of BT5DataSet objects
            datasetList.append(BT5DataSet(filename))
        
        #print datasetList
        #build list of list indices where either scanned motor is A2 or scanned motor is not A2
        for dataset in datasetList:          
            if dataset.scanmot == 'A2':
                #check for 0
                if 0 in dataset.detdata.keys():
                    dataindexList.append(datasetList.index(dataset))
            else:
                dataindexList.append(datasetList.index(dataset))
        
        previndex = 0
        for dataindex in dataindexList:
            if dataindexList.index(dataindex) == len(dataindexList)-1:
                nextindex = len(datasetList)
            else:
                nextindex = dataindex
            datagroupList.append(BT5DataGroup(datasetList[previndex:nextindex]))
            previndex = dataindex
        
        print len(datagroupList)
        
        return datagroupList
    
    
    def RefreshFileList(self, filenames):        
        #print len(filenames)
        
        deletelist = []
        tempstr = self.filter_entry.get_text()
        del self.filter_string[:]
        self.filter_string.append("")
        self.filelistfilter.refilter()
        
        treestore = self.filelistview.get_model()
        treestore.foreach(self.filelist_match_filename, (filenames, deletelist))
          
        for filename in filenames:
            self.filelist.append([filename, 0, None])
        
        deletelist.reverse()
        for path in deletelist:
            treestore.remove(treestore.get_iter(path))

        del self.filter_string[:]
        self.filter_string.append(tempstr)
        self.filelistfilter.refilter()
        return

    def filelist_match_filename(self, model, path, iter, data):
        
        mval = model.get_value(iter, 0)
        
        if mval in data[0]:
            del data[0][data[0].index(mval)]
        else:
            data[1].append(path)
            
        return False
    
    def handle_refreshlist(self, widget):

        self.RefreshFileList(usans.GetBT5DirList())
        
        return

    def filter_filelist(self, model, iter, data):
        
        if model.get_value(iter, 0):        
            match = re.match(data[0], model.get_value(iter, 0))
        else:
            match = None
        
        if match is None:
            return False
        else:
            return True
        
    def handle_filter(self, widget):
        
        del self.filter_string[:]
        self.filter_string.append(self.filter_entry.get_text())
        #print self.filter_string[0]
        self.filelistfilter.refilter()
        
        return

    def setdatadir(self, widget):
        
        #Clear plot before selecting new folder
        #This is a bit clunky, but it avoids a lot of pain for the moment
        
        self.clearplot()
        
        chooser = gtk.FileChooserDialog(title="Select Data Directory", action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
                                  buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        chooser.set_default_response(gtk.RESPONSE_OK)
        chooser.set_current_folder(os.getcwd())
        response = chooser.run()
        if response == gtk.RESPONSE_OK:
            os.chdir(chooser.get_filename())
            self.FillFileList(usans.GetBT5DirList())
        chooser.destroy()

    def handle_plot_toggle(self, filter_cell, filter_path, filter_model):
        model = filter_model.get_model()
        path = filter_model.convert_path_to_child_path(filter_path)
        model[path][1] = not model[path][1]

        if model[path][1]:
            #load data
            model[path][2] = BT5DataSet(model[path][0])
            #add plot
            model[path][2].plot_dataset(self.axis, self.plottype, self.yerrorbars)
            self.rescale_and_redraw()
        else:
            #remove plot
            model[path][2].remove_plot()
            self.rescale_and_redraw()
        return

 
    def handle_xaxis_loglin(self, widget):


        if (self.axis.get_xscale() == "log"):
            self.axis.set_xscale('linear')
        else:
            self.axis.set_xscale('log')

        self.rescale_and_redraw()
        
        return    

    def handle_yaxis_loglin(self, widget):


        if (self.axis.get_yscale() == "log"):
            self.axis.set_yscale('linear')
        else:
            self.axis.set_yscale('log')

        self.rescale_and_redraw()
        return
 
    def handle_yaxis_errorbars(self, widget):
        
        if (self.yerrorbars == True):
            self.yerrorbars = False
        else:
            self.yerrorbars = True

        model = self.filelistview.get_model().get_model()
        iter = model.iter_children(None)
        while iter:
            path = model.get_path(iter)
            if model[path][1] != 0:
                model[path][2].remove_plot()
                model[path][2].plot_dataset(self.axis, self.plottype, self.yerrorbars)
            iter = model.iter_next(iter)

        self.rescale_and_redraw()
        return
       
    def handle_plot_type_change(self, widget):
    	    	
    	if widget.get_active():
    		self.plottype = widget.get_name().split('_')[1]

        model = self.filelistview.get_model().get_model()
        iter = model.iter_children(None)
        while iter:
            path = model.get_path(iter)
            if model[path][1] != 0:
                model[path][2].remove_plot()
                model[path][2].plot_dataset(self.axis, self.plottype, self.yerrorbars)
            iter = model.iter_next(iter)

        self.rescale_and_redraw()
    		
    	return
    	
    def handle_clearplot(self, widget):
        
        self.clearplot()
        
        return
        
    
    def clearplot(self):
        model = self.filelistview.get_model().get_model()
        iter = model.iter_children(None)
        while iter:
            path = model.get_path(iter)
            if model[path][1] != 0:
                model[path][2].remove_plot()
                model[path][1] = not model[path][1]
            iter = model.iter_next(iter)
        
        self.canvas.draw()
        return 
        
    def rescale_and_redraw(self):

        xdata = []
        ydata = []

        if len(self.axis.lines) > 0:

            for line in self.axis.lines:
            	if self.axis.get_xscale() == 'log':
            		xdata.extend([xval for xval in line.get_xdata() if xval > 0])
            	else:
            		xdata.extend(line.get_xdata())
            	if self.axis.get_yscale() == 'log':
            		ydata.extend([xval for xval in line.get_ydata() if xval > 0])
            	else:
            		ydata.extend(line.get_ydata())
          
            #set limits
            xmin = float(min(xdata))
            xmax = float(max(xdata))
            ymin = float(min(ydata))
            ymax = float(max(ydata))	
    
            #adjust for size of markers (sort of)
            xmin = xmin - 0.1 * abs(xmin)
            xmax = xmax + 0.1 * abs(xmax)
            ymin = ymin - 0.1 * abs(ymin)
            ymax = ymax + 0.1 * abs(ymax)
                    
            self.axis.set_xlim(xmin, xmax)
            self.axis.set_ylim(ymin, ymax)
        
        #self.axis.autoscale_view()
        self.canvas.draw()

        return

    def handle_plot_click(self, event):

        if event.mouseevent.button == 1:
            """ Report data about point """
            model = self.filelistview.get_model().get_model()
            iter = model.iter_children(None)
    
    
            if isinstance(event.artist, matplotlib.lines.Line2D):
                #print "Clicked..."
                pickedline = event.artist
                ind = event.ind
                xdata = pickedline.get_xdata()
    
                while iter:
                    path = model.get_path(iter)
                    if model[path][1] != 0:
                        for line in model[path][2].plot:
                            if line == pickedline:
                                model[path][2].calcAlignVals(xdata[ind])
                                label = self.wTree.get_widget("lbl_alignvals")
                                label.set_text(model[path][2].alignvalstring)
                                break
                    iter = model.iter_next(iter)
        elif event.mouseevent.button == 3:
            """ Do fit stuff """
            #print "Right button pressed"
            

app = appGui()
gtk.main()
