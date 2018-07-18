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
#vehicle.mode = VehicleMode("STABILIZE")
vehicle.mode = VehicleMode("GUIDED_NOGPS")
while not vehicle.armed:
    print("Waiting for arming..:% s" % vehicle.mode)
    vehicle.armed = True
    time.sleep(1)

print("Taking off!")
# while True:
#     print("Altitude: ", vehicle.location.global_relative_frame.alt)
#     time.sleep(0.5)