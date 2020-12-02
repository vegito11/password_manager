import datetime
from sync_encrypt import generate_password, get_encrypted_password
from sync_decrypt import get_decrypted_password
import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config/config.properties')
pass_filepath = parser['pass_para']['password_store']
sep = "; "

def fstore_encry_pass(user, website, username, password):
	''' Store Encrypted password and username in file '''
	
	with open(pass_filepath, "a", encoding='utf-8') as f:
		f.writelines(sep.join((user, website, username, str(datetime.date.today()), password)))
		f.write("\n")

def fget_encry_pass(user, website, username):
	''' Get Encrypted password from file '''
	
	# Get encrypted password
	with open(pass_filepath,"r", encoding='utf-8') as pass_file:
		for line in pass_file:
			if sep.join((user, website, username)) in line:
				return line.split(sep)[-1].strip()
				break
	return False

def fupdate_pass(user, website, username, new_pass):
	''' Update password for respective user	 '''
	
	# Get respective line
	with open(pass_filepath, "r", encoding='utf-8' ) as update_fd:
		for line in update_fd:
			if sep.join((user, website, username)) in line:
				break
		else:
			return False
		update_fd.seek(0)		
		new_data = update_fd.read().replace(line, 
					sep.join((user, website, username, str(datetime.date.today()), new_pass)) + "\n") 

	with open(pass_filepath, "w", encoding='utf-8' ) as update_fd:
		update_fd.write(new_data)

	return True	

def fdelete_pass(user, website, username):
	''' Delete Encrypted password and username from file '''
	
	with open(pass_filepath, "r", encoding='utf-8' ) as delete_fd:
		for line in delete_fd:
			if sep.join((user, website, username)) in line:
				break
		else:
			print(" No user with this credentials")		
			return
		delete_fd.seek(0)
		new_data = delete_fd.read().replace(line, "" )

	with open(pass_filepath, "w", encoding='utf-8' ) as delete_fd:
		delete_fd.write(new_data)

def get_user_data():
	'''' Get user, website and username from user using Prompt '''
	global user, website, username
	print("_"*31)
	user = input(" \t Enter the User : ")
	# user = "vegito1"

	website = input(" \t Enter the website name : ")	
	# website = "fb.com"

	username = input(" \t Enter the Username (email, uid) : ")
	# username = "qa@gmail.com"
	global pass_filepath
	user_pass_path = input("\n\t Where to store password [default=%s] : "%(pass_filepath))
	if len(user_pass_path) > 2:
		pass_filepath = user_pass_path
	print("_"*31)


def operations():

	print("\n ******* Menu ******* ")
	print("\n\t 1) Store Password \n\t 2) Get Password \n\t 3) Update Password \n\t 4) Delete Password \n\t 5) Exit",end="\t\t")
	choice = eval(input("Enter the Option : "))
	print("-=-"*29)
	

	# 1) Store Password in file
	if choice == 1:
		
		get_user_data()

		pass_choice = input(" \n\t Own Password or auto-generated [yes or any_char] : ")
		# pass_choice = "y"

		# Enter password from User
		if pass_choice.lower() in ["y", "yes"]:
			password = input("\n\t Enter Password: ")
			# password = "omkar12"

		# Generate Password
		else:
			password = generate_password()

		PIN = input(" \n\t Enter the 4 digit pin** : ")
		# PIN = 4432
		encrypted_password = get_encrypted_password(int(PIN), password)
		fstore_encry_pass(user, website, username, encrypted_password)
		# fstore_encry_pass(user, website, username, password)
		print(" \n\t This is your password : ", password)

	# 2) Get Decryped Password
	elif choice == 2:
		
		get_choice = input("\t Enter password to Decrypt ? or use in the file [yes or any_char] : ")
		# get_choice = "y"

		# Enter password from User
		if get_choice.lower() in ["y", "yes"]:
			encrypted_pass = input("\n\t Enter Encrypted Password:")
			# encrypted_pass = "čþĻĚĠĢĹģČĘķīČĪĭĬĪġľĒĒěýĠğ"

		# Generate Updated Password
		else:
			get_user_data()
			encrypted_pass = fget_encry_pass(user, website, username)
			
		PIN = input("\n\t Enter the 4 digit pin** : ")
		
		
		if encrypted_pass == False:
			print("\n\t !!! User with this credential does not exists !!!")
			return 
		
		decrypted_pass = get_decrypted_password(int(PIN), encrypted_pass)
		print("\n\t This is your decrypted password : ", decrypted_pass)

	# 3) Update Password in file
	elif choice == 3:

		get_user_data()
		pass_choice = input("\n\t Enter Updated password ? or auto-generated [yes or any_char] : ")

		# Enter password from User
		if pass_choice.lower() in ["y", "yes"]:
			updated_pass = input("\t Enter Updated Password: ")
			# updated_pass = "omkar20"

		# Generate Random - Updated Password 
		else:
			updated_pass = generate_password()

		PIN = input("\n\t Enter the 4 digit pin** : ")
		encrypted_password = get_encrypted_password(int(PIN), updated_pass)
		
		if fupdate_pass(user, website, username, encrypted_password) == False:
			print("\n\t !!! User with this credential does not exists !!!")
			return 
		
		# fstore_encry_pass(user, website, username, password)
		print("\n\t This is your new password : ", updated_pass)

	# 4) Delete Password from file
	elif choice == 4:
		get_user_data()
		fdelete_pass(user, website, username)

	else:
		print(" !!! Please Enter Valid Option !!!! ")
		
if __name__ == '__main__':
	
	# pass_filepath = "./encrypt_pass_store.txt"
	operations()
