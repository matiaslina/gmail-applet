import imaplib

class ConnectionManager:

	def __init__(self):

		# Easy way to know if we're connected
		self.connected  = False
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
			imap.logout()

	def select_inbox(self, inbox=None):
		self.inbox = inbox
		self.imap_server.select( inbox )

	def check_unread_emails(self):
		status, response = self.imap_server.status(self.inbox, "(UNSEEN)")

		# Get the count of unread emails.
		unread_emails = int(response[0].split()[2].strip(').,]'))

		return unread_emails

class AccountManager:
	
	self.KEYRING_ID = 'gmail_applet'

	def __init__(self):
		print("Account manager running")

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
