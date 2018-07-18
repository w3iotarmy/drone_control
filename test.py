# /usr/bin/env python
# -*- coding: utf-8 -*-
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil
import time

# Receiving from command line
# import argparse
# parser = argparse.ArgumentParser()
# parser.add_argument('--connect',help="PORT_NO")
# args = parser.parse_args()

# Connecting to the vehicle
# connection_string = args.connect
connection_string = "/dev/ttyAMA0,57600"
print("Connecting to...% s" % connection_string)
vehicle = connect('/dev/ttyACM0', wait_ready=False)

# Function to arm and takeoff to a specified altitude
print(vehicle.mode)
vehicle.mode = VehicleMode("STABILIZE")
print "ALT ", vehicle.location.global_relative_frame.alt
time.sleep(5)

# vehicle.mode = VehicleMode("LAND")
# time.sleep(5)
def arm_and_takeoff(aTargetAlt):
    print("Basic Prearm checks..dont touch!!")

    # while not vehicle.is_armable:
    # print("Waiting for vehicle to initialize")
    # time.sleep(2)

    print("Arming Motors..")
    # Copter should arm in Guided-mode
    vehicle.mode = VehicleMode("GUIDED")
    time.sleep(3)
    vehicle.armed = True

    while not vehicle.armed:
        print("Waiting for arming..:% s" % vehicle.mode)
        vehicle.armed = True
        time.sleep(2)

    print("Taking Off..")
    vehicle.simple_takeoff(aTargetAlt)
    time.sleep(5)

    while True:
        print("Altitude: ", vehicle.location.global_relative_frame.alt)
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt >= aTargetAlt * 0.95:
            print("Reached Target Altitude..")
            modeLand()
            # print("Landing....")
            # vehicle.mode = VehicleMode("LAND");
            # print("Vehicle mode:%s"% vehicle.mode)
            break


def modeLand():
    print("Landing now")
    vehicle.mode = VehicleMode("LAND")
    time.sleep(5)
    print("-------------Vehicle is in:-------%s" % vehicle.mode)


arm_and_takeoff(2)
print(vehicle.mode)
print("Vehicle object closed")
vehicle.close()