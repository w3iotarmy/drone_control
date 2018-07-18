#mmcblk0p2
import threading
import RPi.GPIO as GPIO
import time
import Adafruit_PCA9685
from time import sleep
from flask import Flask, render_template
from flask_socketio import SocketIO
import json
import time
from Constant import ProjectConstant
from GoogleLatLng import LatLngCalculation
obstacle_diable_response = ProjectConstant.ProjectConstantClass.get_obstacle_disable_response()
obstacle_enable_response = ProjectConstant.ProjectConstantClass.get_obstacle_enable_response()
pwm_enable_response = ProjectConstant.ProjectConstantClass.get_pwm_enable_response()
print (obstacle_diable_response," ", obstacle_enable_response)

drone_control_array_type=ProjectConstant.ProjectConstantClass.get_drone_control_array_type()
modeValue=ProjectConstant.ProjectConstantClass.get_defauld_mode_value()
sensor_enable=False
lat_lng_request = ProjectConstant.ProjectConstantClass.get_lat_lng_request()

# allow the camera to warmup
time.sleep(0.1)
pwm_enabled_code=2001

left_or_right=0
control_pwm=420
control_time=1


app = Flask(__name__)
app.config['SECRET_KEY'] = ProjectConstant.ProjectConstantClass.get_secrer_key()
socketio = SocketIO(app)

from socketIO_client import SocketIO as client_socketio, BaseNamespace

my_client = client_socketio(ProjectConstant.ProjectConstantClass.get_host(), ProjectConstant.ProjectConstantClass.get_port())
fl_mode_stabilize=1
fl_mode_loiter=2
fl_mode_rtl=3
fl_mode_land=4
fl_mode_alt_hold=5
fl_mode_auto=6
def send_message(send_msg):
    my_client_send = client_socketio(ProjectConstant.ProjectConstantClass.get_host(), ProjectConstant.ProjectConstantClass.get_port())
    my_client_send.emit('chat message', send_msg)
    #print(str)


GPIO.setmode(GPIO.BCM)
TRIG = 19
ECHO = 26
pulse_end_01 =0.00
pulse_start_01 = 0.00
pulse_duration =0.00
alt_holt_code=456
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


def doSomething(data):
    print (data)
    obj_data = json.loads(data)
    val = int(obj_data['enable_disable'])
    control_type = int(obj_data['control_type'])

    if control_type==1:
        if val == 1:
            global sensor_enable
            sensor_enable = True
            # obstacle enabled
            str = obstacle_enable_response
            send_message(str)
        elif val == 2:
            global sensor_enable
            sensor_enable = False
            # obstacle disable
            str = obstacle_diable_response
            send_message(str)
            # print (fruits_list)
    elif control_type==2:
        pwm.set_pwm(0, 0, 420)
        pwm.set_pwm(1, 0, 420)
        pwm.set_pwm(2, 0, 307)
        pwm.set_pwm(3, 0, 420)
        pwm.set_pwm(4, 0, 307)
        pwm.set_pwm(5, 0, 307)
        pwm.set_pwm(6, 0, 307)
        pwm.set_pwm(7, 0, 307)
        pwm.set_pwm(8, 0, 0)
        #pwn signal enabled
        str=pwm_enable_response
        send_message(str)
    elif control_type == 3:
        global modeValue
        modeValue=470
    elif control_type==4:
        global modeValue
        modeValue=348
    elif control_type== ProjectConstant.ProjectConstantClass.get_drone_lat_lng_response():
        receive_lat = obj_data['lat']
        receive_lng=  obj_data['lng']
        desire_lat_lng =LatLngCalculation.LatLngCalculationClass.get_desired_location(receive_lat,receive_lng,500,135)
        print ("Response data ", receive_lat," ",receive_lng)
        print ("desired data ", desire_lat_lng['lat'],",",desire_lat_lng['lng'])
###################### object code here and send to target lat lng alt
    elif control_type == ProjectConstant.ProjectConstantClass.get_drone_object_detect():
        print "Object detect"
        send_message(ProjectConstant.ProjectConstantClass.object_dect())
    elif control_type==drone_control_array_type:
        obj_data_obstacle=obj_data['variable_array']
        spilit_data = obj_data_obstacle.split(",")
        global control_time
        global control_pwm
        control_pwm=spilit_data[1]
        control_time=spilit_data[2]
        str = ProjectConstant.ProjectConstantClass.get_dialog_completed_response()
        send_message(str)

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


def going_stabilize():
    modeLoiter = 307
    pwm.set_pwm(4, 0, modeLoiter)
def going_automode():
    modeLoiter = 496
    pwm.set_pwm(4, 0, modeLoiter)
def going_loiter():
    modeLoiter = 348
    pwm.set_pwm(4, 0, modeLoiter)
def going_alt_hold_mode():
    mode = 456
    pwm.set_pwm(4, 0, mode)
def goingDrone(pinNumber,value):
    pwm.set_pwm(pinNumber, 0, value)
def random_drone_control():
    print ("Going Throttle up 70% ")
    #465 is the throttle up 70 %
    pwm.set_pwm(2, 0, 465)
    sleep(2)
    print ("Going to mode ")
    pwm.set_pwm(4, 0, modeValue)
    print ("Going to sleep 5 sec ")
    sleep(3)
    print ("Going to left/right PWM=", control_pwm," TIME=", control_time)
    pwm.set_pwm(0, 0, int(control_pwm))
    sleep(int(control_time))
    pwm.set_pwm(0, 0, 420)
    sleep(int(control_time))
    pwm.set_pwm(0, 0, int(control_pwm))
    sleep(int(control_time))
    pwm.set_pwm(0, 0, 420)
    sleep(int(control_time))
    pwm.set_pwm(4, 0, modeValue)
    sleep(5)
    # Going to Auto mode
    pwm.set_pwm(4, 0, 500)
    global sensor_enable
    sensor_enable = False
