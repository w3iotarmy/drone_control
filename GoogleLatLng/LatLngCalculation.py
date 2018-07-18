import argparse
import math

a_constant = 110540
b_constant = 111320

class LatLngCalculationClass:
    def __init__(self):
        self.str_user="borhan"
        self.str_eagleeye="eagleeye"
        print ("LatLngCalculationClass")
    def get_def(self):
        return 5
    @staticmethod
    def get_desired_location(start_lat, start_lng, dist, angel):

        dx = float(float(dist) * float(math.cos(angel)))
        dy = float(float(dist) * float(math.sin(angel)))

        delta_lng = dx / (b_constant * (math.cos(float(start_lat))))
        delta_lat = dy / a_constant

        lng = float(start_lng) + delta_lng
        lat = float(start_lat) + delta_lat
        return_dictionary = dict()
        return_dictionary['lat'] = lat
        return_dictionary['lng'] = lng
        return return_dictionary
    def get_home_location(self,vehicle):
        # Get Vehicle Home location - will be `None` until first set by autopilot
        while not vehicle.home_location:
            cmds = vehicle.commands
            cmds.download()
            cmds.wait_ready()
            if not vehicle.home_location:
                print " Waiting for home location ..."

        # We have a home location.
        print "\n Home location: %s" % vehicle.home_location
        return vehicle.home_location