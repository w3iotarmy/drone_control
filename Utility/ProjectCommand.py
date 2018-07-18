class CommandClass:
    str_user = ""
    str_eagleeye = ""

    def __init__(self):
        self.str_user = "borhan"
        self.str_eagleeye = "eagleeye"
        print ("CommandClass")
    @staticmethod
    def get_arm_string(value):
        if(value==1):
            return 'arm throttle'
        elif value==0:
            return ''
    @staticmethod
    def get_mode_stabilize_string():
        return 'mode stabilize'

    @staticmethod
    def get_mode_land_string():
        return 'mode land'

    @staticmethod
    def get_mode_loiter_string():
        return 'mode loiter'

    @staticmethod
    def get_mode_guided_string():
        return 'mode guided'

    @staticmethod
    def get_mode_rtl_string():
        return 'mode rtl'

    @staticmethod
    def get_mode_althold_string():
        return 'mode alt_hold'