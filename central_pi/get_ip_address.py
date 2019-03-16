import os
import pyrebase

config = {
  "apiKey": "AIzaSyCH2MZ8poMoS3McpnDw6CkM6Uta3NXfgWw",
  "authDomain": "ece196-318b3.firebaseapp.com",
  "databaseURL": "https://ece196-318b3.firebaseio.com",
  "storageBucket": "ece196-318b3.appspot.com",
}

firebase = pyrebase.initialize_app(config)
db = firebase.database()

output = os.popen("hostname -I").read()

print(output)

data = {"ip_address":output}

db.child("ip_central_pi").set(data)
