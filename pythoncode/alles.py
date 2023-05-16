import RPi.GPIO as GPIO
import time
import _thread
import serial
GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)		#importeren en pinnen bepalen
GPIO.setup(21, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)		#importeren en pinnen bepalen
GPIO.setup(27, GPIO.OUT)
PWM = GPIO.PWM(17, 50) #Zet pin 18 op een pwm frequentie van 50Hz
PWM.start(0) #Start 'PWM' met een dutycycle van 0%
PWM1 = GPIO.PWM(21, 50) #Zet pin 18 op een pwm frequentie van 50Hz
PWM1.start(0) 

GPIO.setup(4,GPIO.IN)	   #Pin 19 --> Output
GPIO.setup(22,GPIO.IN)	 #Start 'PWM' met een dutycycle van 0%

distance = 0
TRIG = 26
ECHO = 19
line = "niks"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print ('Waiting a few seconds for the sensor to settle')
time.sleep(5)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

def ultra():
	global distance
	global line
	while True:
		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)
		while GPIO.input(ECHO)==0:
			pulse_start = time.time()
		while GPIO.input(ECHO)==1:
			pulse_end = time.time()
		pulse_duration = pulse_end - pulse_start
		distance = pulse_duration * 17165
		distance = round(distance, 1)
		print ('Distance:',distance,'cm')
		time.sleep(1)
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)

try:
	_thread.start_new_thread(ultra,())
	while True:
		if distance < 5:
			PWM.ChangeDutyCycle(0)
			PWM1.ChangeDutyCycle(0)
		if distance > 5:
			if GPIO.input(4) and GPIO.input(22) and line != "rood":
				PWM.ChangeDutyCycle(70)
				PWM1.ChangeDutyCycle(70)
			if GPIO.input(22) == 0 and line != "rood":
				PWM.ChangeDutyCycle(0)
				PWM1.ChangeDutyCycle(70)
			if GPIO.input(4) == 0 and line != "rood":
				PWM.ChangeDutyCycle(70)
				PWM1.ChangeDutyCycle(0)
			if line == "rood":
				PWM.ChangeDutyCycle(0)
				PWM1.ChangeDutyCycle(0)
				time.sleep(2)
				line = "niks"




except KeyboardInterrupt:
	GPIO.output(20, 0)			#motor stilleggen
	GPIO.output(21, 0)
	

	GPIO.cleanup()
	quit()
	sys.exit()
