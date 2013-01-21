import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import PanelApplet

def applet_fill(applet):
	label = Gtk.Label("Hello World")
	print("label created")
	applet.add(label)
	print("label added")
	applet.show_all()
	print("applet showed")

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		print("iid = " + iid)
		print("FALSE")
		return False
	
	applet_fill(applet)
	print ("applet filled")
	
	print("Return true")
	return True
