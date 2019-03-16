import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import datetime
import json
import ast
from database import Database, SQL_Database

MQTT_SERVER = "localhost"
MQTT_RECEIVE = "uid_pi1_send"
#MQTT_SEND = "uid_pi1_rec"

db = Database()
sql_db = SQL_Database()

package_data_send = {
	"registered": False,
	"is admin": False
}

def on_connect(client, userdata, flags, rc):
	print("connected with result code ", str(rc))

	client.subscribe(MQTT_RECEIVE)


def on_message(client, userdata, msg):
	client.publish(MQTT_SEND, "some message has been received")

	print(msg.topic + " " + str(msg.payload))
	msg.payload = json.loads(msg.payload)
	
	print(msg.topic + " " + msg.payload)

	#package_data_received = ast.literal_eval(msg.payload)	
	#package_data_received = json.loads(msg.payload)

	#print("data = ", package_data_receive)

	#user_id = db.get_user_id(package_data_received["tad id"])
	
	user_id = "adsfasd"

	if user_id is None:
		package_data_send = {
			"registered": False,
			"is admin": False
		}
	
		package_data_send = json.dumps(package_data_send)	
		client.publish(MQTT_SEND, package_data_send)
		print("invalid tag...")
	else:
		print("valid user...")
		
	if str(msg.payload) == "191,56,80,73" or "148,110,106,23":
		time.sleep(1)
		print("this is working")
		#publish.single(MQTT_SEND, "received on central pie", hostname = MQTT_SERVER)
		client.publish(MQTT_SEND, "received on central pie original")
		print("msg sent")


def request_received(client, userdata, msg):
	global package_data_send
	
	db.reload_data()
	
	print("message received on ", MQTT_RECEIVE)
	print(msg.topic + " " + str(msg.payload))

	msg.payload = json.loads(msg.payload)
	tag_id = msg.payload["tag id"]

	print("tag id = ", msg.payload["tag id"])

	user_id = db.get_user_id(tag_id)
	print("user id in central pi = ", user_id)
	did_access = False

	if user_id is None:
		package_data_send = {
			"registered": False,
			"is admin": False
		}
		package_data_send = json.dumps(package_data_send)
		client.publish(msg.payload["topic"], package_data_send)
		did_access = False
	else:
		is_admin = db.user_is_admin(user_id)
		access_id = msg.payload["data auth"]
		has_access = db.get_access_privileged(user_id, access_id)

		package_data_send = {
			"registered": True,
			"is admin": is_admin,
			access_id: has_access
		}
		package_data_send = json.dumps(package_data_send)
		client.publish(msg.payload["topic"], package_data_send)
		did_access = has_access

	
	print("message successfully send...")

	timeStamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	'''
	tag_data = {
		"tad id": tag_id,
		"name": user_id,
		"timestamp": datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
		"pi location": msg.payload["data auth"],
		"access": did_access	
	}

	with open("logs.json", "a") as f:
		json.dump(tag_data, f, indent = 2)
	'''
	sql_db.update_database(timeStamp, tag_id, user_id, msg.payload["data auth"], did_access)

client = mqtt.Client()
client.on_connect = on_connect
#client.on_message = on_message

client.message_callback_add(MQTT_RECEIVE, request_received)

client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
