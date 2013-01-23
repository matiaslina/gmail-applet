import imaplib

class ConnectionManager:

	def __init__(self):

		# Easy way to know if we're connected
		self.connected  = False
		self.inbox 	= None 
		print("Connection manager running")

	def connect_to_server(self, username, password ):
		try:
			self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com",993)
			self.imap_server.login(username, password)
		except:
			print("Unable to connect to gmail")
			self.connected = False
			return False

		self.connected = True
		return True

	def select_inbox(self, inbox=None):
		self.inbox = inbox
		self.imap_server.select( inbox )

	def check_unread_emails(self):
		status, response = self.imap_server.status(self.inbox, "(UNSEEN)")

		# Get the count of unread emails.
		unread_emails = int(response[0].split()[2].strip(').,]'))

		return unread_emails

if __name__ == '__main__':
	pass
