class ProjectConstantClass:
    str_user =""
    str_eagleeye=""
    def __init__(self):
        self.str_user="borhan"
        self.str_eagleeye="eagleeye"
        print ("ProjectConstantClass")
    @staticmethod
    def get_obstacle_enable_response():
        return '{"username":"eagleeye","control_type":"1002","enable_disable":1,"variable_array":"Borhan"}'
    @staticmethod
    def get_obstacle_disable_response():
        return '{"username":"eagleeye","control_type":"1003","enable_disable":1,"variable_array":"Borhan"}'
    @staticmethod
    def get_pwm_enable_response():
        return '{"username":"eagleeye","control_type":"1001","enable_disable":1,"variable_array":"Borhan"}'
    @staticmethod
    def get_dialog_completed_response():
        return '{"username":"eagleeye","control_type":"3001","enable_disable":1,"variable_array":"Borhan"}'
    @staticmethod
    def get_lat_lng_request():
        return '{"username":"eagleeye","control_type":"4001","enable_disable":1,"variable_array":"Borhan"}'
    @staticmethod
    def object_dect():
        return '{"username":"eagleeye","control_type":"5002","enable_disable":1,"variable_array":"Borhan","lat":0.00,"lng":0.00,"alt":100}'
    @staticmethod
    def get_host():
        return '184.72.95.87'
    @staticmethod
    def get_port():
        return 3000
    @staticmethod
    def get_secrer_key():
        return 'secret!'
    @staticmethod
    def get_drone_control_array_type():
        return 2001
    @staticmethod
    def get_defauld_mode_value():
        return 470

    @staticmethod
    def get_drone_lat_lng_response():
        return 4002

    @staticmethod
    def get_drone_object_detect():
        return 5001