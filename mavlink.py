import threading

import time

import sys

import datetime
from droneapi.lib import Location
from dronekit import connect, VehicleMode, LocationGlobalRelative, Battery, GPSInfo, Command
from pymavlink import mavutil
from Databases import DbInitilize, DbConstant
from Constant import Server,CommandConstant,User,ProjectConstant
from Mission import DroneMission
from Utility import ProjectCommand,SdCard,JsonBuilder
from GoogleLatLng import LatLngCalculation
from flask import Flask, render_template
from flask_socketio import SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = Server.ServerClass.get_server_secret_key()
socketio = SocketIO(app)
from socketIO_client import SocketIO as client_socketio, BaseNamespace
import json
from Channels import DroneChannels


vehicle = connect('/dev/ttyACM0', wait_ready=False)

battery_voltage = 0.00
battery_current = 0.00
battery_level = 0
gps_fix = 0
gps_num_sat = 0
gps_lat = 0.00
gps_lon = 0.00
gps_alt = 0
mode =""


def init_sender_socket():
    global my_client_send
    my_client_send = client_socketio(ProjectConstant.ProjectConstantClass.get_host(),ProjectConstant.ProjectConstantClass.get_port())
def send_message(send_msg):
    my_client_send.emit('chat message', send_msg)
#BATTERY INFO
def receive_battery_data():
    # Demonstrate getting callback on any attribute change
    def wildcard_callback(self, attr_name, value):
        #print(" CALLBACK_BATTERY: (%s): %s" % (attr_name, value))
        send_message(JsonBuilder.JsonBuilderClass.get_battery_information(value.voltage,value.current,value.level))
    print("\nAdd attribute callback detecting ANY attribute change L")
    vehicle.add_attribute_listener('battery', wildcard_callback)
previous_milli = 0
#LOCATION INFO
def receive_location_data():
    # Demonstrate getting callback on any attribute change
    def wildcard_callback(self, attr_name, value):
        #print(" CALLBACK_LOCATION: (%s): %s" % (attr_name, value))
        send_message(JsonBuilder.JsonBuilderClass.get_location_information(value.lat,value.lon,value.alt))
    vehicle.add_attribute_listener('location.global_relative_frame', wildcard_callback)
#GPS INFO
def receive_gps_info():
    # Demonstrate getting callback on any attribute change
    def wildcard_callback(self, attr_name, value):
        #print(" CALLBACK_GPS_INFO: (%s): %s" % (attr_name, value))
        send_message(JsonBuilder.JsonBuilderClass.get_gps_inf_information(value.fix_type,value.satellites_visible))
    vehicle.add_attribute_listener('gps_0', wildcard_callback)
#MODE CHANGE
def receive_mode_data():
    @vehicle.on_attribute('mode')
    def wildcard_callback(self, attr_name, value):
        #print(" CALLBACK: Mode changed to (%s), (%s)", value, attr_name)
        send_message(JsonBuilder.JsonBuilderClass.get_mode_information(str(vehicle.mode.name)))
    vehicle.add_attribute_listener('mode', wildcard_callback)
def receive_all_data():
    def wildcard_callback(self, attr_name, value):
        cbv=0
        #print(" All data CALLBACK_ALL: (%s): %s" % (attr_name, value))
    vehicle.add_attribute_listener('*', wildcard_callback)

def all_information():
    previous_milli = 0
    while True:
        current_milli = time.mktime(datetime.datetime.now().timetuple()) * 1000
        if current_milli-previous_milli>=1000:
            print " every 1 second"
            send_message(JsonBuilder.JsonBuilderClass.get_all_information(battery_voltage,battery_current,battery_level,gps_fix,gps_num_sat,gps_lat,gps_lon,gps_alt))
            previous_milli = current_milli

