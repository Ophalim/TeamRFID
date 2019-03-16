#!/usr/bin/env python

import signal
import time
import sys
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json
from pirc522 import RFID
from ledControl import LedControl

received = False
loop = True
rdr = RFID()
util = rdr.util()
util.debug = True
led_control = LedControl()
client = mqtt.Client()

MQTT_SERVER = "192.168.4.1"
MQTT_SEND = "uid_pi1_send"
MQTT_REC = "uid_pi2_rec" 


data_auth = "tool access"
package_data_send = {
	"topic": MQTT_REC,
	"tag id": "send error",
	"data auth": data_auth
}
package_data_received = {
	"registered": "False"
}

def read():
	
	#Mostly copied from example Read.p
	#will wait for a rfid tag and return it's uid stored in an array
	print("-----------------------------")
	print("Read UID: Start")
	run = True
        global package_data_received
        package_data_received["registered"] = False
	while run:
		rdr.wait_for_tag()
		print("Tag Detection: OK")
		(error, data) = rdr.request()
		(error, uid) = rdr.anticoll()

		if not error:
			led_control.processing_on()
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
	client.loop_start()
	publish.single(MQTT_SEND, json.dumps(package_data_send), hostname=MQTT_SERVER)
	#client.loop_start()

	return

def on_connect(client, userdata, flags, rc):
	print("Standing by for message from central server with result code " + str(rc))
	client.subscribe(MQTT_REC)


def on_message(client, userdata, msg):
	print(msg.topic+" "+str(msg.payload))
	global package_data_received
	#package_data_received["registered"] = False
	package_data_received = json.loads(msg.payload)
	print("registered = " + str(package_data_received["registered"]))
        print(str(data_auth) + " = " + str(package_data_received["tool access"]))

def logic_control():
	led_control.processing_off()
        if (str(package_data_received["registered"]) == "False"):
		print("flashing access denied light")
		led_control.tg_unregistered_user()
	else:
		if (str(package_data_received["tool access"]) == "True"):
			print("turn on access granted light")
			led_control.tg_valid_user()
		else:
                        print("turn on access denied light")
                        led_control.tg_invalid_user()

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
	chipid = read()
	send(chipid)
	print("Main Code Loop: OK")
	print("*****************************\n")
	time.sleep(1)
	client.loop_stop()
	logic_control()
	print("-----------------------------\n")
