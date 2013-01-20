#!/usr/bin/python

import sys
from gi.repository import Gtk
from gi.repository import PanelApplet
import gi

from gmailApplet import applet_factory

if __name__= '__main__': # Testing for execution
	print('starting factory')
	PanelApplet.Applet.factory_main("gmailFactory",
					PanelApplet.Applet.__gtype__,
					applet_factory,
					None)
