import sys
import os

import gi
from gi.repository import Gtk
from gi.repository import Gdk
from gi.repository import GObject
from gi.repository import PanelApplet

import managers 

am = managers.AccountManager()
cm = managers.ConnectionManager()
config = managers.ConfigManager()
		
class GmailApplet:

	NEW_EMAIL_ICON_PATH 	= "/usr/share/pixmaps/gmail-applet/new-email.svg"
	NO_EMAIL_ICON_PATH 	= "/usr/share/pixmaps/gmail-applet/no-email.svg"
	NO_CONNECTION_ICON_PATH = "/usr/share/pixmaps/gmail-applet/no-connection.svg"

	HAVE_ICON = False

	can_connect = False
	connected   = False

	main_menu_xml = """<menuitem name='Accounts' action='Accounts'/>"""

	def __init__(self, applet):
		self.applet = applet
		
		is_registered, username = config.get_email()
		print(is_registered)
		if is_registered:
			self.connect_to_gmail(username)
		self.create_widgets()

	def create_widgets(self):
		print("About to create the widgets")
		self.box	= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.event_box	= Gtk.EventBox() 

		try:
			# Trying to put the icon in the applet
			self.icon = Gtk.Image()
			if self.connected:
				self.icon.set_from_file(self.NO_EMAIL_ICON_PATH)
			else:
				self.icon.set_from_file(self.NO_CONNECTION_ICON_PATH)
			
			self.event_box.add(self.icon)
			self.HAVE_ICON = True
		except:
			print("There's no icon :/")
		
		self.event_box.set_visible_window(False)
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

	def connect_to_gmail(self, username):
		self.can_connect = True 
		
		successful_connection = cm.connect(username, am.get_password_from_username( username ) )
		if successful_connection:
			self.connected = True
			GObject.timeout_add(config.get_ping(), self.check_for_new_mails ) 

	def check_for_new_mails(self):
		if self.connected:
			print("Idle check")
			return True
		return False
	
	def show_account_dialog(self):
		print("Opening the dialog")
		return True
		
		dialog = NewAccountDialog()
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			print ("The OK Button it's clicked")
			email 	 = dialog.email_entry.get_text()
			password = dialog.password_entry.get_text()
			
			am.register_new_email( email, password )
			config.set_email( dialog.email_entry.get_text() )

			self.can_connect = True
			
			password = None
		elif response == Gtk.ResponseType.CANCEL:
			pass
		dialog.destroy()

		return True
	
	def check_gmail_on_browser( self, widget, event ):
		print("Gona open firefox")
		return True

class NewAccountDialog(Gtk.Dialog):
	def __init__(self,parent=None):
		Gtk.Dialog.__init__(self,"New Account", parent, 0,
				(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
				 Gtk.STOCK_OK, Gtk.ResponseType.OK))

		self.set_default_size(200,150)
		
		self.email_label = Gtk.Label("Email:")
		self.email_entry = Gtk.Entry()

		self.password_label = Gtk.Label("Password:")
		self.password_entry = Gtk.Entry()
		self.password_entry.set_visibility(False)

		box = self.get_content_area()
		
		# Add everything to the dialog
		box.add(self.email_label)
		box.add(self.email_entry)
		box.add(self.password_label)
		box.add(self.password_entry)
		
		self.show_all()

''' Entry point '''
def applet_factory ( applet, iid, data = None):
	if iid != "gmail":
		return False
	
	GObject.threads_init()
	gmail = GmailApplet( applet )


	return True
