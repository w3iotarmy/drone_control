import Adafruit_PCA9685
def reconnect_io_func():
    try:
        pwm = Adafruit_PCA9685.PCA9685()
        return pwm
    except Exception as error:
        if "Remote I/O error" in (error):
            reconnect_io = True
            while reconnect_io:
                try:
                    print("while Error: "+str(error))
                    pwm = Adafruit_PCA9685.PCA9685()
                    # print(pwm)
                    reconnect_io = False
                    return pwm
                except Exception as error:
                    # print((error))
                    reconnect_io = True
pwm = reconnect_io_func()
pwm.set_pwm_freq(60)
class RcControllerClass:
    @staticmethod
    def send_rc_command(rc_0,rc_1,rc_2,rc_3,rc_4,rc_5,rc_6,rc_7):
        print ("RC val RC Controller", rc_0, " ", rc_1, " ", rc_2, " ", rc_3, " ", rc_4, " ", rc_5, " ", rc_6, " ", rc_7)
        pwm.set_pwm(0, 0, int(rc_0))
        pwm.set_pwm(1, 0, int(rc_1))
        pwm.set_pwm(2, 0, int(rc_2))
        pwm.set_pwm(3, 0, int(rc_3))
        pwm.set_pwm(4, 0, int(rc_4))
        pwm.set_pwm(5, 0, int(rc_5))
        pwm.set_pwm(6, 0, int(rc_6))
        pwm.set_pwm(7, 0, int(rc_7))