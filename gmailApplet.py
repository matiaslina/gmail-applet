import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import PanelApplet

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop

class GmailApplet:

	popupmenu_xml = """<menuitem name='Account' action='Account'/>
			   <menuitem name='Update' action='update />"""

	def __init__(self,applet):
		self.applet = applet
		self.label = Gtk.Label("Hola")

		self.applet.add(self.label)

		# Setup the menu
		group = Gtk.ActionGroup("gmail_actions")

		# account settings item
		a_account = Gtk.Action("Account", None, "Open gmail account settings", Gtk.STOCK_PREFERENCES)
		a_account.connect("activate", lambda x: print("Account activated" ) )
		a_update = Gtk.Action("Update", None,"Manual update", Gtk.STOCK_PREFERENCES)
		a_update.connect("activate", lambda x: print("Manual update activated") )
		group.add_action( a_account )
		group.add_action( a_update )

		self.applet.setup_menu( self.popupmenu_xml, group )

		self.applet.show_all()
		self.applet.connect("destroy", self.shutdown )

	def shutdown( self, wid, data=None):
		Gtk.main_quit()


''' Entry point '''
def applet_factory ( applet, iid, data = None):
	DBusGMainLoop( set_as_default=True )
	the_applet = GmailApplet(applet)
	return True
