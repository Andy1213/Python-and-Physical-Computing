# Python 3.x
# Purpose: simple demo of how to blink an LED using a pushbutton
#
# 2019 04 30 AJL Created file

# standard library
import time

# site packages
import RPi.GPIO as GPIO

# setup GPIO using BCM numbering
GPIO.setmode(GPIO.BCM)

# Pin assignments
LED_Pin = 23
hltPin = 13 # exit program
Button_Pin = 20

# GPIO setup
GPIO.setup(LED_Pin, GPIO.OUT)
GPIO.setup(hltPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Button_Pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    # read button and switch the light
    if GPIO.input(Button_Pin):
        GPIO.output(LED_Pin, GPIO.LOW)
    else:
        GPIO.output(LED_Pin, GPIO.HIGH)

    if GPIO.input(hltPin):
        GPIO.cleanup()  # cleanup all GPIO
        print("Shutting Down")
        exit()


