class DroneChannelsClass:
    @staticmethod
    def read_channels(vehicle):
        print("Read Channels individually:")
        print(" Ch1: %s" % vehicle.channels['1'])
        print(" Ch2: %s" % vehicle.channels['2'])
        print(" Ch3: %s" % vehicle.channels['3'])
        print(" Ch4: %s" % vehicle.channels['4'])
        print(" Ch5: %s" % vehicle.channels['5'])
        print(" Ch6: %s" % vehicle.channels['6'])
        print(" Ch7: %s" % vehicle.channels['7'])
        print(" Ch8: %s" % vehicle.channels['8'])
        print("Number of Channels: %s" % len(vehicle.channels))