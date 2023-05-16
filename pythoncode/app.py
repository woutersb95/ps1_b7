import RPi.GPIO as GPIO
import atexit #Om een functie te doorlopen wanneer de server afsluit
from flask import Flask, render_template, request
import _thread
from time import sleep
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
PWM1.start(0) #Start 'PWM' met een dutycycle van 0%

distance = 0
TRIG = 26
ECHO = 19
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print ('Waiting a few seconds for the sensor to settle')
time.sleep(2)


GPIO.setmode(GPIO.BCM)				
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

aanuitr = 1
aanuitg = 1
aanuitb = 1
line = "neg"

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

def main():
	global aanuitr
	global aanuitg
	global aanuitb
	global line
	while True:
		
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
		if aanuitb == 1 and line != "blauw":
			PWM.ChangeDutyCycle(50)
			PWM1.ChangeDutyCycle(50)
		if line == "blauw" and aanuitb==0:
			line = "neg"
			print("hallo")
			PWM.ChangeDutyCycle(0)
			PWM1.ChangeDutyCycle(0)
			sleep(1)

			

#main programma in multithread
_thread.start_new_thread(main,())

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/dashboard')
def dashboard():
	return render_template('dashboard.html')


@app.route('/rood',methods=["POST"])
def rood():
	global aanuitr
	#aanuit moet veranderd worden voor return, dus is 1 uit en 0 aan
	if aanuitr == 1:
		aanuitr = 0 
		return "LED is aan"
		
	elif aanuitr == 0:
		aanuitr = 1
		return "LED is uit"	

@app.route('/groen',methods=["POST"])
def groen():
	global aanuitg
	#aanuit moet veranderd worden voor return, dus is 1 uit en 0 aan
	if aanuitg == 1:
		aanuitg = 0 
		return "LED is aan"
		
	elif aanuitg == 0:
		aanuitg = 1
		return "LED is uit"	


@app.route('/blauw',methods=["POST"])
def blauw():
	global aanuitb
	#aanuit moet veranderd worden voor return, dus is 1 uit en 0 aan
	if aanuitb == 1:
		aanuitb = 0 
		return "LED is aan"
		
	elif aanuitb == 0:
		aanuitb = 1
		return "LED is uit"	
def stop():
	GPIO.output(20,0)
	GPIO.output(21,0)
	GPIO.output(23,0)

if __name__ == '__main__':
	atexit.register(stop)
	app.run(debug=True, host='0.0.0.0')
	
