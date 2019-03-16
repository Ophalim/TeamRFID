import RPi.GPIO as GPIO
import time

class LedControl:

	def __init__(self):
		print("Initializing led control object")
		self.RED = 36
		self.YEL = 38
		self.GRN = 40
		#GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(self.RED, GPIO.OUT)
		GPIO.setup(self.YEL, GPIO.OUT)
		GPIO.setup(self.GRN, GPIO.OUT)
		GPIO.output(self.YEL, GPIO.HIGH)
		GPIO.output(self.GRN, GPIO.LOW)
		GPIO.output(self.RED, GPIO.LOW)
		
	def tg_valid_user(self):
		print("valid user")
		# TODO: toggle leds for valid user
		GPIO.output(self.YEL, GPIO.LOW)
		GPIO.output(self.RED, GPIO.LOW)
		GPIO.output(self.GRN, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(self.GRN, GPIO.LOW)
		GPIO.output(self.YEL, GPIO.HIGH)

	def tg_invalid_user(self):
		print("invalid user")
		# TODO: toggle leds for invalid user
		GPIO.output(self.YEL, GPIO.LOW)
		GPIO.output(self.GRN, GPIO.LOW)
		GPIO.output(self.RED, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(self.RED, GPIO.LOW)
		GPIO.output(self.YEL, GPIO.HIGH)

	def tg_unregistered_user(self):
		print("unregistered user")
		# TODO: toggle leds for unregisterd user
		t_end = time.time() + 3
		GPIO.output(self.YEL, GPIO.LOW)
		GPIO.output(self.GRN, GPIO.LOW)
		while time.time() < t_end:
			GPIO.output(self.RED, GPIO.HIGH)
			time.sleep(.4)
			GPIO.output(self.RED, GPIO.LOW)
			time.sleep(.4)
		GPIO.output(self.YEL, GPIO.HIGH)

	def processing_off(self):
		print("processing mode")
		# TODO: toggle leds for processing mode
		GPIO.output(self.RED, GPIO.LOW)
		GPIO.output(self.GRN, GPIO.LOW)
		GPIO.output(self.YEL, GPIO.LOW)
	
	def processing_on(self):
		GPIO.output(self.RED, GPIO.HIGH)
		GPIO.output(self.YEL, GPIO.HIGH)
		GPIO.output(self.GRN, GPIO.HIGH) 

	def standby(self):
		GPIO.output(self.YEL, GPIO.LOW)


