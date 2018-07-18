class ServerClass:
    str_user =""
    str_eagleeye=""
    def __init__(self):
        self.str_user="borhan"
        self.str_eagleeye="eagleeye"
        print ("ServerClass")

    @staticmethod
    def get_server_secret_key():
        return 'secret!'
    @staticmethod
    def get_server_ip():
        return '184.72.95.87'
    @staticmethod
    def get_server_port():
        return 3000