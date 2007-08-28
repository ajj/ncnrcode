#!/usr/bin/python

import pygtk
pygtk.require('2.0')
import gtk, vte

window = gtk.Window()
window.resize(600,700)
window.show()

term  = vte.Terminal()
pid   = term.fork_command('icp')
term.set_emulation('xterm')
term.show()

window.add(term)
window.show_all()
window.connect("destroy", lambda w: gtk.main_quit())
gtk.main()


