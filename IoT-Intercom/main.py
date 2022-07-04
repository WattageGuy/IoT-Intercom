import time
from machine import Pin, PWM, I2C
from lib.LCD1602 import LCD1602
from lib.umqtt.simple import MQTTClient

# define frequency for each tone
B0  = 31
C1  = 33
CS1 = 35
D1  = 37
DS1 = 39
E1  = 41
F1  = 44
FS1 = 46
G1  = 49
GS1 = 52
A1  = 55
AS1 = 58
B1  = 62
C2  = 65
CS2 = 69
D2  = 73
DS2 = 78
E2  = 82
F2  = 87
FS2 = 93
G2  = 98
GS2 = 104
A2  = 110
AS2 = 117
B2  = 123
C3  = 131
CS3 = 139
D3  = 147
DS3 = 156
E3  = 165
F3  = 175
FS3 = 185
G3  = 196
GS3 = 208
A3  = 220
AS3 = 233
B3  = 247
C4  = 262
CS4 = 277
D4  = 294
DS4 = 311
E4  = 330
F4  = 349
FS4 = 370
G4  = 392
GS4 = 415
A4  = 440
AS4 = 466
B4  = 494
C5  = 523
CS5 = 554
D5  = 587
DS5 = 622
E5  = 659
F5  = 698
FS5 = 740
G5  = 784
GS5 = 831
A5  = 880
AS5 = 932
B5  = 988
C6  = 1047
CS6 = 1109
D6  = 1175
DS6 = 1245
E6  = 1319
F6  = 1397
FS6 = 1480
G6  = 1568
GS6 = 1661
A6  = 1760
AS6 = 1865
B6  = 1976
C7  = 2093
CS7 = 2217
D7  = 2349
DS7 = 2489
E7  = 2637
F7  = 2794
FS7 = 2960
G7  = 3136
GS7 = 3322
A7  = 3520
AS7 = 3729
B7  = 3951
C8  = 4186
CS8 = 4435
D8  = 4699
DS8 = 4978

# set up pin PWM timer for output to buzzer or speaker
buz = Pin("P8")
tim = PWM(0, frequency=300)
ch = tim.channel(2, duty_cycle=0.5, pin=buz)

# I2C connection pins to LCD
sda = 'P12'
scl = 'P11'

i2c = I2C(1, pins=(sda, scl))

LCD = LCD1602(i2c)

ledPin = Pin('P10', Pin.OUT) # Pin to LED
#Pins for both buttons
blueButton = Pin('P14', Pin.IN)
redButton = Pin('P15', Pin.IN)

zero = [0]

msg = [E7, E7, F6, F6, 0] # Incoming message tone
successRed = [E7, B7, E7, B7, A3, A3, 0] # Red button click tone
successBlue = [E7, B7, E7, B7, B6, B6, 0] # Blue button click tone

# Makes buzzer quiet
for i in zero:
    if i == 0:
        ch.duty_cycle(0)
    else:
        tim=PWM(0, frequency=i)  # change frequency for change tone
        ch.duty_cycle(0.50)
    time.sleep(0.150)

# Establishes a network connection
def do_connect():
    from network import WLAN
    import time
    import pycom
    import machine
    pycom.wifi_mode_on_boot(WLAN.STA)   # choose station mode on boot
    wlan = WLAN() # get current object, without changing the mode
    # Set STA on soft rest
    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.init(mode=WLAN.STA)        # Put modem on Station mode
    if not wlan.isconnected():          # Check if already connected
        print("Connecting to WiFi...")
        LCD.puts("Connecting to") # Shows connection on LCD
        LCD.puts("WiFi...", 0, 1)
        # Connect with your WiFi Credential
        wlan.connect('Your SSID', auth=(WLAN.WPA2, 'Your Passowrd'))
        # Check if it is connected otherwise wait
        while not wlan.isconnected():
            pass
    print("Connected to Wifi")
    LCD.clear()
    LCD.puts("Established") # Shows connected on LCD
    LCD.puts("WiFi connection", 0, 1)
    time.sleep_ms(1000)
    LCD.clear()
    LCD.puts("Awaiting msg") # Shows connected on LCD
    LCD.puts("Screen off...", 0, 1)
    time.sleep_ms(3000)
    LCD.clear()
    LCD.backlight(0)
    LCD.off() # Turns off LCD
    # Print the IP assigned by router
    print('network config:', wlan.ifconfig(id=0))

