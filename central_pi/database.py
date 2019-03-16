import pyrebase
import json
import sqlite3

'''
## from central_pi to pi_door
package_data_send = {
	"registered": "True/False",
	"is admin": False,
	"door access": True
}

## from pi_door to central_pi
package_data_received = {
	"topic": "channel name",
	"tag id": "safadfasd",
	"data auth": "door access"
}
'''

ACCESS_ID = ["door access", "tool access"]

class Database:
	def __init__(self, filename = "database.json"):
		print("Initializing database")
		self.database_file = filename
		with open(self.database_file) as f:
			self.data = json.load(f)

	def reload_data(self):
		with open(self.database_file) as f:
			self.data = json.load(f)

	def get_user_id(self, tag_id):
		#tags = self.data["Tags"]
		try:
			user_id = self.data["Tags"][tag_id]
			return user_id
		except KeyError as e:
			return None

	def get_user(self, user_id):
		try:
			user = self.data["users"][user_id]
			return user
		except KeyError as e:
			return None

	def user_is_admin(self, user_id):
		#print("user id = ", user_id)
		#user = self.data["users"][user_id]
		
		#if user is None:
			#return False

		try:
			is_admin = self.data["users"][user_id]["admin"]
			return is_admin
		except KeyError as e:
			return False
	
	def get_access_privileged(self, user_id, privileged_id):
		#user = self.data["users"][user_id]		

		#if user is None:
			#return False

		try:
			has_privilege = self.data["users"][user_id][privileged_id]
			return has_privilege
		except KeyError as e:
			return False


class Database_Loader:
	def __init__(self):
		self.config = {
  			"apiKey": "AIzaSyCH2MZ8poMoS3McpnDw6CkM6Uta3NXfgWw",
  			"authDomain": "ece196-318b3.firebaseapp.com",
  			"databaseURL": "https://ece196-318b3.firebaseio.com",
  			"storageBucket": "ece196-318b3.appspot.com",
		}
		self.firebase = pyrebase.initialize_app(self.config)
		self.database = self.firebase.database()

	def reload_database(self, filename = "database.json"):
		entire_database = self.database.get().val()
		with open(filename, 'w') as outfile:
			json.dump(entire_database, outfile)


class SQL_Database:
	def __init__(self, database = "logs.db"):
		self.conn = sqlite3.connect(database)
		self.db = self.conn.cursor()
		
	def update_database(self, timestamp, tag_id, user_id, pi_location, access):
		parms = (timestamp, tag_id, user_id, pi_location, access)
		self.db.execute("INSERT INTO Logs VALUES (?, ?, ?, ?, ?)", parms)
		self.conn.commit()

	def close(self):
		self.conn.close()



class User:
	def __init__(self):
		self.config = {
  			"apiKey": "AIzaSyCH2MZ8poMoS3McpnDw6CkM6Uta3NXfgWw",
  			"authDomain": "ece196-318b3.firebaseapp.com",
  			"databaseURL": "https://ece196-318b3.firebaseio.com",
  			"storageBucket": "ece196-318b3.appspot.com",
		}
		self.firebase = pyrebase.initialize_app(self.config)
		self.database = self.firebase.database()
		self.tag_id = None
		self.user_id = None
		self.is_admin = None
		self.access_values = []

	def add_user(self):
		if self.tag_id is not None and self.user_id is not None:
			data = {self.tag_id: self.user_id}
			self.database.child("Tags").update(data)
			data = {
				"admin": False,
				"door access": False,
				"database access": False
			}
			self.database.child("users").child(self.user_id).update(data)
	def is_registered(self, tag_id):
		user_id = self.database.child("Tags").child(tag_id).get().val()
		if user_id is not None:
			return True
		else:
			return False

	def get_user_id(self, tag_id):
		return self.database.child("Tags").child(tag_id).get().val()

	def modify_access(self, user_id, access_id, access_value):
		data = {access_id: access_value}
		self.database.child("users").child(user_id).update(data)

	def get_access_values(self):
		self.access_values = []
		for i in range(len(ACCESS_ID)):
			val = self.database.child("users").child(self.user_id).child(ACCESS_ID[i]).get().val()
			data = {ACCESS_ID[i]: val}
			self.access_values.append(data)

	def print_access_values(self):
		message = self.user_id + " has the following access privileges:"
		print(message)
		for i in self.access_values:
			print(i)

	def toggle_access(self, user_id,  access_value):
		current_access = self.database.child("users").child(user_id).child(access_value).get().val()
		new_access = not current_access
		data = {access_value: new_access}
		self.database.child("users").child(user_id).update(data)
		message = "Successfully toggled " + access_value + " for " + user_id + " from " + str(current_access) + " to " + str(new_access)
		return message
