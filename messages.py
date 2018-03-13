from twilio.rest import Client
import os
import sys

class Message:
	def __init__(self):
		self.body =None	
		# Checking if the credentials file exists
		# Getting the project directory and adding file name to it.
		file_path = str(os.getcwd())+"/Credentials.txt"
		# Checking for file path
		if os.path.isfile(file_path):
			with open("Credentials.txt",'r') as f:
				lines = [i.strip() for i in f.readlines()]
				self.account_sid,self.auth_token,self.twilio_number,self.user_number = lines
				f.close()
		else:
			print("You need to set the Twilio credentials before using this application.\
			    	\nPlease run credentials.py from the module directory !")
			sys.exit(0)
	
	def sendmessage(self,body):
		self.body = body
		
		# making Twilio client object
		client = Client(self.account_sid, self.auth_token)
		try:
			message = client.messages.create( to = self.user_number, from_= self.twilio_number, body = self.body)
			if message.sid:
				print("Notification Message Sent.")
		except Exception as e:
			print("Error occured while sending message.\nCheck your credentials for their validity and errors.")
		


