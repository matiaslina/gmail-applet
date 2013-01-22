import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import PanelApplet

class GmailApplet:

	HAVE_ICON = False
	
	def __init__(self, applet):
		self.applet = applet
		self.button = Gtk.Button()

	def fill(self):
		try:
			self.icon = Gtk.Image()
			self.icon.set_from_file("/usr/share/pixmaps/gmail-applet/update-mail.png")
			self.button.set_property("image", self.icon)
			self.HAVE_ICON = True
		except:
			self.button.set_label("Gmail")
		
		self.applet.set_background_widget(self.button)
		self.applet.add(self.button)
		self.applet.show_all()

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		return False
	
	gmail = GmailApplet( applet )
	gmail.fill()

	return True
