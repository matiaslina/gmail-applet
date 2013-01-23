import sys
import os

import gi
from gi.repository import Gtk, Gdk
from gi.repository import PanelApplet

class GmailApplet:

	HAVE_ICON = False

	main_menu_xml = """<menuitem name='Accounts' action='Accounts'/>"""

	def __init__(self, applet):
		self.applet = applet

		self.box	= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.event_box	= Gtk.EventBox() 

	def create_widgets(self):
		try:
			self.icon = Gtk.Image()
			self.icon.set_from_file("/usr/share/pixmaps/gmail-applet/new-email.svg")
			
			self.event_box.add(self.icon)
			self.HAVE_ICON = True
		except:
			self.button.set_label("Gmail")
		
		try:
			self.event_box.set_visible_window(False)
		except:
			print("unknow lala")
		self.event_box.connect("button_press_event", self.on_eb_press)
		self.box.pack_start(self.event_box, False, False, 0)

		# Setup the menu
		# Action group
		group = Gtk.ActionGroup("gmail_applet_actions")

		# Accounts item
		a_accounts = Gtk.Action("Accounts", None, "Open the account manager dialog", Gtk.STOCK_PREFERENCES)
		a_accounts.connect("activate", lambda x: self.show_account_dialog())

		group.add_action(a_accounts)

		# Create the menu
		self.applet.setup_menu(self.main_menu_xml, group)

		# Making the options menu ( i.e. open a browser, update manually, etc )

		self.menu = Gtk.Menu()

		self.about = Gtk.MenuItem()
		self.about.set_label("about")

		self.about.connect("activate", self.check_gmail_on_browser)

		self.menu.append(self.about)

		self.menu.show_all()

		self.applet.set_background_widget(self.box)
		self.applet.add(self.box)
		self.applet.show_all()
	
	def on_eb_press(self, widget, event):
		if event.type == Gdk.EventType.BUTTON_PRESS and event.button == 1:
			self.menu.popup(None,None,None,None,event.button, event.time)
			return True
		print("Event Box clicked")
		return False
	
	def show_account_dialog(self):
		print("There's no account dialog yet")
		return True
	
	def check_gmail_on_browser( self, widget, event ):
		print("Gona open firefox")
		return True

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		return False
	
	gmail = GmailApplet( applet )
	gmail.create_widgets()

	return True
