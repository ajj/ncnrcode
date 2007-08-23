#!/usr/bin/env python

import sys
import vte
import matplotlib
matplotlib.use('GTK')

from matplotlib.figure import Figure
from matplotlib.axes import Subplot
from matplotlib.backends.backend_gtk import FigureCanvasGTK, NavigationToolbar


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
	def __init__(self):
		gladefile = "icpgui.glade"
		self.windowname = "winMain"
		self.wTree = gtk.glade.XML(gladefile, self.windowname)

		event_dic = {"on_winMain_destroy" : gtk.main_quit,
					 "on_quit1_activate" : gtk.main_quit,
					 "on_but_ls_clicked" : self.termsendlscmd,
 					 "on_but_clear_clicked" : self.termsendclearcmd}

		
		self.wTree.signal_autoconnect(event_dic)


		# Set up terminal widget to run icp
		self.term  = vte.Terminal()
		self.term.set_size(80,15)
		self.termpid  = self.term.fork_command('bash')
		self.term.set_emulation('xterm')
		self.term.show()


		self.termView = self.wTree.get_widget("hbox1")
		self.termView.pack_start(self.term, False, False)

		# Set up graphing widget to display xpeek data
		self.figure = Figure(figsize=(4,4), dpi=72)
		self.axis = self.figure.add_subplot(111)
		self.axis.set_xlabel('Motor position')
		self.axis.set_ylabel('Counts')
		self.axis.set_title('XPeek')
		self.axis.grid(True)
		
		self.canvas = FigureCanvasGTK(self.figure)
		self.canvas.show()
		
		self.xpeekView = self.wTree.get_widget("hbox1")
		self.xpeekView.pack_start(self.canvas, True, True)	

	def termsendlscmd(self, widget):
		self.term.feed_child("ls\n")
		
	def termsendclearcmd(self, widget):
		self.term.feed_child("clear\n")
		
		

app = appGui()
gtk.main()
