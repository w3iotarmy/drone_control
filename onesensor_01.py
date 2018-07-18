from __future__ import division
import time
import RPi.GPIO as GPIO
import Adafruit_PCA9685
from flask import Flask, render_template
from flask_socketio import SocketIO
from dronekit import connect, VehicleMode, LocationGlobalRelative, Battery, GPSInfo, Command
vehicle = connect('/dev/ttyACM0', wait_ready=False)
vehicle.mode = VehicleMode("GUIDED")
while not vehicle.armed:
    print("Waiting for arming..:% s" % vehicle.mode)
    vehicle.armed = True
    time.sleep(1)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

i = -1
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 60)  # channel=12 frequency=50Hz
p.start(0)


def initGpioPwm(x):
    if x == 1:
        p.ChangeDutyCycle(1)
        time.sleep(0.1)
    elif x == 2:
        p.ChangeDutyCycle(3.5)
        time.sleep(0.1)
    if x == 3:
        p.ChangeDutyCycle(4.4)
        # time.sleep(0.5)
    elif x == 4:
        p.ChangeDutyCycle(5.2)
        # time.sleep(0.5)
    elif x == 5:
        p.ChangeDutyCycle(60)
        # time.sleep(0.5)
    elif x == 6:
        p.ChangeDutyCycle(6.8)
        # time.sleep(0.5)
    elif x == 7:
        p.ChangeDutyCycle(7.7)
        # time.sleep(0.5)
    elif x == 5:
        p.ChangeDutyCycle(90)
        # time.sleep(0.5)
    else:
        x = 0
        # print("nothings")
        # Do the default


def reconnect_io_func():
    try:
        pwm = Adafruit_PCA9685.PCA9685()
        return pwm
    except Exception as error:
        if "Remote I/O error" in (error):
            reconnect_io = True
            while reconnect_io:
                try:
                    # print("while Error: "+str(error))
                    pwm = Adafruit_PCA9685.PCA9685()
                    # print(pwm)
                    reconnect_io = False
                    return pwm
                except Exception as error:
                    # print((error))
                    reconnect_io = True


servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
pwm = reconnect_io_func()
from socketIO_client import SocketIO as client_socketio, BaseNamespace

my_client = client_socketio('184.72.95.87', 3000)
str = ""


@socketio.on('chat message')
def handle_message(message):
    x = 0
    # print('received message: ' + message)


# my_client.emit('chat message', str)
# print(str)
def doSomething(data):
    alphabet = data
    dataStr = alphabet.split(":")  # split string into a list
    i = 0
    # pwm = reconnect_io_func()
    for temp in dataStr:
        print temp
        print("Waiting for arming..:% s" % vehicle.mode)
        # print data
        # val= int(data)

        if i == 0:
            val = int(temp)
            try:
                pwm.set_pwm(0, 0, val)
            except Exception as error:
                x = 0
                # print("error")
                # pwm.set_pwm(4, 0, 52)
        elif i == 1:
            val = int(temp)
            pwm.set_pwm(1, 0, val)
        elif i == 2:
            val = int(temp)
            pwm.set_pwm(2, 0, val)
        elif i == 3:
            val = int(temp)
            pwm.set_pwm(3, 0, val)
        elif i == 4:
            val = int(temp)
            pwm.set_pwm(4, 0, val)
        elif i == 5:
            val = int(temp)
            pwm.set_pwm(5, 0, val)
        elif i == 6:
            val = int(temp)
            pwm.set_pwm(6, 0, val)
        elif i == 7:
            val = int(temp)
            #vehicle.mode = VehicleMode("GUIDED")
            #time.sleep(5)
            pwm.set_pwm(7, 0, val)
        # elif i==8:
        # val=int(temp)
        # initGpioPwm(val)
        else:
            x = 0
            # print ("Drone Nothing")
        # print (temp)
        # print (i)
        i = i + 1
        # pwm.set_pwm(0, 0, servo_min)
        # time.sleep(1)
        # pwm.set_pwm(0, 0, servo_max)
        # time.sleep(1)


def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60  # 60 Hz
    # print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096  # 12 bits of resolution
    # print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)


# Set frequency to 60hz, good for servos.
# pwm = reconnect_io_func()
pwm.set_pwm_freq(60)
# pwm.set_pwm(0, 0, 420)
# pwm.set_pwm(1, 0, 420)
# pwm.set_pwm(2, 0, 307)
# pwm.set_pwm(3, 0, 420)
# pwm.set_pwm(4, 0, 307)
# pwm.set_pwm(5, 0, 307)
# pwm.set_pwm(6, 0, 307)
# pwm.set_pwm(7, 0, 307)
# pwm.set_pwm(8, 0, 0)
# my_client.emit('chat message', "420:420:307:420:307:307:307:307:0")

my_client.on('chat message', doSomething)
my_client.wait()

if __name__ == '__main__':
    socketio.run(app)
