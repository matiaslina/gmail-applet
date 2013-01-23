import imaplib
import pynotify

import os
from os.path import expanduser, isdir, isfile

pynotify.init("Gmail-applet")

class ConnectionManager:

	def __init__(self):

		# Easy way to know if we're connected
		self.connected  = False

		# Last count of unread emails
		self.last_unread_emails = -1 

		self.needs_update = True

		self.inbox 	= None 
		print("Connection manager running")

	def connect(self, username, password ):
		try:
			self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
			self.imap_server.login(username, password)
		except:
			print("Unable to connect to gmail")
			self.connected = False
			return False

		self.connected = True
		return True

	def disconnect(self):
		if self.connected:
			self.imap_server.logout()

	def select_inbox(self, inbox=None):
		self.inbox = inbox
		self.imap_server.select( inbox )

	def check_unread_emails(self):
		status, response = self.imap_server.status(self.inbox, "(UNSEEN)")

		# Get the count of unread emails.
		unread_emails = int(response[0].split()[2].strip(').,]'))

		return unread_emails

	def have_new_emails(self):
		unread_emails = self.check_unread_emails()
		if unread_emails > self.last_unread_emails:
			notification = pynotify.Notification('Gmail',"You have " + unread_emails.__str__() + " new emails","/usr/share/pixmaps/gmail-applet/new-email.svg")
			notification.show()
			print("Asdjfasjdfoasjdf")
			self.last_unread_emails = unread_emails
			return (True, unread_emails)
		elif unread_emails < self.last_unread_emails:
			self.last_unread_emails = unread_emails
			return (False, unread_emails)
		else:
			return (False, self.last_unread_emails)
		

class AccountManager:
	
	KEYRING_ID 	= 'gmail_applet'
	CONFIG_FOLDER	= expanduser('~') + "/.gmail-applet"

	def __init__(self):
		print("Account manager running")
		if not isfile(self.CONFIG_FOLDER):
			os.mkdir(self.CONFIG_FOLDER)
	
	def is_user_registered(self):
		if isfile(self.CONFIG_FOLDER + "/accounts"):
			f = open( self.CONFIG_FOLDER + "/accounts", 'r')
			try:
				account = f.readline()
				return (True, account)
			finally:
				f.close()
		return (False,'')

	################ Keyring methods #######################
	def get_password_from_username(self, username):
		return keyring.get_password(self.KEYRING_ID, username)

	def save_password(self, username, password):
		keyring.set_password(self.KEYRING_ID, username, password)
	
	def delete_username(self, username):
		try:
			keyring.delete_password(self.KEYRING_ID, username)
		except:
			print("The username/password doesn't exist")
			return False

		return True

if __name__ == '__main__':
	pass
