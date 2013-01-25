
import imaplib
import notify2 as pynotify
import keyring
import ConfigParser

import os
from os.path import expanduser, isdir, isfile

pynotify.init("Gmail-applet")

CONFIG_FOLDER	= expanduser('~') + "/.gmail-applet"

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
		except:
			print("Unable to connect to gmail")
			self.connected = False
			return False

		self.imap_server.login(username, password)
		self.connected = True
		return True

	def disconnect(self):
		if self.connected:
			self.imap_server.logout()

	def check_unread_emails(self):
		status, response = self.imap_server.status('INBOX', "(UNSEEN)")

		# Get the count of unread emails.
		unread_emails = int(response[0].split()[2].strip(').,]'))

		return unread_emails

	def have_new_emails(self):
		unread_emails = self.check_unread_emails()
		if unread_emails == 0:
			return 1
		if unread_emails > self.last_unread_emails:

			# Notifications
			notification = pynotify.Notification('Gmail',"You have " + unread_emails.__str__() + " new emails","/usr/share/pixmaps/gmail-applet/new-email.svg")
			notification.show()
			self.last_unread_emails = unread_emails
			return 0 
		else:
			return 0

class AccountManager:
	
	KEYRING_ID 	= 'gmail_applet'

	def __init__(self):
		print("Account manager running")
		if not isdir(CONFIG_FOLDER):
			os.mkdir(CONFIG_FOLDER)
	
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

class ConfigManager:

	config_file = CONFIG_FOLDER + "/config.cfg"

	def __init__(self):
		# A Config Parser
		self.config = ConfigParser.RawConfigParser()

		if not isdir (CONFIG_FOLDER):
			os.mkdir(CONFIG_FOLDER)
			self.config.add_section('app')
			self.config.set('app','ping',1000*60*30)
			self.config.add_section('users','email','')
			with open( self.config_file,'wb') as f:
				self.config.write(f)

		else:
			self.config.read( self.config_file )

	def get_ping(self):
		return self.config.getint('app','ping')
	
	def get_email(self):
		email = self.config.get('users','email')
		is_registered = (email != '')

		return (is_registered,email)

	def set_ping(self, ping):
		self.config.set('app','ping',ping)

		with open( self.config_file, 'wb') as f:
			self.config.write(f)

	def set_email(self, email):
		self.config.set('users','email',email)

		with open( self.config_file,'wb') as f:
			self.config.write(f)
