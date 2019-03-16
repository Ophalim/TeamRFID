#!/usr/bin/env python

import signal
import time
import sys
import ast
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
from pirc522 import RFID

received = False
loop = True
rdr = RFID()
util = rdr.util()
util.debug = True

client = mqtt.Client()

MQTT_SERVER = "192.168.4.1"
MQTT_SEND = "uid_pi1_send"
MQTT_REC = "uid_pi1_rec" 

package_data_send = {
	"tag id": "send error",
	"data auth": "door access"
}
package_data_received = {}

def read():
	
	#Mostly copied from example Read.p
	#will wait for a rfid tag and return it's uid stored in an array
	print("-----------------------------")
	print("Read UID: Start")
	run = True
	while run:
		rdr.wait_for_tag()
		print("Tag Detection: OK")	
		(error, data) = rdr.request()
		(error, uid) = rdr.anticoll()

		if not error:
			print("UID Read: OK")
			print("Card UID: " +str(uid[0]) +"," +str(uid[1]) +"," +str(uid[2])+"," +str(uid[3]))
			package_data_send["tag id"] = str(uid[0]) +"," +str(uid[1]) +"," +str(uid[2])+"," +str(uid[3])
  			run = False


	return uid

def send(uid):
	
	#takes the uid given by the read function and then sends it to the main pi for verification
	#returns access status
	print("Sent UID: " +str(uid[0]) +"," +str(uid[1]) +"," +str(uid[2])+ "," +str(uid[3]))
	#package_data_send["tag id"] = str(uid[0]) +"," +str(uid[1]) +"," +str(uid[2])+"," +str(uid[3])
	sub()
	publish.single(MQTT_SEND, json.dumps(package_data_send), hostname=MQTT_SERVER)
	client.loop_start()

	return

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(MQTT_REC)


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	package_data_received = ast.literal_eval(msg.payload)

#def logic_control():
	

def sub():
	print("Connected to: "+str(MQTT_SERVER))
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_SERVER, 1883, 60) 

def end_read(signal, frame):
	#termination of code via ctrl + c input
	print("\nTermination Request Detected")
	global loop
	loop = False
	print("Termination Successful")
	rdr.cleanup()
	sys.exit()
	
signal.signal(signal.SIGINT, end_read)


while loop:
	#print(package_data_send)
	#stest = json.dumps(package_data_send)
	#print(stest)
	#dtest = json.loads(stest)
	#print(dtest)
	#dtest2 = ast.literal_eval(stest)
	chipid = read()
	send(chipid)
	print("Main Code Loop: OK")
	print("-----------------------------\n")
	time.sleep(3)
	client.loop_stop()	
