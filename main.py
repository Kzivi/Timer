# Import necessary libraries
from machine import I2C, Pin, PWM
import time
import utime
from pico_i2c_lcd import I2cLcd

# Initialize I2C, LCD, button, and buzzer
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
button = Pin(6, Pin.IN, Pin.PULL_DOWN)
buzzer = PWM(Pin(15))

# Initialize variables
s = 0
bs = 0
t = 270
x = 1
y = 1

# Initialize relay control pins
relay1 = Pin(9, Pin.OUT)
relay2 = Pin(10, Pin.OUT)
relay3 = Pin(11, Pin.OUT)
relay4 = Pin(12, Pin.OUT)

# Define musical tones and song
tones = {"G": 392, "C": 523, "E": 349, "F": 415}
song = ["G", "G", "C", "G", "G", "E", "G", "G", "G", "G", "G", "G", "G", "G", "G", "F", "E"]

# Define custom characters for LCD
k1 = bytearray([0x01, 0x01, 0x02, 0x06, 0x04, 0x0C, 0x08, 0x18])
k2 = bytearray([0x01, 0x01, 0x01, 0x02, 0x02, 0x0D, 0x08, 0x10])
k3 = bytearray([0x00, 0x02, 0x0C, 0x10, 0x12, 0x0D, 0x00, 0x00])

c1 = bytearray([0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x10])
c2 = bytearray([0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18, 0x18])
c3 = bytearray([0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C, 0x1C])
c4 = bytearray([0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E, 0x1E])
c5 = bytearray([0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F])

# Initialize LCD with custom characters
I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
lcd.custom_char(6, k1)
lcd.custom_char(7, k2)
lcd.custom_char(8, k3)
lcd.custom_char(1, c1)
lcd.custom_char(2, c2)
lcd.custom_char(3, c3)
lcd.custom_char(4, c4)
lcd.custom_char(5, c5)

# Function to update the LCD screen
def UpdateScreen():
    global s, bs, t, x, y
    if s == 1:
        lcd.clear()
        lcd.blink_cursor_on()
        lcd.move_to(0, 0)
        lcd.putstr("Press to start\n")
        lcd.move_to(0, 1)
        lcd.putstr("[4:30]")
        lcd.move_to(15, 0)
    if s == 2:
        if bs == 0:
            lcd.clear()
            bs = 1
            relay1(1)
            relay2(1)
            relay3(1)
            relay4(1)
        if t >= 0:
            lcd.move_to(0, 0)
            lcd.putstr("Time left: " + str(t))
            if t > 100:
                lcd.move_to(12, 0)
                lcd.putstr("s ")
            elif 10 < t < 100:
                lcd.move_to(11, 0)
                lcd.putstr("s ")
            elif t < 10:
                lcd.move_to(10, 0)
                lcd.putstr("s ")
            lcd.move_to(0, 1)
            lcd.putstr("[")
            lcd.move_to(10, 1)
            lcd.putstr("]")
            t = t - 1
            if t % 5 == 0:
                if x < 10:
                    lcd.move_to(x, 1)
                    if y < 6:
                        lcd.putstr(chr(y))
                        y = y + 1
                    else:
                        x = x + 1
                        y = 1
            lcd.hide_cursor()
        else:
            relay1(0)
            relay2(0)
            relay3(0)
            relay4(0)
            bs = 0
            s = s + 1

# Function to play a musical tone
def playtone(frequency):
    buzzer.duty_u16(1000)
    buzzer.freq(frequency)

# Initialize buzzer and display initial message
buzzer.freq(500)
buzzer.duty_u16(1000)
lcd.clear()
lcd.hide_cursor()
lcd.putstr(" " + chr(6) + "   KRZYMOWSKI\n")
lcd.putstr(chr(7) + chr(8) + "    creative")
time.sleep(3)
buzzer.duty_u16(0)
s = 1
UpdateScreen()

while True:
    while s == 1:
        if button.value():
            s = s + 1
            time.sleep(0.3)
            lcd.clear()
            lcd.hide_cursor()
            lcd.blink_cursor_off()
    while s == 2:
        UpdateScreen()
        time.sleep(1)
        if button.value():
            t = 0
    while s == 3:
        lcd.clear()
        lcd.putstr("Times up!")
        buzzer.duty_u16(1000)
        for i in range(len(song)):
            playtone(tones[song[i]])
            time.sleep(0.3)
        buzzer.duty_u16(0)
        s = 1
        t = 270
        x = 0
        y = 0
        UpdateScreen()