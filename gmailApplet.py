import sys
import os
import appletmanagers 

from gi.repository import Gtk, Gdk
from gi.repository import PanelApplet
#cm = ConnectionManager()
#am = AccountManager()


class GmailApplet:

	NEW_EMAIL_ICON_PATH 	= "/usr/share/pixmaps/gmail-applet/new-email.svg"
	NO_EMAIL_ICON_PATH 	= "/usr/share/pixmaps/gmail-applet/no-email.svg"
	NO_CONNECTION_ICON_PATH = "/usr/share/pixmaps/gmail-applet/no-connection.svg"

	HAVE_ICON = False

	can_connect = False

	main_menu_xml = """<menuitem name='Accounts' action='Accounts'/>"""

	def __init__(self, applet):
		self.applet = applet
		
		is_registered, username = am.is_user_registered()
		if is_registered:
			self.can_connect = True 
			
			connected = cm.connect(username, am.get_password_from_username( username ) )
			if connected:
				self.connected = True

		self.create_widgets()

	def create_widgets(self):

		self.box	= Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.event_box	= Gtk.EventBox() 

		try:
			self.icon = Gtk.Image()
			if self.connected:
				self.icon.set_from_file(self.NO_EMAIL_ICON_PATH)
			else:
				self.icon.set_from_file(self.NO_CONNECTION_ICON_PATH)
			
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
		print("Opening the dialog")
		
		dialog = NewAccountDialog()
		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			print ("The OK Button it's clicked")
		elif response == Gtk.ResponseType.CANCEL:
			print ("The Cancel button it's clicked")

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
	
	gmail = GmailApplet( applet )
	gmail.create_widgets()

	return True