def drone_tast_start():
    print ("Going Throttle up 70% ")
    # 465 is the throttle up 70 %
    pwm.set_pwm(2, 0, 465)
    ##Going to LOITER  mode for
    print ("Going to mode LOITER")
    pwm.set_pwm(4, 0, 348)

    str = ProjectConstant.ProjectConstantClass.get_lat_lng_request()
    send_message(str)
    global sensor_enable
    sensor_enable = False
def drone_final_task(lat,lng):
    print(lat," ",lng)
#it will work when drone going to ALT_HOLD Mode
def throttle_up():
    pwm.set_pwm(2, 0, 507)
def object_dectec_01():
    print ("obs Detect")
    pwm.set_pwm(4, 0, modeValue)
    sleep(5)
    print("set pwm ", int(control_pwm))
    pwm.set_pwm(0, 0, int(control_pwm))
    print("set time delay ", int(control_time))
    sleep(int(control_time))
    # strait and wait 5 second
    pwm.set_pwm(0, 0, 420)
    pwm.set_pwm(4, 0, modeValue)
    sleep(5)
    # Going to Auto mode
    pwm.set_pwm(4, 0, 500)


def object_dectec():
    print ("obs Detect")
    # going_stabilize()

    # going to Loiter Mode
    #pwm.set_pwm(4, 0, 350)
    # going alt_hold mode
    print ("")
    pwm.set_pwm(4, 0, modeValue)
    sleep(5)
    # turn left until 0.5 second
    sendValueBACKWARD = 490
    pwm.set_pwm(0, 0, sendValueBACKWARD)
    sleep(0.5)
    # strait and wait 5 second
    pwm.set_pwm(0, 0, 420)
    pwm.set_pwm(4, 0, modeValue)
    sleep(5)
    # Going to Auto mode
    pwm.set_pwm(4, 0, 500)

    # if fleft==False:
    #     sleep(2)
    # fleft=True
    # sendValueBACKWARD = 455
    # pwm.set_pwm(0, 0, sendValueBACKWARD)
def obs_test():
    cc='{"username":"orhan","control_type":"1","enable_disable":1,"variable_array":"Borhan"}'
    msg= '{"username":"orhan","control_type":"1","enable_disable":1,"variable_array":"Borhan","name":"John","age":30,"cars":"ABC"}'
    send_message(msg)
def read_sensor():
    fleft=False
    while True:
        if sensor_enable:
            # print ("dfsfdsf")
            GPIO.output(TRIG, False)
            time.sleep(0.1)
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)
            GPIO.setwarnings(False)

            while GPIO.input(ECHO) == 0:
                global pulse_start_01
                pulse_start_01 = time.time()
                # print ("Start ", pulse_start)
            while GPIO.input(ECHO) == 1:
                global pulse_end_01
                pulse_end_01 = time.time()
            pulse_duration = pulse_end_01 - pulse_start_01
            distance = pulse_duration * 17150
            distance = round(distance, 2)

            if distance > 10 and distance < 400:
                if (distance < 100):
                    #print ("Distance obs:", distance - 0.5, "cm", obsCounter, " ", modeValue)
                    #global obsCounter
                    #obsCounter=obsCounter+1
                    object_dectec_01()
                    #obs_test()
                #print ("Distance:", distance - 0.5, "cm", obsCounter," ", modeValue)
                print ("Distance:", distance - 0.5, "cm"," ", modeValue, control_pwm, " ", control_time)
            else:
                if (fleft):
                    # pwm.set_pwm(4, 0, 500)
                    # sendValueBACKWARD = 420
                    # pwm.set_pwm(0, 0, sendValueBACKWARD)
                    fleft = False

def run_thread():
    while True:
        if sensor_enable:
            #random_drone_control()
            drone_tast_start()
            print ("finish and waiting for new command running....")
global pwm
pwm = reconnect_io_func()

#thread = threading.Thread(target=read_sensor)
thread = threading.Thread(target=run_thread)
thread.daemon = True
thread.start()

servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096

pwm.set_pwm_freq(60)
my_client.on('chat message', doSomething)
my_client.wait()


@socketio.on('chat message')
def create_json_array():
    str = '{"username":"orhan","control_type":"1","enable_disable":1,"variable_array":"Borhan"}'
    my_client.emit('chat message', str)
    print(str)

if __name__ == '__main__':
    send_message()
    socketio.run(app)
    pwm.set_pwm(0, 0, 420)
    pwm.set_pwm(1, 0, 420)
    pwm.set_pwm(2, 0, 307)
    pwm.set_pwm(3, 0, 420)
    pwm.set_pwm(4, 0, 307)
    pwm.set_pwm(5, 0, 307)
    pwm.set_pwm(6, 0, 307)
    pwm.set_pwm(7, 0, 307)
    pwm.set_pwm(8, 0, 0)

    create_json_array()
    #array = '{"fruits": ["apple", "banana", "orange"]}'
    #create_json_array(array)
    #read_sensor()