do_connect() # Establishes WiFi

def continue_check_mqtt(): # Always checks MQTT
    while True:
        mqttc.check_msg()

def notification_check(topic, msg, third, fourth): #Checks MQTT message
    notiValue = msg.decode() # Decodes MQTT message
    n = 16	# Splits every 16 characters
    split_string = [notiValue[i:i+n] for i in range(0, len(notiValue), n)] # Splitted string to fit LCD 16
    if notiValue != "":
        ask_input(split_string, notiValue)

def ask_input(split_string, input): # Displays message and asks for input
    pressed = False
    printed = False
    clicked = False
    start_time = time.time()
    while pressed == False:
      if (redButton.value() == 1) or (blueButton.value() == 1): # Checks if button is pressed
          counterS = time.time() - start_time
          counterS = str(counterS)
          ledPin.value(0) # Turns off LED
          time.sleep_ms(500)
          LCD.clear()
          LCD.puts("Blue: Okay/Yes") # Shows input options on LCD
          LCD.puts("Red: No", 0, 1)
          pressed = True
          while True:
              if redButton.value() == 1: # If red button is pressed
                  answerColor = "No"
                  shortAnswer = "No"
                  clicked = True
              elif blueButton.value() == 1:
                  answerColor = "Okay/Yes"
                  shortAnswer = "Yes"
                  clicked = True
              if clicked == True:
                  time.sleep_ms(1500)
                  LCD.clear()
                  lcdText = "Answered %s to:" % (shortAnswer) # String shown on LCD
                  LCD.puts(lcdText) # Shows choise on LCD
                  # Shows small version of message
                  LCD.puts(split_string[0], 0, 1)
                  lengthOfMessage = str(split_string[0])
                  if len(lengthOfMessage) > 16:
                      LCD.puts("...", 13, 13)
                  color = b"%s" % (answerColor)
                  answerValue = input + " Answered: " + answerColor
                  # Sends all MQTT topics to Node-RED
                  mqttc.publish( answer, answerValue )
                  mqttc.publish( "question", input )
                  mqttc.publish( "answerValue", color )
                  mqttc.publish( "answerTime", counterS )
                  if answerColor == "Okay/Yes": # Plays diffrent tones depending on answer
                      for i in successBlue:
                            if i == 0:
                                ch.duty_cycle(0)
                            else:
                                tim=PWM(0, frequency=i)
                                ch.duty_cycle(0.50)
                            time.sleep(0.150)
                  elif answerColor == "No":
                      for i in successRed: # Plays success sound
                            if i == 0:
                                ch.duty_cycle(0)
                            else:
                                tim=PWM(0, frequency=i)
                                ch.duty_cycle(0.50)
                            time.sleep(0.150)
                  time.sleep_ms(5000)
                  LCD.backlight(0)
                  LCD.clear()
                  continue_check_mqtt()
                  break
      else: # If no button has been pressed continue to show message and play sound
          ledPin.value(1) # Turns LED on
          for i in msg:
              if i == 0:
                  ch.duty_cycle(0)
              else:
                  tim=PWM(0, frequency=i)  # change frequency for change tone
                  ch.duty_cycle(0.50)
              time.sleep(0.150)
          while printed == False:
                  LCD.on()
                  LCD.backlight(1)
                  LCD.clear()
                  showTextTop = split_string[0] # Show MQTT msg on LCD
                  for i in range(len(split_string)):
                      if i == 0:
                          LCD.puts(split_string[i])
                      if i == 1:
                          LCD.puts(split_string[i], 0, 1)
                  time.sleep_ms(1500)
                  printed = True
                  mqttc.publish( "printed", "Received by device" )

# MQTT parameters
CLIENT_NAME = 'notification'
BROKER_ADDR = '172.20.10.2'
mqttc = MQTTClient(CLIENT_NAME, BROKER_ADDR, keepalive=2000)
mqttc.connect()

notification = b'notification' # MQTT Topic for the notification message
answer = b'answer' # MQTT Topic for choise - either red/No or blue/Yes

mqttc.set_callback(notification_check) # function that handles MQTT msg
mqttc.subscribe(notification) # Topic for MQTT subscription

while True:
    mqttc.check_msg() # Checks for MQTT msg
