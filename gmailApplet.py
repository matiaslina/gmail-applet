import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import PanelApplet

class GmailApplet:

	HAVE_ICON = False
	
	def __init__(self, applet):
		self.applet = applet

		self.box	= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.event_box	= Gtk.EventBox() 
		#self.button = Gtk.Button()

	def fill(self):
		try:
			self.icon = Gtk.Image()
			self.icon.set_from_file("/usr/share/pixmaps/gmail-applet/new-email.svg")
			
			#self.button.set_property("image", self.icon)
			self.event_box.add(self.icon)
			self.HAVE_ICON = True
		except:
			self.button.set_label("Gmail")
		
		try:
			self.event_box.set_visible_window(False)
		except:
			print("unknow lala")
		self.event_box.connect("button_press_event", self.on_eb_press)
		self.box.pack_start(self.event_box, False, False, 15)

		self.applet.set_background_widget(self.box)
		self.applet.add(self.box)
		self.applet.show_all()
	
	def on_eb_press(self, widget, event):
		print("Event Box clicked")

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		return False
	
	gmail = GmailApplet( applet )
	gmail.fill()

	return True
