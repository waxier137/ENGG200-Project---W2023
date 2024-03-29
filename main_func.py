# Libraries import
import urequests
from servo import Servo
from machine import Pin, ADC, I2C
import time
from lcd_api import LcdApi
from pico_i2c_lcd import I2cLcd
from neopixel import Neopixel
import network
ssid = 'airuc-guest' # This should be ‘airuc-guest’ on campus Wi-Fi
password = 'YOUR WIFI PASSSWORD HERE'

I2C_ADDR     = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16

pin_servo = 28
pin_button = 27
pin_SDA_LCD = 0
pin_SCL_LCD = 1
pin_strip_leds_1 = 22
pin_strip_leds_1 = 21


'''decks = {'hearts':['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
         ,'spades':[2,6,10,14,18,22,26,30,34,38,42,46,50]
         ,'diamonds':[3,7,11,15,19,23,27,31,35,39,43,47,51]
         ,'clubs':[4,8,12,16,20,24,28,32,36,40,44,48,52]}
'''
# First ever define
cards_name = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
SG90_Servo = Servo(pin = pin_servo)
sda_lcd = machine.Pin(pin_SDA_LCD)
scl_lcd = machine.Pin(pin_SCL_LCD)
#strip_led = Neopixel(30,0,pin_strip_leds,'GRB')
strip_led_1 = Pin(22, Pin.OUT)
strip_led_2 = Pin(21, Pin.OUT)
Button = Pin(pin_button, Pin.PULL_UP, Pin.PULL_DOWN)

i2c_controller = 0
i2c = I2C(i2c_controller, sda=sda_lcd, scl=scl_lcd, freq=400000) 
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)

heart = bytearray([0x00,0x0A,0x1F,0x1F,0x0E,0x04,0x00,0x00])
lcd.custom_char(0, heart)
spade = bytearray([0x00,0x04,0x0E,0x1F,0x1B,0x04,0x0E,0x00])
lcd.custom_char(1, spade)
diamond = bytearray([0x00,0x04,0x0E,0x1F,0x1F,0x0E,0x04,0x00])
lcd.custom_char(2, diamond)
club = bytearray([0x00,0x0E,0x0E,0x1F,0x1B,0x04,0x0E,0x00])
lcd.custom_char(3, club)
# Functions
def get_response_API() -> int:
    # Get response from API
    response = urequests.get("http://www.randomnumberapi.com/api/v1.0/random?min=1&max=52&count=1")
    if response.status_code == 200:
        # Successful request
        print("Successfully get response from API")
    else:
        # Failure request
        print("Error response: %s" % response.status_code)
    rand_num = response.json() # Array of random numbers (contains 1 number)
    response.close()
    return rand_num[0] # Return random number

# Angel from 0-180
def Servo_Function(angel) -> None:
    SG90_Servo.move(90)
    time.sleep(2)
    SG90_Servo.move(145)
    time.sleep(1)
    SG90_Servo.move(30)
    time.sleep(1)
    SG90_Servo.move(90)
    time.sleep(1)
    SG90_Servo.move(60)
    time.sleep(1.2)
    SG90_Servo.move(120)
    time.sleep(0.5)
    SG90_Servo.move(90)
    time.sleep(0.5)
    SG90_Servo.move(45)
    time.sleep(1)
    
# Print on lcd
def print_on_lcd(string) -> None:
    if len(string) < 16:
        lcd.putstr(string)
        time.sleep(0.8)
    else:
        for i in range(len(string) - 15):
            lcd.putstr(string[i:i+16])
            time.sleep(0.6)
            lcd.move_to(0,0)
    time.sleep(5)
    lcd.clear()

# Turn led on or off
#def strip_led(color,status_led):
    #strip_led.fill(color[0],color[1],color[2])
    #if status_led:
       # strip_led.toggle()
       # time.sleep(0.1)
  #  else:
      #  strip_led.low()
  # return
# Connect wifi
def connect():
    # Connect to WLAN
    # Connect function from https://projects.raspberrypi.org/en/projects/get-started-pico-w/2
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid) # Remove password if using airuc-guest
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        time.sleep(1)
try:
    connect()
except KeyboardInterrupt:
    machine.reset()
print('Wifi connected')

def __main__():
    while True:
        cards = get_response_API()
        print(cards)
        number_card = cards // 4
        type_card = ""
        if cards % 4 == 0:
            angel_of_cards = 45 # hearts
        elif cards % 4 == 1:
            angel_of_cards = 75 # spades
        elif cards % 4 == 2:
            angel_of_cards = 115 # diamonds
        else:
            angel_of_cards = 145 # clubs
        Servo_Function(angel_of_cards)
        SG90_Servo.move(angel_of_cards)
        string_on = cards_name[cards // 4] + chr(cards%4)
        strip_led_1.toggle()
        strip_led_2.toggle()
        print_on_lcd(string_on)
        strip_led_1.off()
        strip_led_2.off()
        print_on_lcd('Hold button to continue')
        print(Button.value())
        if Button.value() == 0:
            print_on_lcd('Thank you for playing')
            print_on_lcd('Have a good day!')
            return
        else:
            print_on_lcd('Next card')
__main__()
SG90_move(0)
lcd.clear()
