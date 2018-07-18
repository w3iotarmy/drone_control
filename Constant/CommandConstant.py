class CommandConstantClass:
    str_user = ""
    str_eagleeye = ""

    def __init__(self):
        self.str_user = "borhan"
        self.str_eagleeye = "eagleeye"
        print ("ProjectConstantClass")

    @staticmethod
    def is_equal_start_drone():
        return 'start'

    @staticmethod
    def is_equal_home_location():
        return 'home_location'

    @staticmethod
    def is_equal_read_channels():
        return 'read_channels'
    @staticmethod
    def is_equal_wp():
        return 'wp'

    @staticmethod
    def is_equal_arm():
        return 'arm'

    @staticmethod
    def is_equal_disarm():
        return 'disarm'

    @staticmethod
    def is_equal_mode():
        return 'mode'

    @staticmethod
    def is_equal_takeoff():
        return 'takeoff'

    @staticmethod
    def is_equal_takeoff_land():
        return 'takeoff_land'
    @staticmethod
    def is_equal_store_param():
        return 'store_param'

    @staticmethod
    def is_equal_reboot():
        return 'reboot'

    @staticmethod
    def is_equal_battery_info():
        return 'battery'

    @staticmethod
    def is_equal_rc_03():
        return 'rc_03'

    @staticmethod
    def get_wp_file_name():
        return 'wp.txt'