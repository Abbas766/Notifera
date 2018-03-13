print("Enter your Twilio Credentials:\n(These details will be stored in file credentials.txt)")

account_sid = input("Enter the Account SID : ")
auth_token = input("\nEnter Auth Token ID : ")
twilio_number = input("\nEnter the assigned Twilio Number : ")
user_number = input("\nEnter your registered (with Twilio) Phone Number : ")

with open("Credentials.txt",'w') as f:
	f.write(account_sid+"\n")
	f.write(auth_token+"\n")
	f.write(twilio_number+"\n")
	f.write(user_number+"\n")
	f.close()
	print("Your details were saved succesfully !!!")
