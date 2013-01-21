import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import PanelApplet

def applet_fill(applet):
	label = Gtk.Label("Hello World")
	applet.add(label)
	applet.show_all()

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		return False
	
	applet_fill(applet)

	return True
