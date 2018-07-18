# Drone Control Python File
## Dependency
    RPi.GPIO
    Adafruit_PCA9685
    flask
    flask_socketio
    json 
#### Install
**Install Adafruit PCA9685 I2C device with raspberry pi via I2C Bus**
    
    sudo apt-get install python-smbus 
    sudo apt-get install i2c-tools
    # Test is connected device
    sudo i2cdetect -y 0
    # OR
    sudo i2cdetect -y 1
    sudo apt-get install git build-essential python-dev 
    cd ~ git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git 
    cd Adafruit_Python_PCA9685 
    sudo python setup.py install 
    # if you have python3 installed: 
    sudo python3 setup.py install 
**Flask install**

    pip uninstall gevent
    sudo pip install socketIO_client
    pip install flask
    pip install flask-socketio        
### Download from git
    sudo git clone https://code.leftofthedot.com/borhanreo/drone_control.git
    cd drone_control
    sudo python main.py
    
    
    
### socket io install issue
**If you get any problem then need to uninstall gevent**    
    
    pip2 freeze | grep socket
    sudo pip2 uninstall gevent-socketio
    sudo pip2 uninstall gevent-python
    sudo pip2 install python-socketio
    sudo pip2 install socketIO-client
    sudo pip2 install websocket-client
    
# Install mavlink
### Install
    sudo apt-get update
    sudo apt-get install screen python-wxgtk2.8 python-matplotlib python-opencv python-pip python-numpy python-dev libxml2-dev libxslt-dev python-lxml
    sudo pip install future
    sudo pip install pymavlink
    sudo pip install mavproxy
    
### Show list similar usb port identity  
    python -m serial.tools.list_ports 
    /dev/ttyAMA0
    /dev/ttyUSB0
    /dev/ttyUSB1
    3 ports found
### Need to remember for pip is python2 or python3 here we need pip (python 2)
    pip --version    
### Connect Ardupilot
    bash run.sh
##### Or    
    python mavlink_lib.py --master=/dev/ttyACM0 --baudrate 115200 --aircraft MyCopter  
##### OR    
    bash run.sh     
### Useful mavproxy command
##### show available mod
     mode
##### Guided Mode 
    mode guided
##### Arm    
    arm throttle
##### takeoff    
    takeoff 40
##### Parameter load    
    param load ..\Tools\autotest\default_params\copter.parm
##### Circle mode    
    mode circle
    param set circle_radius 2000         
##### Target altitude 
**Write guided then desire altitude guided ALTITUDE**
    
    guided 100    

**Write guided then desire LAT LNG ALT guided ALTITUDE**    

    guided 22.376666 -121.54464 120
##### save parameter
    param save ./myparams.parm
http://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html
https://ardupilot.github.io/MAVProxy/html/modules/cmdlong.html
#### GPS Data
    master=mpstate.master()
    lat = master.field('GLOBAL_POSITION_INT', 'lat', 0) * 1.0e-7
    lng = master.field('GLOBAL_POSITION_INT', 'lon', 0) * 1.0e-7        
#### Auto open a terminal 
**To auto-start the terminal on boot, open this file with nano:**

    nano ~/.config/lxsession/LXDE-pi/autostart
**Add this line to the end of the file:**

    @lxterminal
**Close, save and reboot**
        
    sudo reboot
    
    
##### Motor can not sync 
--https://youtu.be/Y8G3tua0ezI
 
Power on rpi and run.. **Drone power will be off**   

    All power shuld be off
    cd /home/pi/development/drone_control
    python  python obsAI.py
    RC 3 HIGH / THROTTLE 100% MAXIMUM**
    POWER ON/ CONNECT BATTERY  DRONE** 
    AFTER BEEF COMPLETED then again drone battery power OFF**    
    power on or Plug battery again
    After beef completer then throttle going to minimum**      
    unplug again
    
    
####Reference    
##### Dronekit
http://ardupilot.org/copter/docs/common-lightware-sf40c-objectavoidance.html   
##### OpencV target set 
https://www.pyimagesearch.com/2015/05/04/target-acquired-finding-targets-in-drone-and-quadcopter-video-streams-using-python-and-opencv/
##### Face
https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/
