import os
import signal
import time
import datetime
import sys
import ast
import json
from database import Database, User, ACCESS_ID

from pirc522 import RFID

received = False
loop = True
rdr = RFID()
util = rdr.util()
util.debug = True

db = Database()

def read():
	
	#mostly copied from example Read.py
	#wait for rfid tag and returns uid in array

	print("--------------------")
	print("Read UID: Start")
	
	run = True
	while run:
		rdr.wait_for_tag()
		(error, data) = rdr.request()
		(error, uid) = rdr.anticoll()
		
		if not error:
			print("Tag detected")
			tag_id = str(uid[0]) + "," + str(uid[1]) + "," + str(uid[2]) + "," + str(uid[3])
			print("Card UID: " + tag_id)
			run = False
	db.reload_data()
	return tag_id
#read end

def print_message():
	print("#######################################################")
	print("#######################################################")
	print("Use the following command to interact with the module")
	print("Press 1 to add new card")
	print("Press 2 to modify card access")
	print("Press 3 to exit")

def get_user_input():
	try:
		user_input = input("Waiting for user input... ")
		return user_input
	except NameError as e:
		print("Input must be an integer...")

	except SyntaxError as e:
		print("Input must be an integer...")

def add_new_user(user):
	print("Please scan the new user tag")
	user.tag_id = read()
	user.user_id = db.get_user_id(user.tag_id)
	user.is_admin = db.user_is_admin(user.user_id)

	while user.is_admin:
		print("Admin tag detected...try again")
		user.tag_id = read()
		time.sleep(2)
		user.user_id = db.get_user_id(user.tag_id)
		user.is_admin = db.user_is_admin(user.user_id)

	user.user_id = raw_input("Enter user pid: ")
	print("New user has pid: ", user.user_id)
	print("Is that correct?")
	print("Press 1 for yes")
	print("Press 2 for no")
	user_input = get_user_input()
	while user_input != 1:
		user.user_id = raw_input("Enter user pid: ")
		
		print("New user has pid: ", user.user_id)
		print("Is that correct?")
		print("Press 1 for yes")
		print("Press 2 for no")
		user_input = get_user_input()

	time.sleep(2)
	user.add_user()
	print("New user add with pid: ", user.user_id)


def display_modifiable_values():
	print("#######################################################")
	print("Use the following command to interact with the module")
	for i in range(len(ACCESS_ID)):
		temp = str(i + 1)
		message = "Press " + str(i + 1) + " to toggle " + ACCESS_ID[i]
		print(message)

	message = "Press " + str(len(ACCESS_ID) + 1) + " to print user access values"	
	print(message)

	message = "Press " + str(len(ACCESS_ID) + 2) + " to exit"
	print(message)



def modify_user_access(user):
	print("Scan user id...")
	user.tag_id = read()
	user.user_id = db.get_user_id(user.tag_id)
	user.is_admin = db.user_is_admin(user.user_id)
	
	while user.is_admin:
		print("Admin tag detected...try again")
		user.tag_id = read()
		time.sleep(2)
		user.user_id = db.get_user_id(user.tag_id)
		user.is_admin = db.user_is_admin(user.user_id)

	print("new user tag id = ", user.tag_id)
	if not user.is_registered(user.tag_id):
		print("Invalid card...card not registered")
		return
	user.user_id = user.get_user_id(user.tag_id)
	user.get_access_values()
	user.print_access_values()	

	display_modifiable_values()	
	user_input = get_user_input()
	while user_input != (len(ACCESS_ID)+ 2):
		if user_input <= len(ACCESS_ID):
			user_input = user_input - 1
			message = user.toggle_access(user.user_id, ACCESS_ID[user_input])
			print(message)
		elif user_input == (len(ACCESS_ID) + 1):
			user.get_access_values()
			user.print_access_values()

		display_modifiable_values()
		user_input = get_user_input()	

#main loop
while loop:
	chipid = read()
	
	#check chipid for admin access, replace False with check function
	admin = db.user_is_admin(db.get_user_id(chipid))
	
	#after admin check passes, add next scanned and unregistered chip to database
	while admin:
		print("Admin tag detected.......")
		user = User()
		print_message()
		user_input = get_user_input()
	
		while user_input != 3:
			if user_input == 1:
				user = User()
				add_new_user(user)
			elif user_input == 2:
				modify_user_access(user)

			print_message()
			user_input = get_user_input()
		admin = False
		os.system('clear')	