def init_socket():
    my_client = client_socketio(Server.ServerClass.get_server_ip(), Server.ServerClass.get_server_port())
    @socketio.on('chat message')
    def handle_message(message):
        print('received message init: ' + message)

    def socket_receiver(data):
        try:
            #print (data)
            #vehicle = mpstate.get_vehicles()[0]
            obj_data = json.loads(data.replace('\r\n', '\\r\\n'),strict=False)
            #obj_data = json.loads(data,strict=False)
            #obj_data = json.loads(data)
            sender_user = obj_data['u']
            if(sender_user==User.UserClass.ground_user()):
                val = obj_data['action']
                if (val == CommandConstant.CommandConstantClass.is_equal_wp()):
                    #DbInitilize.DbInitializeClass.dbInit()
                    wp_data = obj_data['data']
                    SdCard.SdCardClass.file_write(wp_data)
                    time.sleep(1)
                    if(DroneMission.DroneMissionClass.upload_mission(CommandConstant.CommandConstantClass.get_wp_file_name(),vehicle)):
                        DbInitilize.DbInitializeClass.update_wp_status_true()
                        send_message(JsonBuilder.JsonBuilderClass.get_waypoint_received_response())
                elif (val == CommandConstant.CommandConstantClass.is_equal_start_drone()): ## Start
                    init_aircraft()
                    send_message(JsonBuilder.JsonBuilderClass.get_start_information(vehicle))
                elif (val == CommandConstant.CommandConstantClass.is_equal_arm()):
                    vehicle.armed=True
                    send_message(JsonBuilder.JsonBuilderClass.get_is_arm())
                elif (val == CommandConstant.CommandConstantClass.is_equal_disarm()):
                    vehicle.armed = False
                elif (val == CommandConstant.CommandConstantClass.is_equal_mode()):
                    mode_str = obj_data['data']
                    vehicle.mode = VehicleMode(mode_str)
                elif (val == CommandConstant.CommandConstantClass.is_equal_takeoff()):
                    aTargetAltitude = obj_data['data']
                    send_message(JsonBuilder.JsonBuilderClass.get_is_takeoff())
                    arm_and_takeoff(aTargetAltitude,True)
                elif (val == CommandConstant.CommandConstantClass.is_equal_takeoff_land()):
                    aTargetAltitude = obj_data['data']
                    print "takeoff land"
                    DbInitilize.DbInitializeClass.get_data_wp_status()
                    if(DbInitilize.DbInitializeClass.get_data_wp_status()==0):
                        send_message(JsonBuilder.JsonBuilderClass.get_is_no_waypoint())
                    elif(DbInitilize.DbInitializeClass.get_data_wp_status()==1):
                        DbInitilize.DbInitializeClass.update_wp_status_false()
                        send_message(JsonBuilder.JsonBuilderClass.get_is_takeoff())
                        #arm_and_takeoff(aTargetAltitude,False)
                elif (val == CommandConstant.CommandConstantClass.is_equal_rc_03()):
                    rc_value = int(obj_data['data'])
                    vehicle.channels.overrides['3'] = rc_value
                elif (val == CommandConstant.CommandConstantClass.is_equal_battery_info()):
                    try:
                        voltage=vehicle.battery.voltage
                        current=vehicle.battery.current
                        level=vehicle.battery.level
                    except:
                        print('An error occurred.')
                        voltage = 0.00
                        current = 0.00
                        level = 0
                    send_message(JsonBuilder.JsonBuilderClass.get_battery_information(voltage,current,level))
                elif (val == CommandConstant.CommandConstantClass.is_equal_reboot()):
                    vehicle.reboot()
                    time.sleep(1)
                elif (val == CommandConstant.CommandConstantClass.is_equal_store_param()):
                    #print "\nPrint all parameters (iterate `vehicle.parameters`):"
                    append_string = ""
                    for key, value in vehicle.parameters.iteritems():
                        #print " Key:%s Value:%s" % (key, value)
                        append_string = append_string + str(key)+":"+str(value)+"\n"
                    SdCard.SdCardClass.param_write(append_string)
                    print append_string
                elif (val == CommandConstant.CommandConstantClass.is_equal_home_location()):
                    #home_lat,home_lng = LatLngCalculation.LatLngCalculationClass.get_home_location(vehicle)
                    #print " ",home_lat," ",home_lng
                    init_aircraft()
                elif (val == CommandConstant.CommandConstantClass.is_equal_read_channels()):
                    DroneChannels.DroneChannelsClass.read_channels(vehicle)
            elif sender_user==User.UserClass.self_user():
                cvb=0
                #print ("self message")
        except Exception as error:
            print (error)
        #set_command(data)
    my_client.on('chat message', socket_receiver)
    my_client.wait()
#{"action":"wp","data":""}
def cmddd():
    # add a takeoff command
    cmds = vehicle.commands
    altitude = 100  # target altitude
    pitch = 45  # take off pitch. Need to check if degrees or radians, and what is a reasonable valued.
    cmd = Command(0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                         mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0,
                         pitch, 0, 0, 0, 0, 0, altitude)
    cmds.add(cmd)
    vehicle.commands.upload()
def arm_and_takeoff(aTargetAltitude,test_type):
    print("Basic pre-arm checks", aTargetAltitude)
    # Don't try to arm until autopilot is ready
    # while not vehicle.is_armable:
    #     print(" Waiting for vehicle to initialise...")
    #     time.sleep(1)
    print("Arming motors")
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)
    print("Taking off!")
    vehicle.simple_takeoff(aTargetAltitude)
    while True:
        print(" Altitude: ", vehicle.location.global_relative_frame.alt)
        if vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)
    if test_type==True:
        vehicle.mode = VehicleMode("AUTO")
    elif test_type==False:
        vehicle.mode = VehicleMode("LAND")
def ai_receiver():
    print "AI"
def init_aircraft():
    # api = local_connect()
    # vehicle = api.get_vehicles()[0]
    print "Global Location: %s" % vehicle.location.global_frame
    print "Global Location (relative altitude): %s" % vehicle.location.global_relative_frame
    print "Local Location: %s" % vehicle.location.local_frame
    print "Home  Location: %s" % vehicle.home_location
    print "Home  Location: %s" % vehicle.home_location
    print "Mode %s" % vehicle
    print "Battery %s" % vehicle.battery
    print "Mode %s" % vehicle.mode

def run_thread():
    thread_apm = threading.Thread(target=receive_battery_data)
    thread_apm.daemon = True
    thread_apm.start()

    thread_apm_location = threading.Thread(target=receive_location_data)
    thread_apm_location.daemon = True
    thread_apm_location.start()

    thread_receiver = threading.Thread(target=init_socket)
    thread_receiver.daemon = True
    thread_receiver.start()

    thread_sender = threading.Thread(target=init_sender_socket)
    thread_sender.daemon = True
    thread_sender.start()

    thread_mode_data_response = threading.Thread(target=receive_mode_data)
    thread_mode_data_response.daemon=True
    thread_mode_data_response.start()

    thread_mode_data_response = threading.Thread(target=receive_gps_info)
    thread_mode_data_response.daemon=True
    thread_mode_data_response.start()

    thread_all_data = threading.Thread(target=receive_all_data)
    thread_all_data.daemon = True
    thread_all_data.start()

    thread_all_data = threading.Thread(target=receive_all_data)
    thread_all_data.daemon = True
    thread_all_data.start()

    thread_ai = threading.Thread(target=ai_receiver)
    thread_ai.daemon = True
    thread_ai.start()
if __name__ == '__main__':
    DbInitilize.DbInitializeClass.update_wp_status_false()
    run_thread()
    socketio.run(app)


